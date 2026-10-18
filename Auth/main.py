import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request, Response, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from auth_service import AuthService

load_dotenv()


class Credentials(BaseModel):
    email: str | None = None
    password: str | None = None


bearer_scheme = HTTPBearer(auto_error=False)
auth = AuthService()


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme)):
    if credentials is None or not credentials.credentials.strip():
        raise HTTPException(status_code=401, detail="Access token required")

    token = credentials.credentials.strip()
    try:
        result = auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = getattr(result, "user", None) if result else None
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user, token


app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


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


@app.post("/auth/login", status_code=200)
def log_in(credentials: Credentials):
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


@app.post("/auth/logout", status_code=204)
def log_out(auth_data=Depends(get_current_user)):
    auth.sign_out()
    return Response(status_code=204)


@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile")
def protected_profile(auth_data=Depends(get_current_user)):
    user, _ = auth_data
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
    }


@app.get("/protected/dashboard")
def protected_dashboard(auth_data=Depends(get_current_user)):
    user, _ = auth_data
    return {"message": "Welcome to your dashboard", "email": user.email}
