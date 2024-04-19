class AccountManager:
    """
    Representation of the class responsible for creating, updating and
    deleting user accounts.
    """

    def get_data(self) -> dict:
        """
        Return dictionary based on given user's name, surname, email and
        password.

        Get first name, last name, email and password for the user and
        return in order to save this data Google sheets.
        Prompt user to type email address two times in order to confirm
        that both entered emails are the same. If not, inform user to
        type email address again.

        :return: Dictionary containing name, last name, and email address
            as the values.
        """
        print("Mateusz Flight Club!")
        phone_number = ''
        first_name = input("What is your name?\n").strip()
        last_name = input("What is your last name?\n").strip()
        while True:
            try:
                phone_number = int(input("What is your phone number?\n").strip())
                break
            except ValueError:
                print("Wrong phone number format. Try again.")
                continue

        while True:
            email_1 = input("Please enter your email address.\n").strip()
            email_2 = input("Please confirm your email address.\n").strip()
            if email_1 == email_2 and all([email_2, email_1]):
                break
            else:
                print("Email don't match. Please try again.")

        data_to_add = {
            'firstName': first_name,
            'lastName': last_name,
            'email': email_1,
            'phoneNumber': phone_number,
        }
        return data_to_add
