"""
Main API entry point
TODO:
 - exception handler
"""
import logging
import requests
import urllib3

from thoughtspot.errors import ThoughtSpotApiError
from thoughtspot.rest.models.auth import Authenticator
from thoughtspot.rest.models.base import TSPublic
from thoughtspot.rest.models.metadata import Metadata
from thoughtspot.utils import TSConfig

# TODO: make this an option not default
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ThoughtSpot:
    """
    Provides access to thoughtspot API
    """
    def __init__(self, ts_config=None):
        """
        :param ts_config: configuration file
        """
        if ts_config:
            self._cnf = TSConfig(cnf_file=ts_config)
        else:
            self._cnf = TSConfig()

        self._logger = logging.getLogger(__name__)
        self._ts_url = self._cnf.get_thoughtspot_url()

        self._session = requests.session()
        self._session.verify = False
        # TODO: move to config?
        self._session.headers = {"X-Requested-By": "ThoughtSpot"}

        # setup functions
        self.auth = Authenticator(self)

        self.public = TSPublic()
        self.public.metadata = Metadata(self)
        self._logger.debug('API setup completed')

    def _post(self, path, data=None, verify=False):
        """
        :param path:
        :param data:
        :param verify:
        :return:
        """
        # silly validation check as we have posts with no data
        self._logger.debug('_post')
        try:
            if data:
                resp = self._session.post(
                    '{}{}'.format(self._ts_url, path),
                    data=data,
                    verify=verify
                )
            else:
                resp = self._session.post(
                    '{}{}'.format(self._ts_url, path),
                    verify=verify
                )
        except Exception as e:
            self._logger.error('failed to execute post: {}'.format(e))
            raise ThoughtSpotApiError(e)

        if resp.status_code >= 400:
            self._logger.error('failed to execute post')
            # TODO:
            #  clean this up just need to capture the basics right now
            #  capture possible errors and where to look ->
            #   400 is client issue (possible bug)
            #   500 is server error (contact admin fix and try again etc.)
            raise ThoughtSpotApiError('post to service failed', resp.status_code)
        # currently just return the response up the chain for further processing
        return resp

    def _get(self, path, payload=None, verify=False):
        """
        :param path:
        :param verify:
        :return:
        """
        self._logger.debug('_get')
        try:
            if payload:
                resp = self._session.get(
                    '{}{}'.format(self._ts_url, path),
                    params=payload,
                    verify=verify
                )
            else:
                resp = self._session.get(
                    '{}{}'.format(self._ts_url, path),
                    verify=verify
                )
        except Exception as e:
            self._logger.error('failed to execute post: {}'.format(e))
            raise ThoughtSpotApiError(e)

        if resp.status_code >= 400:
            self._logger.error('failed to execute post')
            # TODO:
            #  clean this up just need to capture the basics right now
            #  capture possible errors and where to look ->
            #   400 is client issue (possible bug)
            #   500 is server error (contact admin fix and try again etc.)
            raise ThoughtSpotApiError('get request to endpoint failed', resp.status_code)
        # currently just return the response up the chain for further processing
        return resp
