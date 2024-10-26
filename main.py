import os
from argparse import ArgumentParser
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from hashlib import sha256
from pathlib import Path
from shutil import make_archive
from tempfile import NamedTemporaryFile

def create_fernet(phrase: str) -> Fernet:
    """Creates a fernet object with a key based on a phrase."""
    return Fernet(urlsafe_b64encode(sha256(phrase.encode()).digest()))
    
def decrypt(input_path: str, phrase: str):
    """Decrypts an encrypted file or directory using a phrase-based key.

    Arguments
    ---------
        input_path : str
            The file or directory to decrypt. Requires the .textlock extension.
        phrase : str
            The phrase used to derive the decryption key.
    Raises
    ------
        FileExistsError:
            An decrypted version of the file or directory already exists.
        FileNotFoundError: 
            There is no file or directory at the specified input path.
        ValueError: 
            The file does not have the .textlock extension.
        cryptography.fernet.InvalidToken:
            The supplied phrase does not match that used in encryption.
    """

    # An exception is raised if the file extension is invalid:
    if not input_path.endswith('.textlock'):
        raise ValueError('The target requires the .textlock extension.')

    # The phrase is used to create a fernet object:
    fernet = create_fernet(phrase)
    
    # The contents of the path are read and decrypted:
    print('Decrypting content...')
    decrypted_content = fernet.decrypt(Path(input_path).read_bytes())

    # The resulting decrypted bytes are output to a new file:
    print('Writing decrypted content to file...')
    output_path = input_path.rstrip('.textlock')
    with open(output_path, 'xb') as file:
        file.write(decrypted_content)

    print('Decryption successful.')

def encrypt(input_path: str, phrase: str):
    """Encrypts a file or directory using a phrase-based key.

    Arguments
    ---------
        input_path : str
            The file or directory to encrypt.
        phrase : str
            The phrase used to derive the encryption key.
    Raises
    ------
        FileExistsError:
            An encrypted version of the file or directory is already present.
        FileNotFoundError: 
            There is no file or directory at the specified input path.
    """

    # The output path is initialised with the same value as the input path:
    output_path = input_path

    # If the path is a directory, it is temporarily archived:
    if os.path.isdir(input_path):
        print('Archiving directory contents...')
        tmp = NamedTemporaryFile()
        input_path = make_archive(
            base_name=tmp.name,
            format='gztar',
            root_dir=input_path,
            base_dir='',
        )
        output_path += '.tar.gz'

    # The output path is labelled as an encrypted file:
    output_path += '.textlock'        

    # The phrase is used to create a fernet object:
    fernet = create_fernet(phrase)

    # The contents of the path are read and encrypted:
    print('Encrypting content...')
    encrypted_content = fernet.encrypt(Path(input_path).read_bytes())        

    # The resulting encrypted bytes are output to a new file:
    print('Writing encrypted content to file...')
    with open(output_path + '.textlock', 'xb') as file:
        file.write(encrypted_content)
        
    print('Encryption successful.')

#TODO: arg parser