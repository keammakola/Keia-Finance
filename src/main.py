import os
import time
from data_manager import create_db
from user_management import create_account, login_account

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    clear_screen()
    print("What would you like to do today?\n"
          "1. Investments\n"
          "2. Finance Tracker\n"
          "3. Budgeting\n"
          "4. Logout")

    choice = input("Choose an option: ").strip()
    return choice

def login_flow():
    while True:
        clear_screen()
        print("Welcome to Keia Finance, your AI-powered personal finance assistant!\n")
        print("1. Create a new account")
        print("2. Login to an existing account")
        print("3. Exit\n")

        choice = input("Your choice: ").strip()

        if choice == "1":
            if create_account():
                print("Account created! Now, please log in.")
                time.sleep(1.5)
            else:
                input("Press Enter to continue...")
        elif choice == "2":
            user = login_account()
            if user:
                return user
            else:
                input("Press Enter to try again...")
        elif choice == "3":
            print("Goodbye!")
            time.sleep(1.5)
            clear_screen()
            return None
        else:
            print("Hmm, that choice doesn’t look right. Try again.")
            time.sleep(1.5)
            input("Press Enter to continue...")

def main():
    create_db()

    try:
        user = login_flow()
        if not user:
            return


        while True:
            choice = main_menu()
            if choice == "1":
                print("Investment tracking feature coming soon!")
                time.sleep(1.5)

            elif choice == "2":
                print("Finance Tracker feature coming soon!")
                time.sleep(1.5)

            elif choice == "3":
                print("Budgeting tool coming soon!")
                time.sleep(1.5)
            elif choice == "4":
                print(f"Logging out. See you next time, {user['name']}! 👋")
                break
            else:
                print("Invalid choice, please try again.")
                time.sleep(1.5)
    except Exception as e:
        print(f"Oops, something went wrong: {e}")

if __name__ == "__main__":
    main()
