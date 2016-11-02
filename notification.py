DEFAULT_TO_NAME = 'Joffrey The Drug Meistahr'
DEFAULT_TO_ADDR = 'jeffrey.bakker@gmail.com'


class Email:
    def __init__(self, from_name='', from_addr='', to_name='', to_addr=DEFAULT_TO_ADDR, subject='', body=''):
        self._from_name = from_name
        self._from_addr = from_addr

        self._to_name = to_name
        self._to_addr = to_addr

        self._subject = subject
        self._body = body

    def send(self):
        from email.mime.text import MIMEText
        import smtplib

        msg = MIMEText(self.body)
        msg['From'] = self.from_name
        msg['To'] = self.to_name
        msg['Subject'] = self.subject

        server = smtplib.SMTP('mail.jbakker.co')
        server.starttls()

        server.login('drug.dispensr@jbakker.co', 'dispensr')

        text = msg.as_string()
        server.sendmail(self.from_addr, self.to_addr, text)
        server.quit()

    @property
    def from_name(self):
        return self._from_name

    @from_name.setter
    def from_name(self, value):
        self._from_name = value

    @property
    def from_addr(self):
        return self._from_addr

    @from_addr.setter
    def from_addr(self, value):
        self._from_addr = value

    @property
    def to_name(self):
        return self._to_name

    @to_name.setter
    def to_name(self, value):
        self._to_name = value

    @property
    def to_addr(self):
        return self._to_addr

    @to_addr.setter
    def to_addr(self, value):
        self._to_addr = value

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        self._subject = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

DEFAULT_TAKE_MEDS = Email('Drug Dispensr', 'drug.dispensr@jbakker.co', DEFAULT_TO_NAME, DEFAULT_TO_ADDR,
                          'Take your fucking meds now!',
                          'Do it now!')

DEFAULT_FILL_NOW = Email('Drug Dispensr', 'drug.dispensr@jbakker.co', DEFAULT_TO_NAME, DEFAULT_TO_ADDR,
                         'Take your fucking meds now!',
                         'Do it now!')


def send_refill():
    DEFAULT_FILL_NOW.send()


def send_take_med():
    DEFAULT_TAKE_MEDS.send()