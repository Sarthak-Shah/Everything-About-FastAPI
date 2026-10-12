"""
jwt = JSON Web token.
- Client (browser), gets the token after inserting usernam and password for authentication.
- In token, Header and Payload are encoded and signed with a secret key.

jwt is a third party library that is used to generate and verify JSON Web Tokens (JWTs). 
It is commonly used for authentication and authorization in web applications. 
The library provides functions to encode and decode JWTs, as well as to verify their signatures.
jose = javascript object signing and encryption.
"""
#Uvicorn currently supports HTTP/1.1, HTTP/2 and WebSockets.

from fastapi import FastAPI, Depends, HTTPException, Header
from jose import jwt
from datetime import datetime, timedelta, timezone
import uvicorn

app = FastAPI()

SECRET_KEY = "MY SECRET KEY - CILLIAN MURPHY"
ALGORITHM = "HS256" # RS256, HS256, ES256

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)  # Token expires in 30 minutes
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

#Login API Endpoint For Token Generation
@app.post("/login")
def login(username: str, password: str):
    # In a real app, you would verify the username and password here
    if username != "admin" or password != "password":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:   
        token_data = {"sub": username}
        token = create_token(token_data)
        return {"access_token": token}

#Token Verification
def verify_token(token: str = Header(None)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        return payload
    except:
        raise HTTPException(
            status_code = 401,
            detail="Invalid or expired Token"
        )

# Protected API Endpoint
@app.get("/secure")
def secure_endpoint(user = Depends(verify_token)):
    return {"message": "This is a secure endpoint"}