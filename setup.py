
from setuptools import setup, find_packages

version = '5.3.5'

setup(
    name="alerta-sms",
    version=version,
    description='Alerta plugin for SMS',
    url='https://github.com/alerta/alerta-contrib',
    license='MIT',
    author='Nick Satterly',
    author_email='nick.satterly@theguardian.com',
    packages=find_packages(),
    py_modules=['alerta_sms'],
    install_requires=[
        'requests'
    ],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'alerta.plugins': [
            'sms = alerta_sms:ServiceIntegration'
        ]
    }
)

