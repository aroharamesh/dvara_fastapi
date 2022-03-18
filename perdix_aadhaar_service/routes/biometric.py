import json
from typing import Optional
from fastapi import APIRouter, Request, Header
from gateway import transform, icici
from service import crypto

router = APIRouter(prefix='/biometric')

@router.post('/validate')
async def validate(request: Request, authorization: Optional[str] = Header(None)):
	req_json = await request.json()
	raw_request = transform.device_to_adhaar_xml(req_json['fpCaptureXml'], req_json['aadhaarNumber'])
	(enc_key, enc_req, iv) = crypto.encrypt(raw_request)
	icici_request =  icici.prepare_request(enc_key, enc_req, iv, req_json['moduleReferenceId'])
	icici_response = icici.send_request(icici_request)
	raw_response = crypto.decrypt(icici_response['encryptedKey'], icici_response['encryptedData'])
	return {
		"response": json.loads(raw_response)
	}

@router.post('/request')
async def validate(request: Request, authorization: Optional[str] = Header(None)):
	req_json = await request.json()
	reqdata_xml = transform.prepare_reqdata_xml(req_json['fpCaptureXml'])
	enc_reqdata_block = crypto.encrypt_req_data_block(reqdata_xml)
	raw_request = transform.prepare_mantra_xml(req_json['fpCaptureXml'], enc_reqdata_block, req_json['aadhaarNumber'])
	(enc_key, enc_req, iv) = crypto.encrypt(raw_request)
	return  icici.prepare_request(enc_key, enc_req, iv, req_json['moduleReferenceId'])

@router.post('/response')
async def validate(request: Request, authorization: Optional[str] = Header(None)):
	req_json = await request.json()
	return {
		"response": crypto.decrypt(req_json['encryptedKey'], req_json['encryptedData'])
	}
