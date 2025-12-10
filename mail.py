## 邮箱有问题，时好时坏，需要使用时再研究

import time
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig

from config import config


router = APIRouter()


# 邮件配置
yahoo_mail_config = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_FROM,
    MAIL_SERVER="smtp.qq.com",  # smtp.mail.yahoo.com
    MAIL_PORT=465,  # 常用465、587
    MAIL_SSL_TLS=True,  # 465开启
    MAIL_STARTTLS=False,  # 587开启
    USE_CREDENTIALS=False,  # 是否需要验证，通常为True
    VALIDATE_CERTS=False,  # 证书是否需要验证（测试环境有问题，但生产时开启没问题）
)


class Email(BaseModel):
    addresses: list[EmailStr]  # 类型为list，方便同时给多个地址发邮件，数据校验是否符合EmailStr格式
    

@router.post('/send_email')
async def send_email(email: Email):
    start_time = time.time()

    # 邮件正文
    body_html = '''
    <h1>ok</h1>
    <p>p</p>
    '''
    message = MessageSchema(
        subject="fastapi邮件",  # 邮件主题
        recipients=email.addresses,  # 收件人(此处采用常量)。写死的话就["510702433@qq.com"]
        body=body_html,  # 邮件正文
        subtype=MessageType.html,
    )

    fm = FastMail(yahoo_mail_config)
    await fm.send_message(message)

    return {
        'address': email.addresses,
        '发送邮件所需时间': time.time()-start_time,
    }
