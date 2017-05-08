# pxpaypy
Python library for DPS PaymentExpress PxPay 2.0 API

## Usage
pip install pxpaypy

## Running Tests
* Install required libraries

        pip install -r requirements.txt
        pip install -r requirements.dev.txt

* Copy example configuration file and edit configuration file with UAT
authentication details

        cp tests/config.ini.example tests/config.ini

* Run tests

        python -m unittest discover tests  -p "*.py"
