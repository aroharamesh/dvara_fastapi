from fastapi import FastAPI, Body
import requests
from requests.exceptions import Timeout
from logging.config import dictConfig
import logging
from logger.config import LogConfig

from commons import env, get_env, get_env_or_fail, _raise
from helpers.functions import create_user_data, create_loan_data

app = FastAPI()

dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")

@app.post("/process-perdix-data")
async def post_perdix_to_user_data(
        payload: dict = Body(...)
):
    user_info = await create_user_data(payload)
    loan_info = await create_loan_data(payload)
    print(user_info)
    print(loan_info)
    try:
        user_create_api = get_env('destination-end-points','user-create-url','')
        loan_create_api = get_env('destination-end-points','loan-request-url','')
        post_user_data = requests.post(user_create_api, user_info)
        post_loan_data = requests.post(loan_create_api, loan_info)
    except Timeout as ex:
        print("Exeption Raised", ex)
    
    logger.info("Dummy Info")
    logger.error("Dummy Error")
    logger.debug("Dummy Debug")
    logger.warning("Dummy Warning")

    logger.info(post_user_data)
    # print(post_user_data)
    # print(post_loan_data)
    return {"output": "success"}
