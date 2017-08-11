"""DPS PaymentExpress PxPay 2.0 API"""
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

import requests

from pxpaypy import helper

# transaction types
TXN_AUTH = "Auth"
TXN_PURCHASE = "Purchase"

# requests
_BILL_CARD = "<EnableAddBillCard>1</EnableAddBillCard>"

_BILLING_ID = "<BillingId>{billing_id}</BillingId>"

_DPS_BILLING_ID = "<DpsBillingId>{dps_billing_id}</DpsBillingId>"

_OPTIONAL = "<Opt>{optional_text}</Opt>"

_TRANSACTION_REQUEST = """
<GenerateRequest>
    <PxPayUserId>{user_id}</PxPayUserId>
    <PxPayKey>{auth_key}</PxPayKey>
    <MerchantReference>{merchant_reference}</MerchantReference>
    <TxnType>{transaction_type}</TxnType>
    <AmountInput>{amount:.2f}</AmountInput>
    <CurrencyInput>{currency}</CurrencyInput>
    <TxnData1>{data_1}</TxnData1>
    <TxnData2>{data_2}</TxnData2>
    <TxnData3>{data_3}</TxnData3>
    <EmailAddress>{email_address}</EmailAddress>
    <TxnId>{transaction_id}</TxnId>
    {bill_card}
    {billing_id}
    {dps_billing_id}
    <UrlSuccess>{url_success}</UrlSuccess>
    <UrlFail>{url_fail}</UrlFail>
    {optional}
</GenerateRequest>"""

_RESULT_REQUEST = """
<ProcessResponse>
    <PxPayUserId>{user_id}</PxPayUserId>
    <PxPayKey>{auth_key}</PxPayKey>
    <Response>{response}</Response>
</ProcessResponse>"""


class PxPay:
    """DPS PaymentExpress PxPay 2.0 API"""
    def __init__(self, url, user_id, auth_key):
        self.url = url
        self.user_id = user_id
        self.auth_key = auth_key

    def make_transaction_request(
            self, merchant_reference, transaction_type, amount, currency,
            transaction_id, url_success, url_fail, add_bill_card=False,
            billing_id=None, dps_billing_id=None, data_1="", data_2="",
            data_3="", email_address="", optional_text=None, mock=False):
        """Returns PxPay URL for credit card payment and original XML"""

        # check if add bill card is set
        if add_bill_card:
            bill_card = _BILL_CARD
        else:
            bill_card = ""

        # check if billing id is present
        if billing_id is not None:
            billing_id = _BILLING_ID.format(billing_id=billing_id)
        else:
            billing_id = ""

        # check if dps billing id is present
        if dps_billing_id is not None:
            dps_billing_id = _DPS_BILLING_ID.format(
                dps_billing_id=dps_billing_id)
        else:
            dps_billing_id = ""

        # check if optional text is present
        if optional_text is not None:
            optional = _OPTIONAL.format(optional_text=optional_text)
        else:
            optional = ""

        xml = _TRANSACTION_REQUEST.format(
            user_id=self.user_id,
            auth_key=self.auth_key,
            merchant_reference=merchant_reference,
            transaction_type=transaction_type,
            amount=amount,
            currency=currency,
            data_1=data_1,
            data_2=data_2,
            data_3=data_3,
            email_address=email_address,
            transaction_id=transaction_id,
            bill_card=bill_card,
            billing_id=billing_id,
            dps_billing_id=dps_billing_id,
            url_success=url_success,
            url_fail=url_fail,
            optional=optional)

        if mock:
            return xml
        else:
            response = requests.post(
                self.url,
                data=xml,
                headers={'Content-Type': 'application/xml'})
            url = self._get_url(response)
            return {"url": url, "xml": response.text}

    def get_transaction_status(self, result, mock=False):
        """Returns transaction result & original XML"""
        xml = _RESULT_REQUEST.format(
            user_id=self.user_id,
            auth_key=self.auth_key,
            response=result)
        if mock:
            return xml
        else:
            response = requests.post(
                self.url,
                data=xml,
                headers={'Content-Type': 'application/xml'})
            xml_response = helper.get_xml(response)
            dps_response = helper.process_status(xml_response)
            return {"result": dps_response, "xml": response.text}

    def _get_url(self, response):
        """Returns URL from PxPay response."""
        et = helper.get_xml(response)

        if (et.get("valid") != "1"):
            raise(Exception("Invalid request."))

        uri = et.find("URI")
        if uri is not None:
            return uri.text
        else:
            raise(Exception("Request failed: {reason}".format(
                reason=et.find("ResponseText").text)))
