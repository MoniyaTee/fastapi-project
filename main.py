
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import time
import logging

app = FastAPI()

# CORS middleware to allow only http://localhost:8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logger middleware to log request time
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f"Request completed in {process_time:.4f} seconds")
    return response

# In-memory storage
users: List[Dict] = []

# Pydantic model for the user
class User(BaseModel):
    first_name: str = Field(..., example="Jane")
    last_name: str = Field(..., example="Doe")
    age: int = Field(..., gt=0, example=30)
    # email: EmailStr = Field(..., example="jane.doe@example.com")
    height: float = Field(..., gt=0, example=5.5)
    notes: str = Field(None, example="Likes reading and hiking")

# Endpoint to create a user
@app.post("/users", status_code=201)
async def create_user(user: User):
    user_data = user.dict()
    users.append(user_data)
    return {"message": "User created successfully", "user": user_data}
