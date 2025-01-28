import secrets, string, json, os
from cryptography.fernet import Fernet
from Cryptography_functions import derive_key_scrypt, generate_salt
import base64

class PasswordManager:
    def __init__(self, user : str, master_password : str):
        self.user = user
        self.filepath = f"Password_Manager_Encrypted\\Passwords\\{user}_passwords.json"

        salt = base64.b64decode(master_password[:44].encode("utf-8"))
        self.fernet = Fernet(derive_key_scrypt(master_password[44:], salt))
        

        if not (os.path.exists(self.filepath)) :
            with open(self.filepath, 'w') as file:
                file.write('')
        else :
            pass

    def add_password(self, website: str, username: str, password: str) -> None:
        new_data = {
            website: {
                "username" : username,
                "password" : self.fernet.encrypt(password.encode()).decode(),
            }
        }
        try:
            with open(self.filepath, "r") as password_file :
                data = json.load(password_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError) :
            data = new_data
        else :
            data.update(new_data)
        with open(self.filepath, "w") as password_file :
            json.dump(data,password_file,indent=4)

    def retrieve_password(self, website: str) -> dict:
        retrieved_data = {
            website: {
                "username" : None,
                "password" : None,
            }
        }
        try:
            with open(self.filepath, "r") as password_file :
                data = json.load(password_file)

                if (website in data) :
                    encrypted_password = data[website]["password"]

                    retrieved_data[website]["username"] = data[website]["username"]
                    retrieved_data[website]["password"] = self.fernet.decrypt(encrypted_password).decode()
                return retrieved_data

        except (FileNotFoundError) :
            return retrieved_data
        
    def generate_random_password(self) -> str:
        char_pool = string.ascii_letters + string.digits + string.punctuation
        generated_password = ''.join(secrets.choice(char_pool) for _ in range(20))
        return generated_password

