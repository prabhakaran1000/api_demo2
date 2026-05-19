from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

API_KEY = "ABC123"

@app.middleware("http")
async def log_requests(request, call_next):
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        return JSONResponse(status_code=401, content={"message": "not authorized"})
    return await call_next(request)

@app.get("/welcome")
def welcome():
    return {"message": "Welcome to my FastAPI application!"}

@app.get("/user")
def get_user():
    return {"name": "John", 
            "age": 30, 
            "email": "john@example.com"
            }

@app.get("/user/{user_id}")
def user_profile(user_id: int):
    if user_id == 1:
        return {"user_id": user_id, 
                "name": "Alice", 
                "age": 28
        }                                                                                       
    else:
        return {"user_id": user_id, 
                "name": f"User{user_id}", 
                "age": 25 + user_id, 
        }
    
class User(BaseModel):
    name: str
    age: int
    email: str

Users = []

@app.post("/users")
def create_user(user: User):
    Users.append(user.dict())
    return {"message": "User created successfully", "total_users": len(Users)}
