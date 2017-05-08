from string import ascii_letters, digits
import configparser
import random
import unittest

from xml.etree.ElementTree import Element
from defusedxml.ElementTree import fromstring as parseXML
from hypothesis import given
from hypothesis.strategies import floats, text
import requests

from src import pxpay

ALPHANUMERIC = [ascii_letters, digits]


class TestPxPay(unittest.TestCase):
    """Tests for PxPay module"""

    def setUp(self):
        # load configurations
        config = configparser.ConfigParser()
        config.read("tests/config.ini")
        config = config["DEFAULT"]
        self.pxpay = pxpay.PxPay(
            url=config["URL"],
            user_id=config["UserID"],
            auth_key=config["AuthKey"])

    @given(
        merchant_reference=text(alphabet=ALPHANUMERIC, min_size=1),
        transaction_type=text(
            alphabet=[pxpay.TXN_AUTH, pxpay.TXN_PURCHASE],
            min_size=1),
        amount=floats(min_value=00.00, max_value=999999.99),
        transaction_id=text(alphabet=ALPHANUMERIC, min_size=1),
        billing_id=text(alphabet=ALPHANUMERIC),
        data_1=text(alphabet=ALPHANUMERIC),
        data_2=text(alphabet=ALPHANUMERIC),
        data_3=text(alphabet=ALPHANUMERIC),
        email=text(alphabet=ALPHANUMERIC),
        optional_text=text(alphabet=ALPHANUMERIC))
    def test_make_request_mock(
            self, merchant_reference, transaction_type, amount, transaction_id,
            billing_id, data_1,
            data_2, data_3, email, optional_text):
        """Test XML generation of make_reques function"""
        xml = self.pxpay.make_request(
            merchant_reference=merchant_reference,
            transaction_type=transaction_type,
            amount=amount,
            currency="NZD",
            transaction_id=transaction_id,
            url_success="https://pass.nzrs.nz",
            url_fail="https://fail.nzrs.nz",
            billing_id=billing_id,
            data_1=data_1,
            data_2=data_2,
            data_3=data_3,
            email_address=email,
            optional_text=optional_text,
            mock=True)
        self.assertIsInstance(parseXML(xml), Element)

    def test_make_request(self):
        """Tests make_request function"""
        generic_request = {
            "merchant_reference": "MREF",
            "amount": 1.00,
            "currency": "NZD",
            "url_success": "https://pass.nzrs.nz",
            "url_fail": "https://fail.nzrs.nz"}

        # authentication transaction
        url = self.pxpay.make_request(
            **generic_request,
            transaction_type=pxpay.TXN_AUTH,
            transaction_id="TID-{}".format(str(random.randint(10000, 999999))),
            billing_id="BILLID")
        self.assertIsNotNone(url)
        self.assertIsInstance(url, str)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        # purchase transaction
        url = self.pxpay.make_request(
            **generic_request,
            transaction_type=pxpay.TXN_PURCHASE,
            transaction_id="TID-{}".format(str(random.randint(10000, 999999))))
        self.assertIsNotNone(url)
        self.assertIsInstance(url, str)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        # duplicate transaction IDs
        # attempt 1
        try:
            self.pxpay.make_request(
                **generic_request,
                transaction_type=pxpay.TXN_AUTH,
                transaction_id="TID-A")
        except Exception as e:
            # exception due to duplicate transaction ID may happen
            pass
        # attempt 2
        with self.assertRaises(
                Exception,
                msg="Request failed: TxnId/TxnRef duplicate"):
            self.pxpay.make_request(
                **generic_request,
                transaction_type=pxpay.TXN_AUTH,
                transaction_id="TID-A")
