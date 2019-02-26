import logging

import time
import atexit
import crayons
import functools
from itertools import chain, islice

# Email Handler
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class EmailHandler:

    def __init__(self, address='', password='', server='smtp.gmail.com:587'):
        """
        :param address: String --   Email Address to use as sender (localhost can be used if enabled)
        :param password: String --  Email Address Password
        :param server: String --    Server Type

        Creates An EmailHandler Instance capable of handling Mail notifications
        """

        self.logger = logging.getLogger(__name__)

        self.address = address
        self.msg = MIMEMultipart()

        try:
            # Server Connection
            self.server = smtplib.SMTP(server)

            if self.server != 'localhost':
                self.server.ehlo()  # Start Connection
                self.server.starttls()  # Secure Connection
                self.server.login(address, password)

            # Closing SMTP Connection at script exit
            atexit.register(lambda: self.server.quit())

        except smtplib.SMTPAuthenticationError as e:
            self.logger.critical('Authentication Error: {}'.format(e))

        except Exception as e:
            self.logger.error('Unknown Error: {}'.format(e))

    def __radd__(self, attachment):
        self.addAttachments(attachment)

    def prepareImage(self, path):
        """
        :param path: String -- Saved image complete path
        :return: Image File ready to include in email body
        """
        name = path.split('/')[-1]

        # Add HTML Tag for image
        self.msg.attach(MIMEText('<img src="cid:{}">'.format(name), 'html'))

        with open(path, 'rb') as file:
            file = MIMEImage(file.read(), 'png')
            file.add_header('Content-ID', '<{}>'.format(name))
            return file

    def addAttachments(self, attachments):
        """
        :param attachments: List(Dict(attachment_type: attachment)

        Available attachement and object type:
            image: path to saved png image
            dataframe: pandas dataframe
        """

        for attachment in attachments:
            if attachment.get('image'):
                self.msg.attach(self.prepareImage(attachment.get('image')))

            elif attachment.get('dataframe') is not None:
                file = attachment.get('dataframe').to_html()
                self.msg.attach(MIMEText(file, 'html'))

            else:
                self.logger.error('{} is not yet supported as an attachment'.format(list(attachment.keys())[0]))

    def sendMessage(self, to, subject='', message=''):
        """
        :param to: List(String) | String -- Receivers Email addresses
        :param subject: String --           Email Subject
        :param message: String --           Body message of email

        Send the Email and reinitialize the msg object
        """

        if not isinstance(to, list): to = [to]

        try:

            self.msg['To'] = ','.join(to)
            self.msg['Subject'] = subject
            self.msg['From'] = self.address
            self.msg.attach(MIMEText(message, 'plain'))

            self.msg.attach(MIMEText(message))

            self.server.send_message(self.msg)
            self.msg = MIMEMultipart()

        except Exception as e:
            self.logger.critical('SendMessage Failed with error message: {}'.format(e))


def batch(iterable, size):
    """
    :param iterable: Iterable (list, dict, sets, tuples)
    :param size: Size of batch. The size of the iterable to iterate over
    :return: Iterable object

    Use batch function to return an iterable of length 'size' until the 'iterable' is empty
    """
    source_iter = iter(iterable)
    while True:
        batchiter = islice(source_iter, size)
        yield chain([batchiter.__next__()], batchiter)


def time_func(_func=None, *, runs=3):
    """https://realpython.com/primer-on-python-decorators/"""

    if runs < 1:
        raise ValueError('runs should be higher than 0 not {}'.format(runs))

    def decorator(func):

        @functools.wraps(func)
        def inner(*args, **kwargs):

            value = None
            start = time.perf_counter()

            for _ in range(runs):
                value = func(*args, **kwargs)

            end = time.perf_counter()
            run_time = (end - start) / (_ + 1)
            print(crayons.red('{} took {:.4f} secs on an average of {} runs'.format(func.__name__, run_time, runs), bold=True))
            return value

        return inner

    if _func is None:
        return decorator
    return decorator(_func)


@time_func(runs=10)
def test():
    for i in range(100000):
        print(i)


if __name__ == '__main__':
    test()

