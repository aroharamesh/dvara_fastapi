
from pydantic import BaseSettings


class Settings(BaseSettings):
    user_url: str
    loan_url: str
    repayment_url: str
    user_document_upload_url: str
    loan_document_upload_url: str
    disbursement_status_url: str
    file_stream_url: str
    username: str
    password: str

    class Config:
        env_file = "arthmate_lender_handoff_service/.env"
        env_file_encoding = 'utf-8'

