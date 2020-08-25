"""
Basic utility classes for health check applications
TODO: Need to document
"""
import base64
import json
import logging
import logging.config
from Crypto import Random
from Crypto.Cipher import AES

from .errors import ThoughtSpotConfigError


class AESCipher:
    """
    Wrapper to AES
    TODO: is there a better way to setup a key?
    """
    def __init__(self, key='tsconfigfiledefaultpasswordforhc'):
        """
        initialize AESCipher with key to use
        :param key: key of length 16, 24, or 32 bytes long default value 'mysecretpassword'
        :raises ValueError: when key is not the appropriate length
        """
        self._logger = logging.getLogger()
        if len(key) not in [16, 24, 32]:
            raise ValueError('key must be 16, 24, or 32 bytes long')
        self.key = key
        self._logger.debug('AES Cipher Setup')

    @staticmethod
    def pad(text):
        """
            pad the raw data
            :param text: string
            :return: string padded
        """
        return \
            text + \
            (AES.block_size - len(text) % AES.block_size) * \
            chr(AES.block_size - len(text) % AES.block_size)

    @staticmethod
    def unpad(text):
        """
        :param text:
        :return:
        """
        return text[:-ord(text[len(text) - 1:])]

    def encrypt(self, plaintext):
        """
        Encrypt plaintext using random initialization vector
        :param plaintext:
        :return:
        """
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(self.pad(plaintext)))

    def encrypt_to_str(self, plaintext):
        """

        :param plaintext:
        :return:
        """
        return self.encrypt(plaintext).decode()

    def decrypt(self, ciphertext):
        """
        returns a binary representation of the decrypted data
        :param ciphertext:
        :return:
        """
        ciphertext = base64.b64decode(ciphertext)
        iv = ciphertext[:AES.block_size]
        ct = ciphertext[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(ct))

    def decrypt_str(self, ciphertext):
        """
        returns decrypted string of plaintext
        :param ciphertext:
        :return:
        """
        return self.decrypt(ciphertext).decode()


class TSConfig:
    """
    TSConfig represents a basic JSON configuration to be used by the
    health check application
    """
    def __init__(self, cnf_file='./cfg/thoughtspot.json'):
        """
        initialize with a configuration file, by default the thoughtspot.json which is
        shipped with the application
        :param cnf_file:
        """
        self._cipher = AESCipher()
        self._cnf_file = cnf_file
        self._load_cnf()

        logging.config.dictConfig(self.config['logging'])
        self._logger = logging.getLogger()
        self._logger.debug('thoughtspot configurator setup finished')

    def _load_cnf(self):
        """
        :return:
        """
        with open(self._cnf_file) as cnf_data:
            self.config = json.load(cnf_data)
        self._validate()

    def _validate(self):
        """
        Simple validate of top level keys
        Occurs before logging
        :return:
        """
        keys = ('thoughtspot', 'creds', 'logging')
        for k in keys:
            if k not in self.config:
                raise ThoughtSpotConfigError(
                    'missing configuration key, please check documentation',
                    k
                )

    def _commit_config(self):
        """
        :return:
        """
        self._logger.info('Attempting to commit changes to config file')
        with open(self._cnf_file, 'w') as outfile:
            json.dump(self.config, outfile, indent=2)

        self._logger.info('Successfully committed changes to config file')
        self._load_cnf()
        self._logger.info('Successfully reloaded configuration cache')

    def add_user_info(self, user, password, label='default', upsert=True):
        """
        Add a user with an encrypted password to the configuration file
        If this user already exists the user will be updated
        :param user:
        :param password:
        :param label:
        :param upsert:
        :return:
        """
        self._logger.debug('attempting to update user info')
        if label in self.config['creds']:
            if not upsert:
                raise ThoughtSpotConfigError(
                    'credential label {} already exists, set arg upsert=True'.format(label),
                    label
                )
        else:
            self._logger.info('upserting existing user')

        self.config['creds'][label] = {
            'username': user,
            'password': self._cipher.encrypt_to_str(password)
        }

        self._commit_config()
        self._logger.info('user info committed to configuration file')

    def get_user_info(self, label='default', decrypt=True):
        """
        return a set representing the username and password.
        By default the password will be decrypted
        - please note that it will use the AESCipher default key, if you
          change the key you must decrypt the password yourself
        :param label:
        :param decrypt:
        :return:
        """
        self._logger.debug('attempting to get user info')
        if label not in self.config['creds']:
            raise ThoughtSpotConfigError(
                'credential label {} does not exist'.format(label),
                label
            )
        if decrypt:
            self._logger.info('returning decrypted user information')
            return (
                self.config['creds'][label]['username'],
                self._cipher.decrypt_str(self.config['creds'][label]['password'])
            )
        else:
            self._logger.info('returning encrypted user information')
            return (
                self.config['creds'][label]['username'],
                self.config['creds'][label]['password']
            )

    def add_thoughtspot_host(self, host, port=443, is_secure=True):
        """
        update existing thoughtspot host
        :param host:
        :param port:
        :param is_secure:
        :return:
        """
        self._logger.debug('attempting to update thoughtspot host information')
        self.config['thoughtspot']['url']['host'] = host
        self.config['thoughtspot']['url']['port'] = port
        self.config['thoughtspot']['url']['is_secure'] = is_secure
        self._commit_config()
        self._logger.info('host info committed to configuration file')

    def get_thoughtspot_host(self):
        """

        :return:
        """
        self._logger.debug('attempting to get thoughtspot host')
        return self.config['thoughtspot']['url']['host']

    def get_thoughtspot_url(self):
        """

        :return:
        """
        self._logger.debug('attempting to build thoughtspot url')
        protocol = 'http'
        if self.config['thoughtspot']['url']['is_secure']:
            protocol = 'https'

        return '{}://{}:{}'.format(
            protocol,
            self.config['thoughtspot']['url']['host'],
            self.config['thoughtspot']['url']['port']
        )
