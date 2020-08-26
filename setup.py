"""
setup util
"""
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='thoughtspot',
    version='1.0',
    description='demo packaging',
    long_description_content_type='text/markdown',
    long_description=README,
    author='thoughtspot csa team',
    author_email='demo@thoughtspot.com',
    license='MIT',
    packages=find_packages(),
    url='https://github.com/shawnbmccarthy/periscope',
    package_data={'': ['cfg/*.json']},
    data_files=[('./cfg', ['./cfg/thoughtspot.json'])]
)

install_requires = [
    'pycrypto==2.6.1',
    'requests==2.24.0'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires, include_package_data=True)

