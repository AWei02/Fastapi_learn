from tortoise import fields  # 用于声明数据库字段
from tortoise.models import Model  # 用于继承数据库模型


class Account(Model):
    id = fields.IntField(primary_key=True, generated=True)  # 主键
    username = fields.CharField(null=False,
                                unique=True,
                                max_length=32,
                                description="用户名")  # 非空，唯一，最大长度，描述
    hashed_password = fields.CharField(null=False,
                                       max_length=128,
                                       description="加密的密码")
    create_time = fields.DatetimeField(auto_now_add=True,
                                       description="创建时间")  # 数据添加时间
    update_time = fields.DatetimeField(auto_now=True,
                                       description="更新时间")  # 数据更新时间

    class Meta:
        # 数据库表配置信息
        table_description = "Account账户信息表"
        table = "account"
