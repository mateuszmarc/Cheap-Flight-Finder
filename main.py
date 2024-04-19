import datetime
import data_manager
import flight_finder
import dotenv
import os
import notification_manager
import account_manager
import flight_club_front_desk

dotenv.load_dotenv('.env.txt')

SHEETY_API_FLIGHTS = os.getenv('sheety_api_end_arkusz1')
SHEETY_API_FLIGHTS_SHEET = os.getenv('sheety_api_sheet_name_arkusz')
FLIGHTS_SHEETY_AUTH_CODE = os.getenv('flight_authentication_code')


SHEETY_API_USERS = os.getenv('sheety_api_end_users')
SHEETY_API_USERS_SHEET = os.getenv('sheety_api_sheet_name')
USERS_SHEETY_AUTH_CODE = os.getenv('authentication_code')

KIWI_API_END = os.getenv('kiwi_api_end')
KIWI_API_KEY = os.getenv('kiwi_api_key')
EMAIL_ADDRESS = os.getenv('email_address')
EMAIL_SMTP = os.getenv('email_smtp')
EMAIL_APP_PASS = os.getenv('email_app_password')
TWILIO_MY_SID = os.getenv('my_sid')
TWILIO_MY_TOKEN = os.getenv('my_token')
MY_PHONE_NUMBER = os.getenv('my_phone_number')


today_date = datetime.datetime.now(datetime.timezone.utc).date()
date_delta = datetime.timedelta(days=180)
date_to = today_date + date_delta
formatted_current_date = datetime.datetime.strftime(today_date, '%d/%m/%Y')
formatted_date_to = datetime.datetime.strftime(date_to, '%d/%m/%Y')

front_desk = flight_club_front_desk.FrontDesk()
data_manager = data_manager.DataManager(front_desk)
account_database = data_manager.get_data(api_endpoint=SHEETY_API_USERS,
                                         sheet_name=SHEETY_API_USERS_SHEET,
                                         authentication_code=USERS_SHEETY_AUTH_CODE)
print(account_database)
flight_finder = flight_finder.FlightFinder(KIWI_API_END, KIWI_API_KEY)
notification_manager = notification_manager.NotificationManager(
    email_address=EMAIL_ADDRESS,
    email_smtp=EMAIL_SMTP,
    account_sid=TWILIO_MY_SID,
    account_token=TWILIO_MY_TOKEN,
    phone_number_from=MY_PHONE_NUMBER,
    data_handler=data_manager,
    account_database=account_database,
)

account_manager = account_manager.AccountManager()

while True:
    activity = front_desk.get_user_need()
    if activity == 'check':
        break
    data_to_write = account_manager.get_data()

    # check if data to write exists in the Google Sheets Data.
    checked_data = data_manager.check_account(account_data=data_to_write,
                                              account_list=account_database)
    if activity == 'open':
        if not checked_data[0]:
            data_manager.add_data(api_endpoint=SHEETY_API_USERS,
                                  new_data=data_to_write,
                                  sheet_name=SHEETY_API_USERS_SHEET,
                                  authentication_code=USERS_SHEETY_AUTH_CODE)
            break
        else:
            front_desk.inform_user(message='Account already exists.')
            continue

    elif activity == 'update':
        if checked_data[0]:
            front_desk.inform_user(message='Enter updated account details:')
            new_data = account_manager.get_data()
            data_manager.update_data(row=checked_data[1],
                                     sheet_name=SHEETY_API_USERS_SHEET,
                                     api_endpoint=SHEETY_API_USERS,
                                     data_to_update=new_data,
                                     authentication_code=USERS_SHEETY_AUTH_CODE)
            message = 'Account updated successfully! Congrats!'
            front_desk.inform_user(message)
            break
        else:
            front_desk.inform_user(message='No such account in database.')
            continue
    else:
        if checked_data[0]:
            delete = data_manager.delete_data(api_endpoint=SHEETY_API_USERS,
                                              row_to_delete=checked_data[1],
                                              authentication_code=USERS_SHEETY_AUTH_CODE)
            if delete:
                break
            else:
                continue
        else:
            front_desk.inform_user(message='No such account in database.')
            continue

flight_ticket_data = data_manager.get_data(api_endpoint=SHEETY_API_FLIGHTS,
                                           sheet_name=SHEETY_API_FLIGHTS_SHEET,
                                           authentication_code=FLIGHTS_SHEETY_AUTH_CODE)
for row in flight_ticket_data:
    if row['iataCode'] == '':
        to_write = flight_finder.find_data(query=row['city'])
        data_to_write = {'iataCode': to_write['locations'][0]['code']}
        data_manager.update_data(row=row['id'],
                                 data_to_update=data_to_write,
                                 sheet_name=SHEETY_API_FLIGHTS_SHEET,
                                 api_endpoint=SHEETY_API_FLIGHTS,
                                 authentication_code=FLIGHTS_SHEETY_AUTH_CODE)

    data = flight_finder.find_cheap_flights(flight_from='LON',
                                            flight_to=row['iataCode'],
                                            date_from=formatted_current_date,
                                            date_to=formatted_date_to,
                                            price_to=row['lowestPrice'])
    if data:
        notification_manager.send_email_notification(data_to_send=data,
                                                     password=EMAIL_APP_PASS)
        print('Email sent. Check your mailbox :)')
