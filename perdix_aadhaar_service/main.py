import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from routes import biometric, user
from gateway import perdix_server

app = FastAPI()

@app.middleware("http")
async def validate_token(request: Request, call_next):
	if 'authorization' in request.headers:
		if not perdix_server.validate_token(request.headers['authorization']):
			raise HTTPException(status_code=401, detail='Authorization failed')
	else:
		raise HTTPException(status_code=403, detail='No authorization header present')
	return await call_next(request)

@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
	return JSONResponse(status_code=exc.status_code if hasattr(exc, 'status_code') else 500, content={ "error": exc.detail if hasattr(exc, 'detail') else exc.args })

app.include_router(biometric.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)