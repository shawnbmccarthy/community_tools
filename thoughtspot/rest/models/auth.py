"""
auth support
"""
from .base import TSBase


class Authenticator(TSBase):
    """
    Represents the base authenticator model
    /tspublic/v1/session
    """
    def login(self):
        """
        login
        :return:
        """
        self._tsapi._logger.debug('attempting login')
        ui = self._tsapi._cnf.get_user_info()
        return self._tsapi._post(
            '/callosum/v1/session/login', { 'username': ui[0], 'password': ui[1] }
        )

    def logout(self):
        """
        logout
        :return:
        """
        self._tsapi._logger.debug('attempting logout')
        return self._tsapi._post('/callosum/v1/session/logout')