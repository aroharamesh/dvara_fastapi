from commons import env, get_env, get_env_or_fail, _raise
from contextvars import ContextVar
import peewee

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())

class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]

def _connect_mysql(db_conf) -> peewee.MySQLDatabase:
	db_section = 'db-'+db_conf
	if env.has_section(db_section):
		h = get_env(db_section, 'host', 'localhost')
		p = int(get_env(db_section, 'port', '3306'))
		database = get_env(db_section, 'database', db_conf)
		usr = get_env_or_fail(db_section, 'username', f'Username not configured for {db_conf}')
		pwd = get_env_or_fail(db_section, 'password', f'Password not configured for {db_conf}')
		db = peewee.MySQLDatabase(database, user=usr, password=pwd, host=h, port=p)
		db._state = PeeweeConnectionState()
		return db
	_raise(f'{db_conf} not configured')

financialForms = _connect_mysql('financialForms')