# This file is part of PxPayPy.
#
# PxPayPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# PxPayPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public
# License along with PxPayPy. If not, see
# <http://www.gnu.org/licenses/>.

from string import ascii_letters, digits
from urllib import parse
from xml.etree.ElementTree import Element
import configparser
import unittest
import uuid
import webbrowser

from defusedxml.ElementTree import fromstring as parseXML
from hypothesis import given
from hypothesis.strategies import floats, text

from pxpaypy import pxpay, pxpost

ALPHANUMERIC = [ascii_letters, digits]


class TestPxPost(unittest.TestCase):
    """Tests for PxPost module"""

    def setUp(self):
        # load configurations
        self.config = configparser.ConfigParser()
        self.config.read("tests/config.ini")
        _config = self.config["DEFAULT_PXPOST"]
        # intialize PxPost
        self.pxpost = pxpost.PxPost(
            url=_config["URL"],
            user_name=_config["UserName"],
            password=_config["Password"])

    @given(
        merchant_reference=text(alphabet=ALPHANUMERIC, min_size=1),
        transaction_type=text(
            alphabet=[
                pxpost.TXN_AUTH, pxpost.TXN_COMPLETE, pxpost.TXN_PURCHASE,
                pxpost.TXN_REFUND],
            min_size=1),
        amount=floats(min_value=00.00, max_value=999999.99),
        transaction_id=text(alphabet=ALPHANUMERIC, min_size=1),
        card_number_2=text(alphabet=digits, min_size=12),
        billing_id=text(alphabet=ALPHANUMERIC),
        data_1=text(alphabet=ALPHANUMERIC),
        data_2=text(alphabet=ALPHANUMERIC),
        data_3=text(alphabet=ALPHANUMERIC))
    def test_make_token_based_transaction_mock(
            self, merchant_reference, transaction_type, amount, transaction_id,
            card_number_2, billing_id, data_1, data_2, data_3):
        """Test XML generation of make_token_based_transaction"""
        xml = self.pxpost.make_token_based_transaction(
            merchant_reference=merchant_reference,
            transaction_type=transaction_type,
            amount=amount,
            currency="NZD",
            transaction_id=transaction_id,
            card_number_2=card_number_2,
            billing_id=billing_id,
            data_1=data_1,
            data_2=data_2,
            data_3=data_3,
            mock=True)
        self.assertIsInstance(parseXML(xml), Element)

    def test_make_token_based_transaction(self):
        # Initiate PxPay
        _config = self.config["DEFAULT"]
        _pxpay = pxpay.PxPay(
            url=_config["URL"],
            user_id=_config["UserID"],
            auth_key=_config["AuthKey"])

        # Create token
        # authentication transaction
        billing_id = str(uuid.uuid4()).replace("-", "")
        url = _pxpay.make_transaction_request(
            merchant_reference="MREF",
            amount=1.00,
            currency="NZD",
            url_success=_config["URL_SUCCESS"],
            url_fail=_config["URL_FAIL"],
            transaction_type=pxpay.TXN_AUTH,
            transaction_id=str(uuid.uuid4()).replace("-", "")[0:16],
            add_bill_card=True,
            billing_id=billing_id)
        print("\n")
        print("Make sure following transaction succeeds.")
        webbrowser.open(url)
        result_url = input("Enter forwarding URL:")
        query_string = parse.urlparse(result_url).query
        self.assertTrue(len(query_string) > 0)
        parsed_query_string = parse.parse_qs(query_string)
        self.assertIn("userid", parsed_query_string)
        self.assertIn("result", parsed_query_string)
        result = parsed_query_string["result"][0]

        # get transaction status
        result = _pxpay.get_transaction_status(result)
        self.assertIn("Success", result)
        self.assertIn("CardNumber2", result)
        self.assertIn("BillingId", result)
        self.assertEqual(int(result["Success"]), 1)
        self.assertEqual(result["BillingId"], billing_id)
        card_number_2 = result["CardNumber2"]
        self.assertTrue(len(card_number_2) > 0)

        # make token based transaction
        transaction_id = str(uuid.uuid4()).replace("-", "")[0:16]
        amount = 10.00
        result = self.pxpost.make_token_based_transaction(
            merchant_reference="MREF_POST",
            transaction_type=pxpost.TXN_PURCHASE,
            amount=amount,
            currency="NZD",
            card_number_2=card_number_2,
            transaction_id=transaction_id,
            billing_id=billing_id)

        labels = ["ResponseText", "Success", "DpsTxnRef", "TxnRef"]
        for label in labels:
            self.assertIn(label, result)
        self.assertEqual(int(result["Success"]), 1)
        self.assertEqual(result["ResponseText"], "APPROVED")
        self.assertEqual(result["TxnRef"], transaction_id)
        self.assertEqual(int(result["Transaction"]["Authorized"]), 1)
        self.assertEqual(float(result["Transaction"]["Amount"]), amount)
        self.assertEqual(result["Transaction"]["BillingId"], billing_id)
        self.assertEqual(result["Transaction"]["CardNumber2"], card_number_2)
