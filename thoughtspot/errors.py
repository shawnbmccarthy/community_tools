"""
Exceptions raised by ThoughtSpot library
"""


class ThoughtSpotError(Exception):
    """
    Base ThoughtSpot error
    """
    def __init__(self, msg='', label='GENERIC'):
        """

        :param msg:
        :param label:
        """
        super(ThoughtSpotError, self).__init__(msg)
        self._msg = msg
        self._label = label

    def __str__(self):
        """

        :return:
        """
        return '{} - {}'.format(self._label, self._msg)


class ThoughtSpotApiError(ThoughtSpotError):
    """
    Rest Api Errors
    """
    def __init__(self, msg='', status_code=None):
        """

        :param msg:
        :param status_code:
        """
        super(ThoughtSpotApiError, self).__init__(msg=msg, label='HTTP_REST')
        self._status_code = status_code

    def __str__(self):
        """

        :return:
        """
        return '{}(status code:{})'.format(super().__str__(), str(self._status_code))


class ThoughtSpotConfigError(ThoughtSpotError):
    """
    Configuration Errors
    """
    def __init__(self, msg='', config_key=None):
        """

        :param msg:
        :param config_key:
        """
        super(ThoughtSpotConfigError, self).__init__(msg=msg, label='TS_CONFIG')
        self._config_key = config_key

    def __str__(self):
        """

        :return:
        """
        return '{}(key:{})'.format(super().__str__(), str(self._config_key))
