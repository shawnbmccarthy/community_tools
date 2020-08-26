"""
setup util
"""
from setuptools import setup, find_packages

setup_args = dict(
    name='thoughtspot',
    version='1.0',
    description="demo packaging",
    packages=find_packages(),
    url="https://github.com/shawnbmccarthy/periscope",
    data_files=[('config', ['cfg/thoughtspot.json'])]
)

install_requires = [
    'pycrypto==2.6.1',
    'requests==2.24.0'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires, include_package_data=True)

