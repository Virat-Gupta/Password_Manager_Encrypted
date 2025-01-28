import os, json, base64
from Cryptography_functions import derive_key_scrypt, generate_salt

class UserHandler:
    def __init__(self):
        self.user_filepath = "users.json"
        if not os.path.exists(self.user_filepath) :
            with open(self.user_filepath, 'w') as file:
                file.write('')

    def add_user(self, user: str, master_password: str) -> bool:
        salt = generate_salt()

        new_data = {user : base64.b64encode(salt).decode('utf-8') + derive_key_scrypt(master_password, salt).decode()}
        try:
            with open(self.user_filepath, "r") as password_file :
                data = json.load(password_file)
                if (user in data) : 
                    return False
        except (FileNotFoundError, json.decoder.JSONDecodeError) :
            data = new_data
        else :
            data.update(new_data)
        with open(self.user_filepath, "w") as password_file :
            json.dump(data,password_file,indent=4)
            return True
    
    def login_user(self, user: str, master_password: str) -> bool:
        new_data = {None : None}

        with open(self.user_filepath, 'r') as users:
            data = json.load(users)
            
            if (user in data) :
                salt = base64.b64decode(data[user][:44].encode("utf-8"))
                hashed_pasword = derive_key_scrypt(master_password, salt).decode()
                if (hashed_pasword == data[user][44:]) : 
                    return True
            return False

    def remove_user(self, user: str):
        with open(self.user_filepath, 'r') as users :
            data = json.load(users)

        if user in data: 
            del data[user]
            if os.path.exists(f"Passwords\\{user}_passwords.json") :
                os.remove(f"Passwords\\{user}_passwords.json")

            with open(self.user_filepath, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        return False
    
    def get_user_salt(self, user: str) -> str:
        with open(self.user_filepath, 'r') as users :
            data = json.load(users)
            if user in data:
                return data[user][:44]
            else :
                return None

