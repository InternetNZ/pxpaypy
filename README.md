# PxPayPy
Python library for DPS PaymentExpress PxPay 2.0 API

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

        python -m unittest discover tests  -p "*.py"

## Contribute
* Issue Tracker: https://github.com/NZRS/pxpaypy/issues
* Source Code: https://github.com/NZRS/pxpaypy

## License
Copyright (C) 2017 NZRS Ltd.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
