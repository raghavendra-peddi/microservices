from pydantic import BaseModel, EmailStr, field_validator


class CustomerLogin(BaseModel):
    email: EmailStr
    password: str
