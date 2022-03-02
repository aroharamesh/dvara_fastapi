import json
from pydantic import BaseSettings
from operator import itemgetter
from fastapi import FastAPI, Request, Body, status, HTTPException, Response
import requests
from requests.exceptions import Timeout
from fastapi.testclient import TestClient
from commons import env, get_env, get_env_or_fail, _raise

app = FastAPI()

client = TestClient(app)


# class Settings(BaseSettings):
#     app_name: str = "perdixData"
#     source_api: ""
#     user_create_api: str
#     loan_create_api: str

#     class Config:
#         env_file = ".env"

# def get_settings():
#     return Settings()

async def create_user_data(data):
    customer_info = data['enrollmentDTO']['customer']
    sm_user_id, firstName, lastName, middleName, gender, \
    fatherFirstName, fatherLastName, fatherMiddleName, maritalStatus, \
    mobilePhone, email, doorNo, street, locality, district, state, pincode, \
    panNo = itemgetter('id', 'firstName', 'lastName', 'middleName', 'gender', 'fatherFirstName', 'fatherLastName', 'fatherMiddleName', 'maritalStatus', 'mobilePhone', 'email', 'doorNo', 'street', 'locality', 'district', 'state', 'pincode', 'panNo')(customer_info)
    
    firstName = (firstName if firstName else "")
    lastName = (lastName if lastName else "")
    middleName = (middleName if middleName else "")
    full_name = firstName + middleName + lastName
    
    gender = ('M' if gender=="MALE" else "F")

    fatherFirstName = (fatherFirstName if fatherFirstName else "")
    fatherLastName = (fatherLastName if fatherLastName else "")
    fatherMiddleName = (fatherMiddleName if fatherMiddleName else "")
    father_full_name = fatherFirstName + fatherMiddleName + fatherLastName
    # Missing attributes
    # "res_type": "Rent",
    #     "shop_name": "xyz shop",
    #     "shop_type": "Manufacturers",
    #     "shop_address": "kolkata",
    # "udhyog_aadhar": "Yes",
    # "uan_number": "123456987",
        # "poa_type": "1",
        # "poa_number": "123456",
    # "bureau_score": "650",

    # "sm_score": "3",

    # "sm_loan_eligibility": 25000.00,
    doorNo = (doorNo if doorNo else "")
    street = (street if street else "")
    locality = (locality if locality else "")
    res_address = doorNo + street + locality


    dob_info = data['enrollmentDTO']['customer']['dateOfBirth']
    year, monthValue, dayofMonth = itemgetter('year', 'monthValue', 'dayOfMonth')(dob_info)
    date_of_birth = str(year)+'-'+str(monthValue)+'-'+str(dayofMonth)

    bank_accounts_info = data['enrollmentDTO']['customer']['customerBankAccounts']
    account_info = bank_accounts_info[0]
    customerBankName, ifscCode, accountType, accountNumber, bankStatements = itemgetter('customerBankName', 'ifscCode', 'accountType', "accountNumber", "bankStatements")(account_info)
    bank_statement_availability = ("Yes" if(len(bankStatements)>0) else "No")

    family_info = data['enrollmentDTO']['customer']['familyMembers']
    income_info = family_info[0]['incomes'][0]['incomeEarned']

    print(income_info)
    user_data = {
        "sm_user_id": sm_user_id,
        "name": full_name,
        "date_of_birth": date_of_birth,
        "gender": gender,
        "father_name": father_full_name,
        "marital_status": maritalStatus,
        "mobile_number": mobilePhone,
        "email_id": email,
        "res_address": res_address,
        "res_city": district,
        "res_state": state,
        "res_pin_code": pincode,
        "shop_name": "Not Found",
        "shop_type": "Not Found",
        "shop_address": "Not Found",
        "monthly_income": income_info,
        "udhyog_aadhar": "Not Found",
        "uan_number": "Not Found",
        "pan_number": panNo,
        "poa_type": "Not Found",
        "poa_number": "Not Found",
        "bank_name": customerBankName,
        "account_number": accountNumber,
        "ifsc_code": ifscCode,
        "account_type": accountType,
        "bureau_score": "Not Found",
        "sm_score": "Not Found",
        "sm_loan_eligibility": "Not Found",
        "bank_statement_availability": bank_statement_availability,
    }
    return user_data


async def create_loan_data(data):
    loan_info = data['loanDTO']['loanAccount']
    loanAmount, interestRate, disbursementSchedules, tenure, processingFeeInPaisa, insuranceFee = itemgetter('loanAmount', 'interestRate', 'disbursementSchedules', 'tenure', 'processingFeeInPaisa', 'insuranceFee')(loan_info)
    disbursement_amount = disbursementSchedules[0]['disbursementAmount']
    # "repayment_schedule_json":
    #     "am_user_token": "6facc090-3a98-412c-8d0b-66999449406c",
    # "sm_user_id": "SM000001250",
    # "sm_loan_id": "SML00258995"

    # "additional_charges": "250",
    # "number_of_edis": "5"
    print(loanAmount, interestRate, disbursement_amount, processingFeeInPaisa)
    response = {
        "loan_amount": loanAmount,
        "interest_rate": interestRate,
        "disbursement_amount": disbursement_amount,
        "tenure": tenure,
        "repayment_schedule_json":"Not Found",
        "am_user_token": "Not Found",
        "sm_user_id": "Not Found",
        "sm_loan_id": "Not Found",
        "processing_fee": processingFeeInPaisa,
        "additional_charges": "Not Found",
        "insurance_charges": insuranceFee,
        "number_of_edis": "Not Found"
    }

    return response

@app.post("/post_perdix_to_user_data")
async def post_perdix_to_user_data(
        payload: dict = Body(...)
):
    # user_request_url = f'http://apistaging.arthmate.com/spice/moneSDSapi/v1/user'
    # loan_request_url = f'http://apistaging.arthmate.com/spice/money/api/v1/loan/request'
    user_info = await create_user_data(payload)
    loan_info = await create_loan_data(payload)
    print(user_info)
    print(loan_info)
    try:
        # post_user_data = requests.post(user_request_url, user_info)
        # post_loan_data = requests.post(loan_request_url, loan_info)
        user_create_api = get_env('destination-end-points','user-create-url','')
        post_user_data = requests.post(user_create_api, user_info)
        # post_loan_data = requests.post(Settings.loan_create_api, loan_info)
    except Timeout as ex:
        print("Exeption Raised", ex)
    
    print(post_user_data)
    # print(post_loan_data)
    return {"output": "success"}
    

def test_read_main():
    response = client.get("/post_perdix_to_user_data")
    assert response.status_code == 200
    assert response.json() == {"msg": "Executing Successfully"}