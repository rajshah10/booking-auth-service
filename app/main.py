from fastapi import HTTPException, status
from fastapi import Depends
from fastapi import FastAPI
from pydantic import BaseModel
from app.database import engine , SessionLocal
from sqlalchemy.orm import Session
from app.models import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app=FastAPI()

# A Pydantic model describes what data our API expects.Converts Request into JSON format
class LoginRequest(BaseModel):
    email:str
    password:str

# The @app.get("/") decorator is a "path operation decorator".
# It tells FastAPI that the function right below it is in charge of handling requests that:
# 1. Use the HTTP GET method (used to read data).
# 2. Go to the path "/" (the root URL of the API).
@app.get("/")
def root():
    return{
        "message":"Booking Auth Service is running"
    }

# ==============================================================================
# FastAPI vs Django Comparison
# ==============================================================================
# | Feature              | FastAPI                          | Django                               |
# |----------------------|----------------------------------|--------------------------------------|
# | Primary Use Case     | Modern APIs, Microservices       | Full-stack web apps (HTML/CSS/JS)    |
# | Performance          | Extremely fast (Node/Go levels)  | Slower (synchronous by default)      |
# | Architecture         | Minimalist (bring your own tools)| "Batteries included" (built-in ORM)  |
# | Data Validation      | Built-in via Pydantic            | Handled via Django Forms/Serializers |
# | Async Support        | Native and built-in (async/await)| Added later, not fully native yet    |
# | Auto Documentation   | Yes (Swagger UI, ReDoc built-in) | No (Requires third-party packages)   |
# | Learning Curve       | Low (easy to start)              | Moderate to High                     |
# ==============================================================================

@app.get("/health/db")
def database_health():
   try:
    with engine.connect():
        return {"database": "connected"}
   except Exception as e:
        return {"database": "disconnected"}

@app.get('/users/{email}')
def get_user(email:str,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{email}' not found"
        )
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
    }


@app.post("/login")
def login(request:LoginRequest):
    return {
        "message": "Login request received by Auth Service"
    }