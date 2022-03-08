
import logging
import requests
import os

from functools import lru_cache
from fastapi import Body, Depends, FastAPI
from requests.exceptions import Timeout
from logging.config import dictConfig
from requests.auth import HTTPBasicAuth

from . import config
from arthmate_lender_handoff_service.logger.config import LogConfig
from arthmate_lender_handoff_service.helpers.functions import create_user_data, create_loan_request_data, \
    create_loan_repayment_data, create_user_document_upload_data, create_loan_document_upload_data
from arthmate_lender_handoff_service.helpers.generics import response_to_dict, download_from_s3
import mimetypes
import urllib.request

app = FastAPI()

dictConfig(LogConfig().dict())
logger = logging.getLogger("arthmate-lender-handoff-service")


@lru_cache()
def get_settings():
    return config.Settings()


logger = logging.getLogger("arthmate-lender-handoff-service")


@app.post("/process-automator-data")
async def post_automator_data(
        payload: dict = Body(...),
        settings: config.Settings = Depends(get_settings),
):
    try:

        # prepare the user data from perdix data
        user_info = await create_user_data(payload['enrollmentDTO']['customer'])
        # logger.info(user_info)

        # call all the urls from config where the prepared data needs to be posted
        user_create_url = settings.user_url
        loan_request_url = settings.loan_url
        repayment_request_url = settings.repayment_url
        user_document_url = settings.user_document_upload_url
        loan_document_url = settings.loan_document_upload_url
        disbursement_status_url = settings.disbursement_status_url

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        # Post the prepared user data to the endpoint - 1
        user_response = requests.post(
            user_create_url,
            auth=HTTPBasicAuth(settings.username, settings.password),
            json=user_info,
            headers=headers)

        # Check for the status codes and the message from the response
        if user_response.status_code == 401:
            logger.error("Not Authorised to post the data, please login with correct credentials: ")
        elif user_response.status_code == 400:
            logger.error("Please provide all details or verify date of birth field ")
        elif user_response.status_code == 503:
            logger.error("Customer endpoint is not available, please connect later")
        elif user_response.status_code == 200:
            # convert the response to dictionary to get the uuid
            user_dict = response_to_dict(user_response)

            # check whether there is body attribute in the response to get used_by_uuid
            response_uuid_check = user_dict.get('body')
            if response_uuid_check:
                response_uuid = response_uuid_check['used_by_uuid']
                am_user_token = response_uuid
                sm_user_id = user_info['sm_user_id']

                # prepare user document data with the uuid which we got as a response
                # along with userid
                document_info = await create_user_document_upload_data(payload['loanDTO']['loanAccount'], sm_user_id, am_user_token)

                # Get the file object information from the perdix data
                file_object = document_info.get('fileObject', 'f45ff335-6bc3-42b1-b152-9db71e735581')
                file_url = settings.file_stream_url + file_object

                # Find the extension of the file object
                response = requests.get(file_url)
                content_type = response.headers['content-type']
                extension = mimetypes.guess_extension(content_type)

                # Find the size of the file object
                file_size = requests.get(file_url)
                print(len(file_size.content))

                # Download the file and save the file withe name of the object with the extension
                urllib.request.urlretrieve(file_url, file_object + extension)

                # upload the file to the endpoint
                files = {'file': open(file_object + extension, 'rb')}

                # post the file along with other fields for the document upload api endpoint - 2
                user_document_response = requests.post(user_document_url,
                                                       auth=HTTPBasicAuth(settings.username, settings.password),
                                                       data=document_info,
                                                       files=files,
                                                       )

                print(user_document_response.content)
                # Prepare loan request data
                loan_info = await create_loan_request_data(payload['loanDTO']['loanAccount'], sm_user_id, am_user_token)

                # post the prepared loan request to the api endpoint - 3
                loan_response = requests.post(loan_request_url,
                                              auth=HTTPBasicAuth(settings.username, settings.password),
                                              json=loan_info,
                                              headers=headers
                                              )

                # Check for the status codes and the message from the response
                if loan_response.status_code == 500:
                    logger.error("Please check the field names")
                elif loan_response.status_code == 200:
                    # convert the response to dictionary to get the amlid
                    loan_dict = response_to_dict(loan_response)

                    # check whether there is body attribute in the response to get aml_id
                    loan_response_amlid_check = loan_dict.get('body')

                    # if we have body attribute then the new aml_id is generated
                    if loan_response_amlid_check:
                        loan_response_amlid = loan_response_amlid_check['aml_id']
                        am_loan_id = loan_response_amlid
                        am_user_token = response_uuid

                        # post the aml_id to the disbursement status endpoint- 4
                        disbursement_status_response = requests.post(disbursement_status_url,
                                                                     auth=HTTPBasicAuth(settings.username, settings.password),
                                                                     data=am_loan_id,
                                                                     files=files,
                                                                    )
                        print(disbursement_status_response)

                        # prepare the data for loan document upload along with
                        loan_document_upload_info = create_loan_document_upload_data(
                            payload['loanDTO']['loanAccount'], sm_user_id, am_loan_id)

                        # Get the file object information from the perdix data
                        file_object = document_info.get('fileObject', 'f45ff335-6bc3-42b1-b152-9db71e735581')
                        file_url = settings.file_stream_url + file_object

                        # Find the extension of the file object
                        response = requests.get(file_url)
                        content_type = response.headers['content-type']
                        extension = mimetypes.guess_extension(content_type)

                        # Find the size of the file object
                        file_size = requests.get(file_url)
                        print(len(file_size.content))

                        # Download the file and save the file withe name of the object with the extension
                        urllib.request.urlretrieve(file_url, file_object + extension)

                        # upload the file to the endpoint
                        files = {'file': open(file_object + extension, 'rb')}

                        # post the loan documents to the loan document endpoint- 5
                        loan_document_response = requests.post(loan_document_url,
                                                               auth=HTTPBasicAuth(settings.username, settings.password),
                                                               data=loan_document_upload_info,
                                                               files=files,
                                                               )

                        # print(loan_document_response)
                        repayment_info = await create_loan_repayment_data(payload['loanDTO']['loanAccount'], am_loan_id,
                                                                          am_user_token)
                        # print('repayment ', repayment_info)

                        # post the repayment data to the repayment endpoint- 6
                        repayment_response = requests.post(repayment_request_url,
                                                           auth=HTTPBasicAuth(settings.username, settings.password),
                                                           json=repayment_info,
                                                           headers=headers
                                                           )
                        print('repayment response', repayment_response.content)
    except Timeout as ex:
        logger.error("Error Occurred: ", ex)

    return {"result": "success"}



