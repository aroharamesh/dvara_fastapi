from commons import get_env_or_fail
import requests

def prepare_request(enc_key, enc_data, iv, module_ref):
    return {
        "requestId": module_ref,
        "service": "AccountCreation",
        "encryptedKey": enc_key,
        "oaepHashingAlgorithm": "NONE",
        # "iv": iv,
        "encryptedData": enc_data,
        "clientInfo": "",
        "optionalParam": ""
    }

APP_ICICI_SERVER = 'app-icici-server'

def send_request(request):
    validate_url = get_env_or_fail(APP_ICICI_SERVER, 'validate-url', APP_ICICI_SERVER+' base-url not configured')
    api_key = get_env_or_fail(APP_ICICI_SERVER, 'api-key', APP_ICICI_SERVER+' api-key not configured')
    r = requests.post(validate_url, request, headers={'Content-Type': 'application/json', 'ApiKey': api_key})
    return r.json()