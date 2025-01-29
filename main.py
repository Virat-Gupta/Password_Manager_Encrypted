from Password_Manager import PasswordManager
from User_Handler import UserHandler

def login_screen() -> int:
    print(r"""
     ___  _   ___ _____      _____  ___ ___    __  __   _   _  _   _   ___ ___ ___ 
    | _ \/_\ / __/ __\ \    / / _ \| _ \   \  |  \/  | /_\ | \| | /_\ / __| __| _ \
    |  _/ _ \\__ \__ \\ \/\/ / (_) |   / |) | | |\/| |/ _ \| .` |/ _ \ (_ | _||   /
    |_|/_/ \_\___/___/ \_/\_/ \___/|_|_\___/  |_|  |_/_/ \_\_|\_/_/ \_\___|___|_|_\
    """)
    print("0. Exit")
    print("1. Register")
    print("2. Login")
    print("3. Remove User")
    choice = int(input("Choose Option:"))
    if (choice in [0, 1, 2, 3]) :
        return choice
    else :
        print("[+] Select Something!")
        login_screen()

def after_login_screen(user: str) -> None:
    print("\n")
    print(f"Welcome {user}")
    print("0. Exit")
    print("1. Add Password")
    print("2. Retrieve Password")
    choice = int(input("Choose Option:"))
    if (choice in [0, 1, 2]) :
        return choice
    else :
        print("[+] Select Something!")
        after_login_screen()

def after_login(password_manager: PasswordManager) -> None:
    while True:
        choice = after_login_screen(password_manager.user)
        if (choice == 0) :
            return
        elif (choice == 1) :
            website = input("Enter Website Name :")
            username = input("Enter Username/Email :")
            password = input("Enter Password (Leave Blank for Random Password)")
            if (password == '') :
                password = password_manager.generate_random_password()
            password_manager.add_password(website, username, password)
            print("[+] PASSWORD ADDED SUCCESSFULLY!")
        elif (choice == 2) :
            website = input("Enter Website Name :")
            data = password_manager.retrieve_password(website)
            print(f"[+] USERNAME FOR {website} :{data[website]["username"]}")
            print(f"[+] PASSWORD For {website} :{data[website]["password"]}")


def main():
    user_handler = UserHandler()
    while True:
        choice = login_screen()
        if (choice == 0) :
            exit(0)
        elif (choice == 1):
            user = input("Enter UserName :")
            master_password = input("Enter Password (keep it Secure!) :")
            if user_handler.add_user(user,master_password) :
                print("[+] User Added Successfully")
            else :
                print("[+] User Already Exist, retry!")
        elif (choice == 2) :
            user = input("Enter UserName :")
            master_password = input("Enter Password :")
            
            if user_handler.login_user(user, master_password):
                print("[+] Login Success!")
                password_manager = PasswordManager(user,master_password + user_handler.get_user_salt(user))
                after_login(password_manager)
            else :
                print("[+] Wrong Password, or User Does not exit")
        elif (choice == 3) :
            user = input("Enter UserName :")
            master_password = input("Enter Password :")
            if user_handler.login_user(user) :
                confirm = input("Type 'CONFIRM' to remove the user :")
                if confirm == "CONFIRM":
                    print("[+] USER DELETED.")
                    user_handler.remove_user(user)
                else :
                    print("[+] USER NOT DELETED")
            else : 
                print("[+] User or Password Incorrect.")



if (__name__ == "__main__") :
    main()