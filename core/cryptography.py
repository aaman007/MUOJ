from cryptography.fernet import Fernet


class Cryptography:
    def __init__(self, file_name='secret.key'):
        self.file_name = file_name

    def generate_key(self):
        """
        Generates a key and save it into a file
        """
        key = Fernet.generate_key()
        with open(self.file_name, "wb") as key_file:
            key_file.write(key)

    def load_key(self):
        """
        Loads the key named `secret.key` from the current directory.
        """
        return open(self.file_name, "rb").read()

    def encrypt_message(self, message):
        """ Encrypts a message """
        key = self.load_key()
        encoded_message = message.encode()
        f = Fernet(key)
        encrypted_message = f.encrypt(encoded_message).decode('utf-8')

        return encrypted_message

    def decrypt_message(self, encrypted_message):
        """ If message is str, encode to bytes string """
        if type(encrypted_message) == str:
            encrypted_message = encrypted_message.encode('utf-8')

        """ Decrypts an encrypted message """
        key = self.load_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message).decode('utf-8')

        return decrypted_message
