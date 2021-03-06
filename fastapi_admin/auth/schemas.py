# -*- encoding: utf-8 -*-
"""
@File    : schemas.py
@Time    : 2020/4/5 11:00
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :权限先关的schema
"""
from pydantic import BaseModel, validator, Field


class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    is_active: bool
    is_superuser: bool


class UserDB(UserSchema):
    pass


from pydantic import EmailStr


class UserInDb(UserDB):
    email: EmailStr


class TokenData(BaseModel):
    username: str = None


class Token(BaseModel):
    access_token: str
    token_type: str


def is_ascii(s):
    return all((ord(c) < 128 or ord(c) == 95) for c in s)


def is_enable_passowrd(s):
    return all((ord(c) < 128 and (ord(c) != 33 and ord(c) != 42 and ord(c) != 37)) for c in s)


class RegisterUser(BaseModel):
    """注册用"""
    username: str = Field(..., description="账户")
    password: str = Field(..., description="密码")
    nick_name: str = Field(..., description="昵称")
    email: EmailStr = Field(..., description="邮箱")
    qq: str = Field(None, description="qq号")
    phone_number: str = Field(None, description="手机号", max_length=11, min_length=11)

    @validator('username')
    def username_match(cls, v, values, **kwargs):
        if not is_ascii(v):
            raise ValueError('账户不能有特殊符号')
        if len(v) < 4:
            raise ValueError('账户太短')
        return v

    @validator('password')
    def password_match(cls, v, values, **kwargs):
        if not is_enable_passowrd(v):
            raise ValueError('密码不能有特殊符号')
        if len(v) < 8:
            raise ValueError("密码长度不能少于8")
        return v


class ModifyPassword(BaseModel):
    id: int
    new_password: str


class ModifyBaseInfo(BaseModel):
    id: int
    qq: str
    email: EmailStr
    nick_name: str


class ForbbidenAccount(BaseModel):
    id: int  # 禁用账户
    is_active: bool


class DeleteAccount(BaseModel):
    id: int  # 删除账户
    # is_delete:bool=False
