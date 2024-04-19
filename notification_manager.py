import smtplib
import flight_data
from twilio.rest import Client
import data_manager


class NotificationManager:
    """
    Class responsible for sending notifications to the user via email.
    """

    def __init__(self, email_address: str, email_smtp: str,
                 account_sid: str, account_token: str,
                 phone_number_from: str,
                 data_handler: data_manager.DataManager,
                 account_database: list) -> None:
        """
        Initialize data attributes foe NotificationManager.
        :param email_address: Email address of the sender.
        :param email_smtp: SMTP of the sender server.
        :param phone_number_from: Phone number that will send the
            `message`.
        :param data_handler: Instance of the DataManager class. It
            is responsible for getting account data for
            NotificationManager.
        :param account_database: List of all users returned from
            Google Sheets.

        """
        self.data_manager = data_handler
        self.email_address = email_address
        self.email_smtp = email_smtp
        self.account_sid = account_sid
        self.auth_token = account_token
        self.phone_number = phone_number_from
        self.account_database = account_database

    def send_email_notification(self, data_to_send: flight_data.FlightData,
                                password: str) -> None:
        """
        Send `message` to given `email_address`.
        :param data_to_send: Instance of FlightData object to generate
            message to send from.
        :param password: Password of sender e-mail.
        """
        if self.account_database:
            for account in self.account_database:
                email_address = account['email']
                name = f'{account["firstName"]} {account["lastName"]}'
                message = f'Subject: Low price alert!\n\n' \
                          f'Dear {name},\n' \
                          f'Only £{data_to_send.price} to fly from' \
                          f' {data_to_send.city_from}-{data_to_send.airport_from}' \
                          f' to {data_to_send.city_to}-{data_to_send.airport_to}, ' \
                          f'from {data_to_send.time_from} to {data_to_send.time_to}. '.encode('utf-8')

                with smtplib.SMTP(self.email_smtp) as connection:
                    connection.starttls()
                    connection.login(user=self.email_address, password=password)
                    connection.sendmail(from_addr=self.email_address,
                                        to_addrs=email_address,
                                        msg=message)

    def send_sms_notification(self,
                              data_to_send: flight_data.FlightData) -> None:
        """
        Send sms notification about cheap flight to all number from
        `account_database`.

        :param data_to_send: Instance of FlightData object to generate
            message to send from.

        """
        if self.account_database:
            for account in self.account_database:
                name = f'{account["firstName"]} {account["lastName"]}'
                phone_number = account['phoneNumber']

                client = Client(self.account_sid, self.auth_token)
                message = 'Low price alert!\n\n' \
                          f'Dear {name},\n' \
                          f'Only £ {data_to_send.price} to fly from' \
                          f' {data_to_send.city_from}-{data_to_send.airport_from}' \
                          f' to {data_to_send.city_to}-{data_to_send.airport_to}, ' \
                          f'from {data_to_send.time_from} to {data_to_send.time_to}. '.encode('utf-8')

                message_to_send = client.messages.create(body=message,
                                                         from_=self.phone_number,
                                                         to=phone_number)
                print(message_to_send.status)
