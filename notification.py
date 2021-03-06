# Some default variables
DEFAULT_TO_NAME = 'You'
DEFAULT_TO_ADDR = 'rufiw@stromox.com'


class Email:
    def __init__(self, from_name='', from_addr='', to_name='', to_addr='', subject='', body=''):
        self._from_name = from_name
        self._from_addr = from_addr

        self._to_name = to_name
        self._to_addr = to_addr

        self._subject = subject
        self._body = body

    def send(self):
        # Import the needed packages
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        import smtplib

        # Setup the message
        msg = MIMEMultipart()
        msg['From'] = self.from_addr
        msg['To'] = self.to_addr

        # Attach the subject and body
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.body))

        # Make a secure connection with the mailserver
        server = smtplib.SMTP('smtp.utwente.nl')
        # server.starttls()

        # Login onto the mailserver
        # server.login('', '')

        text = msg.as_string()

        # Send the mail and close the connection
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

# Some default templates
DEFAULT_TAKE_MEDS = Email('Drug Dispensr', 'drugs@dispen.sr',
                          DEFAULT_TO_NAME, DEFAULT_TO_ADDR,
                          'Take your meds now',
                          'Do it now!')

DEFAULT_FILL_NOW = Email('Drug Dispensr', 'drugs@dispen.sr',
                         DEFAULT_TO_NAME, DEFAULT_TO_ADDR,
                         'Refill the dispenser',
                         'Do it now!')


def send_refill():
    """
    Sends an email to the default refiller saying that he or she has to
    refill the Drug Dispenser
    """
    DEFAULT_FILL_NOW.send()


def send_take_med():
    """
    Sends an email to some email-adress that he or she has to take his
    or her medication immediately.

    NOTE: Currently not implemented
    """
    DEFAULT_TAKE_MEDS.send()
