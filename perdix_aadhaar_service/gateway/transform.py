from commons import get_env_or_fail
from datetime import datetime
from fastapi.exceptions import HTTPException
from yattag import Doc
import xml.etree.ElementTree as ET

def prepare_reqdata_xml(capture_xml):
	try:
		pid_data = ET.fromstring(capture_xml)
		data = pid_data.find('Data')
		device_info = pid_data.find('DeviceInfo')
		additional_info = device_info.find('additional_info')
		hmac = pid_data.find('Hmac')
		skey = pid_data.find('Skey')
		doc, tag, text = Doc().tagtext()

		with tag('ReqData'):
			with tag('TransactionReqInfo'):
				with tag('Channel'):
					text('MATM')
				with tag('IIN'):
					text(additional_info.find('Param[@name="srno"]').get('value')) # 508534
				with tag('TxnType'):
					text('bkyc')
				with tag('Local_Trans_Time'):
					text(datetime.now().strftime('%H%M%S'))
				with tag('Local_date'):
					text(datetime.now().strftime('%m%d'))
				with tag('Pan_entry_mode'):
					text('MN')
				with tag('Pos_code'):
					text('CPCN')
				with tag('CA_ID'):
					text(additional_info.find('Param[@name="sysid"]').get('value'))
				with tag('CA_TA'):
					text('IN')
			with tag('UidaiData'):
				with tag('Data', type=data.get('type')):
					text(data.text)
				with tag('Hmac'):
					text(hmac.text)
				with tag('Skey', ci=skey.get('ci')):
					text(skey.text)
		return doc.getvalue()
	except Exception as exc:
		raise HTTPException(status_code=500, detail=f"Failed to prepare request XML, {exc.args[0]}")

def prepare_mantra_xml(capture_xml, enc_reqdata_block, customer_aadhaar):
	try:
		pid_data = ET.fromstring(capture_xml)
		device_info = pid_data.find('DeviceInfo')
		doc, tag, text = Doc().tagtext()

		with tag('MAS_Request', de="N", lr="N", pfr="N", ra="F", rc="Y", tid="registered", ver="2.5"):
			with tag('UID'):
				text(customer_aadhaar)
			with tag('Terminal_Ip'):
				text(get_env_or_fail('app-mantra-server', 'terminal-ip', 'Terminal IP not configured'))
			with tag('ReqId'):
				text(datetime.now().strftime('%Y%m%d%H%M%S%f'))
			doc.stag('Uses', bio="y", bt="FMR", otp="n", pa="n", pfa="n", pi="n", pin="n")
			doc.stag('Meta',
				dc=device_info.get('dc'),
				dpId=device_info.get('dpId'),
				mc=device_info.get('mc'),
				mi=device_info.get('mi'),
				rdsId=device_info.get('rdsId'),
				rdsVer=device_info.get('rdsVer')
			)
			with tag('ReqData'):
				text(enc_reqdata_block)
		return doc.getvalue()
	except Exception as exc:
		raise HTTPException(status_code=500, detail=f"Failed to prepare request XML, {exc.args[0]}")
