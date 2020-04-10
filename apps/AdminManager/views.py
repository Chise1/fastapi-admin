# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/4/10 13:38
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :后台管理使用的view
"""
from fastapi import APIRouter, Depends
from sqlalchemy import select

from fastapi_admin import AdminDatabase
from fastapi_admin.auth.schemas import ModifyPassword, ModifyBaseInfo
from fastapi_admin.publicDepends.paging_query import page_base_query
from fastapi_admin.views.methods_patch import model_patch_func
from .models import AccountBook
from .schemas import UserListModel
from fastapi_admin.auth.depends import create_current_active_user, get_current_active_user, get_password_hash
from fastapi_admin.auth.models import User

router = APIRouter()
# 展示数据
user_list = page_base_query(model=User, default_query=select([User, AccountBook.money, AccountBook.rate]).where(
    AccountBook.user_id == User.id),need_user=True)
# 修改数据
user_update, update_schema = model_patch_func(User, "UserUpdateInfo", fields=['nick_name', 'qq', 'email'])


# 修改密码
# user_modify_password,modify_password_schema=model_patch_func(User,"UserModifyPassword",fields=['password'])

async def modify_password(new_password: ModifyPassword, current_user: User = Depends(create_current_active_user(True))):
    """
    修改密码
    :param current_user:
    :return:
    """
    hash_password = get_password_hash(new_password.new_password)
    query = User.__table__.update().values({"password": hash_password}).where(User.id == current_user.id)
    print(query)
    res=await AdminDatabase().database.execute(query)
    print(res)
    return {"code": 200, "message": "success"}


async def modify_base_info(new_info: ModifyBaseInfo, current_user: User = Depends(create_current_active_user(True))):
    """
    修改密码
    :param current_user:
    :return:
    """
    query = User.__table__.update().values(dict(new_info)).where(User.id == current_user.id)
    await AdminDatabase().database.execute(query)
    return new_info


router.get('/user/list',tags=['user'], response_model=UserListModel, summary="获取用户列表")(user_list)
router.patch('/user/updateInfo',tags=['user'], response_model=ModifyBaseInfo, summary="更新个人数据")(modify_base_info)
router.patch('/user/modifyPassword',tags=['user'], description="修改密码",summary="修改个人密码")(modify_password)