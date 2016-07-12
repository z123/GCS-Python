from distutils.util import convert_path
from setuptools import find_packages
from setuptools import setup

setup_args = dict(
    name='GCS-Python',
    description='Simple Python client for interacting with Google Cloud Storage.',
    url='https://github.com/z123/GCS-Python',
    version='.01',
    license='Apache',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'google-api-python-client',
        'httplib2',
    ],
    author='Zaheen'
)

if __name__ == '__main__':
    setup(**setup_args)
