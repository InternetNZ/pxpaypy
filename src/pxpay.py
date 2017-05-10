"""DPS PaymentExpress PxPay 2.0 API"""

import requests
from defusedxml.ElementTree import fromstring as parseXML

# transaction types
TXN_AUTH = "Auth"
TXN_PURCHASE = "Purchase"

# requests
_BILL_CARD = "<EnableAddBillCard>1</EnableAddBillCard>"

_BILLING_ID = "<BillingId>{billing_id}</BillingId>"

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
            billing_id=None, data_1="", data_2="", data_3="", email_address="",
            optional_text=None, mock=False):
        """Returns PxPay URL for credit card payment"""

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
            return self._get_url(response)

    def get_transaction_status(self, result, mock=False):
        """Returns transaction status"""
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
            return self._process_status(response)

    def _get_xml(self, response):
        """Returns XML object from web response"""
        if response.status_code != 200:
            raise(Exception("Server responded with {status}: {reason}".format(
                status=response.status_code, reason=response.reason)))
        else:
            try:
                et = parseXML(response.text)
            except Exception as e:
                raise(Exception("Error parsing response: {description}".format(
                    description=str(e))))
            return et

    def _get_url(self, response):
        """Returns URL from PxPay response."""
        et = self._get_xml(response)

        if (et.get("valid") != "1"):
            raise(Exception("Invalid request."))

        uri = et.find("URI")
        if uri is not None:
            return uri.text
        else:
            raise(Exception("Request failed: {reason}".format(
                reason=et.find("ResponseText").text)))

    def _process_status(self, response):
        """Returns transaction status"""
        et = self._get_xml(response)

        if (et.get("valid") != "1"):
            raise(Exception("Invalid request."))

        result = {}
        for element in et.getchildren():
            result[element.tag] = element.text
        return result
