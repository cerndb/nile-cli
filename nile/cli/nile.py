import socket
import fire
import requests
from plumbum import local, cli

with cli.Config('~/.nile_rc') as conf:
    api_url = conf.get('api_url', 'localhost:5443')
    ssl_verify = conf.get('ssl_verify', 'yes') != 'no'  # Only skip ssl verification if 'no'


class Nile(object):
    """NILE command line interface application"""

    def __init__(self, debug=False):
        self._debug = debug

    def list(self):
        """List the clusters in this machine"""

        url = '{}/api/v1/host/{}/metadata'.format(api_url, socket.getfqdn())
        if self._debug:
            print('Sending request to {}'.format(url))

        response = requests.get(url=url, verify=ssl_verify)

        if self._debug:
            print(response)

        if response.status_code != 200:
            print('There was an error getting the metadata for {}'.format(socket.getfqdn()))
            exit(1)

        for cluster in response['response']:
            print('cluster={}'.format(cluster['name']))

    def status(self, instance):
        """List the clusters in this machine"""

        service = local['service']
        service['kafka status']


if __name__ == "__main__":
    fire.Fire(Nile)
