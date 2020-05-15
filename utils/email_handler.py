# coding: utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config.ConfigManager import ConfigManager
class SendMail(object):
    config = ConfigManager()
    def __init__(self, title, content, file=None):
        self.username = self.config.yaml_setting['email']['username']
        self.passwd = self.config.yaml_setting['email']['passwd']
        self.recv = self.config.yaml_setting['email']['recv']
        self.email_host = self.config.yaml_setting['email']['email_host']
        self.port = self.config.yaml_setting['email']['port']
        self.title = title
        self.content = content
        self.file = file

    def send_mail(self):
        msg = MIMEMultipart()
        #发送内容的对象
        if self.file:#处理附件的
            att = MIMEText(open(self.file).read())
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"'%self.file
            msg.attach(att)
        msg.attach(MIMEText(self.content))#邮件正文的内容
        msg['Subject'] = self.title  # 邮件主题
        msg['From'] = self.username  # 发送者账号
        msg['To'] = ";".join(self.recv)  # 接收者账号列表
        self.smtp = smtplib.SMTP(self.email_host,port=self.port)
        #发送邮件服务器的对象
        self.smtp.login(self.username, self.passwd)
        try:
            self.smtp.sendmail(self.username, self.recv, msg.as_string())
        except Exception as e:
            logging.exception(e)
    def __del__(self):
        self.smtp.quit()

if __name__ == '__main__':
    # m = SendMail(
    #     title='服务器测试请勿回复',
    #     content='gather_taobao.ir_taobao_product_trade_china_2019',file='../spiders/detail.csv'
    # )
    # m.send_mail()
    logging.basicConfig()
    # config = ConfigManager()
    # print(config.yaml_setting['email']['recv'])
