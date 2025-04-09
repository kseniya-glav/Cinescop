from pydantic import BaseModel, Field, field_validator
from typing import Optional
from constants.roles import Roles 
import datetime

class BaseUser(BaseModel):
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None
    
    @field_validator("email")
    def check_email(cls, value):
        if "@" not in value:
            raise ValueError("Нет символа @")
        return value
    

class User(BaseUser):
    id: str

class UserRegistr(BaseUser):
    password: str = Field(min_length=8)
    passwordRepeat: str = Field(description="Пароли должны совпадать")
    
    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value, info):
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value
    
class UserRegistrResponse(User):
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")
       
    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value

class UserLoginResponse(BaseModel):
    user: User
    accessToken: str = Field(description="Токен доступа")
    refreshToken: str = Field(description="Токен обновления")
    expiresIn: int = Field(description="Время жизни токена (сек)")
    