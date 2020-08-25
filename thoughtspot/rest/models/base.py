"""
some base classes that will be inherited
"""


class TSBase:
    """
    TSBase
    """
    def __init__(self, tsapi):
        """
        :param tsapi:
        """
        self._tsapi = tsapi


class TSPublic:
    """
    TSPublic
    """
    def __init__(self):
        self.metadata = None
