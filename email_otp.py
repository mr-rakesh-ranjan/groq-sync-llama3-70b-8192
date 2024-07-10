import random
import smtplib
import math

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
appPwd = os.getenv("APP_PWD")
# appPwd1 = os.getenv("APP_PWD1")
# print(appPwd)
# print(appPwd1)


def generate_otp():
    digits = "0123456789"
    OTP = ""
    
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP

def sendEmailVerificationRequest(receiver, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    sender = "rakesrcciit@gmail.com"
    server.login(sender, appPwd)
    curr_otp = generate_otp()
    # print(curr_otp)
    body = message + "\n\nYour OTP is: " + curr_otp
    subject = "Email verification Request"
    server.sendmail(sender, receiver, f"Subject: {subject}\n\n{body}")
    server.quit()
    return curr_otp

def sendEmailVerificationRequest_smtp2go(receiver, message):
    server = smtplib.SMTP('mail.smtp2go.com', 2525)
    server.starttls()
    sender = "sujit_s@pursuitsoftware.biz"
    server.login(sender, appPwd1)
    curr_otp = generate_otp()
    # print(curr_otp)
    body = message + "\n\nYour OTP is: " + curr_otp
    subject = "Email verification Request"
    server.sendmail(sender, receiver, f"Subject: {subject}\n\n{body}")
    server.quit()
    return curr_otp

