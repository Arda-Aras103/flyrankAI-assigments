import os
from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import create_client

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

app = FastAPI()

@app.on_event("startup")
def startup():
    print("Server running and connected to Supabase")
