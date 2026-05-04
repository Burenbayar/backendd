from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str | None = None

    class Config:
        from_attributes = True  # pydantic v2

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
