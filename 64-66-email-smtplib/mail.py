import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class mailSender(object):
    def __init__(
        self,
        username,
        password,
        smtp_server,
        smtp_port,
    ):
        self._username = username
        self._password = password
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port

    def connect(self, debug=0, timeout=10):
        """initialize connect to smtp server"""

        smtp_server = smtplib.SMTP_SSL(
            self._smtp_server, self._smtp_port, timeout=timeout
        )

        smtp_server.set_debuglevel(debug)
        return smtp_server

    def send(self, from_addr, to_addr, bcc, subject, body):
        """send email"""

        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["To"] = to_addr
        msg["Subject"] = subject
        msg_body = body
        msg.attach(MIMEText(msg_body, "plain"))
        text = msg.as_string()
        smtp_server = self.connect()
        smtp_server.login(self._username, self._password)
        smtp_server.sendmail(from_addr, [to_addr] + bcc, text)
        smtp_server.quit()
