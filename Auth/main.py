import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from auth_service import AuthService

load_dotenv()


class Credentials(BaseModel):
    email: str | None = None
    password: str | None = None


app = FastAPI()
auth = AuthService()


@app.on_event("startup")
def startup():
    print("Server running and connected to Supabase")


@app.post("/auth/signup", status_code=201)
def sign_up(credentials: Credentials):
    if not credentials.email or not credentials.password:
        return JSONResponse(status_code=400, content={"error": "Bad Request"})
    try:
        result = auth.sign_up(credentials.email, credentials.password)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    return result.user.model_dump() if result.user else {}

@app.post("/auth/login",status_code=200)
def log_in(credentials:Credentials):
    if not credentials.email or not credentials.password:
        return JSONResponse(status_code=400, content={"error": "Bad Request"})
    try:
        result = auth.sign_in(credentials.email, credentials.password)
    except Exception:
        return JSONResponse(status_code=401, content={"error": "Invalid login credentials"})
    if result.session is None:
        return JSONResponse(status_code=401, content={"error": "Invalid login credentials"})
    return {
        "access_token": result.session.access_token,
        "refresh_token": result.session.refresh_token,
    }
