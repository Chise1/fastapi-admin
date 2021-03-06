# -*- encoding: utf-8 -*-
"""
@File    : models.py
@Time    : 2020/4/4 15:31
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :创建基本需要的models
"""
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Table, DateTime, DECIMAL, UniqueConstraint, func, \
    text
from datetime import datetime

__all__ = ['User', 'Group', 'Permission']
Base = declarative_base()


class User(Base):
    __tablename__ = 'fastapi_auth_user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, comment="用户名",nullable=False)
    password = Column(String(128), comment="密码",nullable=False)
    guid = Column(String(16), comment="系统生成，不可重复，证书", unique=True,nullable=False)
    nick_name = Column(String(64), comment="昵称", nullable=False,unique=True)
    qq = Column(String(16), comment="qq")
    email = Column(String(64), nullable=True, unique=True,comment="邮箱")
    phone_number = Column(String(18), nullable=True, unique=True, comment="手机号")
    register_ip = Column(String(32), comment="注册ip")
    register_time = Column(DateTime, comment="注册时间", server_default=func.now())
    level_id = Column(Integer, comment="会员等级？", server_default='0')
    status = Column(Integer, comment="状态", server_default='0')
    is_superuser = Column(Boolean, server_default=text('false'), comment="是否为超级管理员")
    is_active = Column(Boolean, server_default=text('true'), comment="是否刻可登录")
    is_delete=Column(Boolean, server_default=text('false'), comment="是否删除")
    def __str__(self):
        return self.username


class UserLog(Base):
    """用户日志"""
    __tablename__ = "fastapi_auth_userlog"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("fastapi_auth_user.id"), comment="用户ID")
    user = relationship("User", backref="userLogs", )
    operate_status = Column(Integer, comment="操作类型：(0密码修改，1资料编辑，2登陆，3注册)", server_default='0')
    operate_detial = Column(String(128), comment="操作详情")
    operate_ip = Column(String(16), comment="操作ip")
    operate_time = Column(DateTime, comment="操作时间", default=func.now())
    operate_result = Column(Boolean, comment="操作成功还是失败登陆失败这种状态就可以当作失败", )


auth_user_group = Table(  # 多对多的第三方表，居然还要自己生成。。
    'fastapi_auth_user_group',
    Base.metadata,
    Column("user_id", Integer, ForeignKey("fastapi_auth_user.id")),
    Column("group_id", Integer, ForeignKey("fastapi_auth_group.id")),
UniqueConstraint('user_id', 'group_id', name='idx_user_id_group_id'),
)


class Group(Base):
    __tablename__ = 'fastapi_auth_group'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, index=True, comment="组名")
    users = relationship("User", backref="groups", secondary=auth_user_group)

    def __str__(self):
        return self.name


auth_group_permission = Table(  # 多对多的第三方表，居然还要自己生成。。
    'fastapi_auth_group_permission',
    Base.metadata,
    Column("group_id", Integer, ForeignKey("fastapi_auth_group.id")),
    Column("permission_id", Integer, ForeignKey("fastapi_auth_permission.id")),
    UniqueConstraint('group_id', 'permission_id', name='idx_group_id_permission_id'),
)


class Permission(Base):
    __tablename__ = 'fastapi_auth_permission'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, index=True, comment="权限名称")  # 权限名称
    codename = Column(String(100), unique=True, index=True, comment="权限字段")  # 权限字段
    groups = relationship("Group", backref="permissions", secondary=auth_group_permission)

    def __str__(self):
        return self.name
