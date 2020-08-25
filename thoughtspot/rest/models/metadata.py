"""
public metadata api
"""
from thoughtspot.rest.models.base import TSBase


class Metadata(TSBase):
    """
    Metadata
    """
    def list_object_headers(self, payload={}):
        """
        TODO:
          - need to sort out validations for lots of arguments - right now will make it work only
            for get_tables python but will update for system
        :param payload:
        :return:
        """
        self._tsapi._logger.debug('attempting to get object headers, payload: {}'.format(payload))
        return self._tsapi._get(
            '/callosum/v1/tspublic/v1/metadata/listobjectheaders',
            payload
        )
