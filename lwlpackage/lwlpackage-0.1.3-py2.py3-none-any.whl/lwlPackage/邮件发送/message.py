# coding:utf-8

# 这些库都是原生的，不用安装
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def sendMessage(file, receiver):

    # 服务器地址
    smtpserver = 'smtp.163.com'
    # 发送账号
    user = '17742566640@163.com'
    # 发送密码
    password = '18774370611'

    # 邮件标题
    subject = 'python自动发送验证短信'
  
    # 02. 添加图片
    file = open(file, "rb")
    img_data = file.read()
    file.close()
    img = MIMEImage(img_data)
    img.add_header('Content-ID', 'imageid')
    content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>','html','utf-8')

    message = MIMEMultipart()
    # 发送地址
    message['From'] = user
    # 接受地址
    message['To'] =  receiver
    # 邮件标题
    message['subject'] =subject
    # 正文内容
    message.attach(img)
    message.attach(content)


  
    smtp = smtplib.SMTP()
    # 连接服务器
    smtp.connect(smtpserver)
    # 登录邮箱账号
    smtp.login(user,password)
    # 发送账号信息
    smtp.sendmail(user,receiver,message.as_string())
    # 关闭
    smtp.quit()

if __name__ =="__main__":
    sendMessage('/home/lwl/Code/2020-07-06_01-20.png', '2892211452@qq.com')