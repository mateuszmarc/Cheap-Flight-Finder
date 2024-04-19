class FrontDesk:
    """
    Class responsible for communication with the user.

    User is able to create, update and delete his account.
    This class is responsible for recognition of the user need and
    passes duties to the AccountManager.
    """

    def get_user_need(self) -> str:
        """
        Return string describing the option that the user has chooses.

        for e.g. if he wants to delete his account then return 'delete'
        string which will be recognized by the other object in order to
        complete the task.

        :return: Command the user wants to perform.
        """
        options = ['open', 'update', 'delete', 'check']
        while True:
            print("Welcome in the Flight Club. What do you want to do?\n"
                  "Open account (Open) / Update account (Update) / "
                  "Delete account: (Delete) / Check Flights (Check):")
            activity = input().casefold()
            if activity in options:
                return activity
            else:
                print("There is no such option. Try again:")

    def inform_user(self, message: str) -> None:
        """
        Display `message` for the user on the screen.
        :param message: Message to display.
        """
        print(message)
