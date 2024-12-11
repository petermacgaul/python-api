from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class JWTtoken(BaseModel):
    access_token: str
