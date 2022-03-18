from pydantic import BaseModel

class OpenAPISchema(BaseModel):
	class Config:
		orm_mode = True

class UserSchema(OpenAPISchema):
	id: int
	user_id: str
	user_name: str
	email_address: str
