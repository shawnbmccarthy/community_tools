"""
setup util
"""
from setuptools import setup

setup(
    name='pythoughtspot',
    version='1.0',
    description="demo packaging",
    url="https://github.com/shawnbmccarthy/periscope",
    data_files=[('config', ['cfg/thoughtspot.json'])]
)
