import mail
import os

PASSWORD = os.getenv.get("YANDEX_MAIL_TOKEN")
USERNAME = os.getenv.get("YANDEX_MAIL_USERNAME")
from_addr = USERNAME
to_addr = "admin@gmail.com"
bcc = ["user1@yandex.ru", "user2@yandex.ru"]
body = "Hello world!"
subject = "Test message"

if __name__ == "__main__":

    email = mail.mailSender(
        username=USERNAME,
        password=PASSWORD,
        smtp_server="smtp.yandex.ru",
        smtp_port=465,
    )
    email.connect()
    email.send(from_addr, to_addr, bcc, subject, body)
    print("Success!")
