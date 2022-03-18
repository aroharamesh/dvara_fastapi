from fastapi import APIRouter
from data import model, schema

router = APIRouter(prefix = '/user')

@router.get('/{user_id}', response_model=schema.UserSchema)
async def get_user(user_id):
	return model.User.get(user_id = user_id)
