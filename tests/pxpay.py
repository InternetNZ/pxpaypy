from string import ascii_letters, digits
from urllib import parse
import configparser
import unittest
import uuid
import webbrowser

from xml.etree.ElementTree import Element
from defusedxml.ElementTree import fromstring as parseXML
from hypothesis import given
from hypothesis.strategies import booleans, floats, text
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
        # intialize PxPay
        self.pxpay = pxpay.PxPay(
            url=config["URL"],
            user_id=config["UserID"],
            auth_key=config["AuthKey"])
        # generic transaction request
        self.generic_request = {
            "merchant_reference": "MREF",
            "amount": 1.00,
            "currency": "NZD",
            "url_success": config["URL_SUCCESS"],
            "url_fail": config["URL_FAIL"]}

    @given(
        merchant_reference=text(alphabet=ALPHANUMERIC, min_size=1),
        transaction_type=text(
            alphabet=[pxpay.TXN_AUTH, pxpay.TXN_PURCHASE],
            min_size=1),
        amount=floats(min_value=00.00, max_value=999999.99),
        transaction_id=text(alphabet=ALPHANUMERIC, min_size=1),
        add_bill_card=booleans(),
        billing_id=text(alphabet=ALPHANUMERIC),
        data_1=text(alphabet=ALPHANUMERIC),
        data_2=text(alphabet=ALPHANUMERIC),
        data_3=text(alphabet=ALPHANUMERIC),
        email=text(alphabet=ALPHANUMERIC),
        optional_text=text(alphabet=ALPHANUMERIC))
    def test_make_transaction_request_mock(
            self, merchant_reference, transaction_type, amount, transaction_id,
            add_bill_card, billing_id, data_1, data_2, data_3, email,
            optional_text):
        """Test XML generation of make_reques method"""
        xml = self.pxpay.make_transaction_request(
            merchant_reference=merchant_reference,
            transaction_type=transaction_type,
            amount=amount,
            currency="NZD",
            transaction_id=transaction_id,
            url_success="https://pass.nzrs.nz",
            url_fail="https://fail.nzrs.nz",
            add_bill_card=add_bill_card,
            billing_id=billing_id,
            data_1=data_1,
            data_2=data_2,
            data_3=data_3,
            email_address=email,
            optional_text=optional_text,
            mock=True)
        self.assertIsInstance(parseXML(xml), Element)

    def test_make_transaction_request(self):
        """Tests make_transaction_request method"""
        # authentication transaction
        url = self.pxpay.make_transaction_request(
            **self.generic_request,
            transaction_type=pxpay.TXN_AUTH,
            transaction_id=str(uuid.uuid4()).replace("-", "")[0:16],
            add_bill_card=True,
            billing_id="BILLID")
        self.assertIsNotNone(url)
        self.assertIsInstance(url, str)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        # purchase transaction
        url = self.pxpay.make_transaction_request(
            **self.generic_request,
            transaction_type=pxpay.TXN_PURCHASE,
            transaction_id=str(uuid.uuid4()).replace("-", "")[0:16])
        self.assertIsNotNone(url)
        self.assertIsInstance(url, str)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        # duplicate transaction IDs
        # attempt 1
        try:
            self.pxpay.make_transaction_request(
                **self.generic_request,
                transaction_type=pxpay.TXN_AUTH,
                transaction_id="TID-A")
        except Exception as e:
            # exception due to duplicate transaction ID may happen
            pass
        # attempt 2
        with self.assertRaises(
                Exception,
                msg="Request failed: TxnId/TxnRef duplicate"):
            self.pxpay.make_transaction_request(
                **self.generic_request,
                transaction_type=pxpay.TXN_AUTH,
                transaction_id="TID-A")

    @given(result=text(alphabet=ALPHANUMERIC, min_size=1))
    def test_get_transaction_status_mock(self, result):
        """Tests XML generation of get_transaction_status method"""
        xml = self.pxpay.get_transaction_status(result=result, mock=True)
        self.assertIsInstance(parseXML(xml), Element)

    def test_get_transaction_status(self):
        """Test get transaction status"""
        # authentication transaction
        billing_id = str(uuid.uuid4()).replace("-", "")
        transaction_id = str(uuid.uuid4()).replace("-", "")[0:16]
        url = self.pxpay.make_transaction_request(
            **self.generic_request,
            transaction_type=pxpay.TXN_AUTH,
            transaction_id=transaction_id,
            add_bill_card=True,
            billing_id=billing_id)
        webbrowser.open(url)
        result_url = input("Enter forwarding URL:")
        query_string = parse.urlparse(result_url).query
        self.assertTrue(len(query_string) > 0)
        parsed_query_string = parse.parse_qs(query_string)
        self.assertIn("userid", parsed_query_string)
        self.assertIn("result", parsed_query_string)
        result = parsed_query_string["result"][0]

        # get transaction status
        result = self.pxpay.get_transaction_status(result)
        labels = [
                "AmountSettlement", "AuthCode", "CardName", "CardNumber",
                "DateExpiry", "DpsTxnRef", "Success", "ResponseText",
                "DpsBillingId", "CardHolderName", "CurrencySettlement",
                "TxnType", "CurrencyInput", "MerchantReference", "ClientInfo",
                "TxnId", "BillingId", "TxnMac", "Cvc2ResultCode"]
        for label in labels:
            self.assertIn(label, result)
        self.assertEqual(result["TxnType"], pxpay.TXN_AUTH)
        self.assertEqual(result["TxnId"], transaction_id)
        self.assertEqual(result["BillingId"], billing_id)
        print("Transaction success: {}".format(result["Success"]))
