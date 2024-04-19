import requests
import flight_club_front_desk


class DataManager:
    """
    Class responsible for communication with Google sheets.
    """

    def __init__(self, front_desk: flight_club_front_desk.FrontDesk) -> None:
        """
        Initialize data attributes for AccountManager class.
        :param front_desk: Instance of FrontDesk class. Responsible
        for informing the user about status of requests.
        """
        self.front_desk = front_desk

    def get_data(self, api_endpoint: str, sheet_name: str,
                 authentication_code: str = None) -> list:
        """
        Return list of rows with data from Google Sheets using
        `api_endpoint` request.

        :param authentication_code: Api authentication code.
        :param sheet_name: Name of the Google Sheet.
        :param api_endpoint: Api endpoint used to get data.
        """
        if authentication_code:
            headers = {
                "Authorization": f"Bearer {authentication_code}"
            }
            response = requests.get(url=api_endpoint, headers=headers)
        else:
            response = requests.get(url=api_endpoint)
        response.raise_for_status()
        return response.json()[sheet_name]

    def update_data(self, row: int,
                    data_to_update: dict,
                    sheet_name: str,
                    api_endpoint: str,
                    authentication_code: str = None) -> None:
        """
        Update Google sheet by passing `data_to_update` as a parameter
        to post request.

        :param authentication_code: Api authentication code.
        :param api_endpoint: Api endpoint used to edit data.
        :param data_to_update: New data to be written.
        :param sheet_name: Name of the Google sheet.
        :param row: Google sheet row to be updated.
        """

        params_to_write = {
            sheet_name: data_to_update

        }

        if authentication_code:
            headers = {
                'Authorization': f'Bearer {authentication_code}'
            }
            response = requests.put(url=f'{api_endpoint}/{row}',
                                    json=params_to_write,
                                    headers=headers)

        else:
            response = requests.put(url=f'{api_endpoint}/{row}',
                                    json=params_to_write)
        response.raise_for_status()

    def add_data(self, sheet_name: str, new_data: dict,
                 api_endpoint: str, authentication_code: str = None) -> None:
        """
        Add new row of the data to the `sheet_name` Google sheet.

        :param authentication_code: Api authentication code.
        :param api_endpoint: Api endpoint used to add data to Google
            sheets.
        :param sheet_name: Name of Google Sheet.
        :param new_data: Data to be added to `sheet_name` Google Sheet.
        """

        params_to_add = {
            sheet_name: new_data

        }
        if authentication_code:
            headers = {
                "Authorization": f"Bearer {authentication_code}"
            }
            response = requests.post(url=api_endpoint, json=params_to_add,
                                     headers=headers)

        else:
            response = requests.post(url=api_endpoint, json=params_to_add)
        response.raise_for_status()
        message = 'Account created successfully! Congrats!'
        self.front_desk.inform_user(message)

    def delete_data(self, api_endpoint: str, row_to_delete: str,
                    authentication_code: str = None) -> bool:
        """
        Delete row from Google Sheets.

        Get confirmation from the user if he wants to delete an account.
        If True then delete account and return bool True. Return
        False otherwise.
        :param authentication_code: Api authentication code.
        :param api_endpoint: Api endpoint used to delete row.
        :param row_to_delete: Number of the row to delete.
        """
        delete = input("Are you sure you want to delete account?"
                       " Y/N:\n").strip().casefold()
        if delete == 'y':
            if authentication_code:
                headers = {
                    'Authorization': f'Bearer {authentication_code}'
                }

                response = requests.delete(url=f"{api_endpoint}/{row_to_delete}",
                                           headers=headers)

            else:
                response = requests.delete(url=f"{api_endpoint}/{row_to_delete}")
            response.raise_for_status()

            message = 'Account deleted successfully.'
            self.front_desk.inform_user(message)
            return True
        else:
            return False

    def check_account(self, account_data: dict,
                      account_list: list) -> tuple:
        """
        Check if `account_data` exists in `account_list` returned from
        Google Sheet.

        Return tuple containing bool True and number of row to update
        if account data exist in returned data from Google
        Sheets. Return False and None otherwise.
        :param account_list: List of the accounts returned from the
            Google Sheet.
        :param account_data: Dictionary containing 3 items:
            'firstName', 'lastName', 'email' as the keys and values from
            the Google Sheet.
        """
        if account_list:
            # iterate over the account list
            for index, row in enumerate(account_list):
                # iterate over the items from account data to compare them
                # with the items from account_list.
                for key, value in account_data.items():
                    if value == row[key]:
                        # Go and check next item in account_data
                        pass
                    else:
                        # Break inner loop and go to next row in account_list
                        # to check the values against the account_data items.
                        break
                # if loop executes it means that the account data matches data
                # in one of the rows. Then break out of the loop using
                # return keyword
                else:
                    row = account_list[index]['id']
                    return True, row
            # If outer loop terminates itself then it means that there was
            # no record that matched account_data.
            else:
                return False, None
        else:
            return False, None
