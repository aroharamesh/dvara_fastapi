from commons import get_env_or_fail
import requests

APP_PERDIX_SERVER = 'app-perdix-server'

def validate_token(auth_token: str) -> bool:
    account_url = get_env_or_fail(APP_PERDIX_SERVER, 'base-url', APP_PERDIX_SERVER+' base-url not configured')
    account_url += '/api/account'
    r = requests.get(account_url, headers={'authorization': auth_token})
    return r.status_code == requests.codes.ok
