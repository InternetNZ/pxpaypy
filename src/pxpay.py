"""DPS PaymentExpress PxPay 2.0 API"""

import requests
from defusedxml.ElementTree import fromstring as parseXML

# transaction types
TXN_AUTH = "Auth"
TXN_PURCHASE = "Purchase"

# requests
_BILLING_CARD = """
<EnableAddBillCard>1</EnableAddBillCard>
<BillingId>{billing_id}</BillingId>"""

_OPTIONAL = "<Opt>{optional_text}</Opt>"

_REQUEST = """
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
    {billing_card}
    <UrlSuccess>{url_success}</UrlSuccess>
    <UrlFail>{url_fail}</UrlFail>
    {optional}
</GenerateRequest>"""


class PxPay:
    """DPS PaymentExpress PxPay 2.0 API"""
    def __init__(self, url, user_id, auth_key):
        self.url = url
        self.user_id = user_id
        self.auth_key = auth_key

    def make_transaction_request(
            self, merchant_reference, transaction_type, amount, currency,
            transaction_id, url_success, url_fail, billing_id=None,
            data_1="", data_2="", data_3="", email_address="",
            optional_text=None, mock=False):
        """Returns PxPay URL for credit card payment"""

        if billing_id is not None:
            billing_card = _BILLING_CARD.format(billing_id=billing_id)
        else:
            billing_card = ""
        if optional_text is not None:
            optional = _OPTIONAL.format(optional_text=optional_text)
        else:
            optional = ""

        xml = _REQUEST.format(
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
            billing_card=billing_card,
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

    def _get_url(self, response):
        """Returns URL from PxPay response."""
        if response.status_code != 200:
            raise(Exception("Server responded with {status}: {reason}".format(
                status=response.status_code, reason=response.reason)))
        else:
            try:
                et = parseXML(response.text)
            except Exception as e:
                raise(Exception("Error parsing response: {description}".format(
                    description=str(e))))
            uri = et.find("URI")
            if uri is not None:
                return uri.text
            else:
                raise(Exception("Request failed: {reason}".format(
                    reason=et.find("ResponseText").text)))
