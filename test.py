import smtplib

email_address='pythontester2900@gmail.com'
email_smtp='smtp.gmail.com'
email_app_password = ''


with smtplib.SMTP(email_smtp) as connection:
    connection.starttls()
    connection.login(user=email_app_password, password=email_app_password)
    connection.sendmail(from_addr=email_address, to_addrs='matemat547@yahoo.com',
                        msg='£')
