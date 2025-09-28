from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from passlib.hash import bcrypt
from dotenv import load_dotenv
import os

router = APIRouter(prefix="/auth", tags=['auth'])
load_dotenv()

# Pydantic model for user input
class UserIn(BaseModel):
    email: EmailStr
    password: str

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['AIplanner']
user_collection = db["users"]
print(f"connected")

# Signup route
@router.post('/signup')
def signup(user:UserIn):
    existing_user = user_collection.find_one({"email":user.email})
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registred")
    
    hashed_password = bcrypt.hash(user.password)
    user_collection.insert_one({
        "email":user.email,
        "password":hashed_password
    })
    return {'message':"User Created Successfully"}

# Login route
@router.post("/login")
def login(user: UserIn):
    existing_user = user_collection.find_one({"email":user.email})
    if not existing_user:
        raise HTTPException(status_code=400, detail='Invlid Credentilas')
    
    
    if not bcrypt.verify(user.password, existing_user['password']):
        raise HTTPException(status_code=400, detail='Invalid credentials')
    
    return {"message":"Login Successful"}