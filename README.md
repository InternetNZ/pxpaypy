# PxPayPy
Python library for DPS PaymentExpress PxPay 2.0 API

Documentation: https://pxpaypy.readthedocs.io/en/latest/

**Note: This repository has not been used since Dec 2018 and is therefore currently archived. You are happy to fork it, but before using it, please verify that the libraries and packages included haven't been subject to a security vulnerability in the meantime.**

## Features
* Supports DPS PxPay 2.0 API
* Supports DPS PxPost token based payments with CardNumber2

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

        python -m unittest discover tests -p "*.py"


* Some tests needs manual intervention. If you want to skip those tests, set
environment variable `NO_MANUAL=1`.

## Building Documentation
* Install required Python libraries

        pip install -r requirements.docs.txt

* Build documentation

        sphinx-build -nW  docs docs/_build

* Resulting documentations will be available on `docs/_build directory`.

## Contribute
* Issue Tracker: https://github.com/InternetNZ/pxpaypy/issues
* Source Code: https://github.com/InternetNZ/pxpaypy

## License
Copyright (C) 2018 [Internet New Zealand Inc](https://internetnz.nz/).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with this program. If not, see
<http://www.gnu.org/licenses/>.
