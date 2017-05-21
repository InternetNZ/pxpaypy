"""DPS PaymentExpress PxPost API (token based transactions)"""

import requests

from . import helper

# transaction types
TXN_AUTH = "Auth"
TXN_COMPLETE = "Complete"
TXN_PURCHASE = "Purchase"
TXN_REFUND = "Refund"

# requests
_TRANSACTION_REQUEST = """
<Txn>
    <PostUsername>{user_name}</PostUsername>
    <PostPassword>{password}</PostPassword>
    <TxnType>{transaction_type}</TxnType>
    <InputCurrency>{currency}</InputCurrency>
    <Amount>{amount:.2f}</Amount>
    <MerchantReference>{merchant_reference}</MerchantReference>
    <CardNumber2>{card_number_2}</CardNumber2>
    <TxnData1>{data_1}</TxnData1>
    <TxnData2>{data_2}</TxnData2>
    <TxnData3>{data_3}</TxnData3>
    <TxnId>{transaction_id}</TxnId>
    <BillingId>{billing_id}</BillingId>
</Txn>"""


class PxPost:
    """DPS PaymentExpress PxPost API (token based transactions)"""
    def __init__(self, url, user_name, password):
        self.url = url
        self.user_name = user_name
        self.password = password

    def make_token_based_transaction(
            self, merchant_reference, transaction_type, amount, currency,
            transaction_id, card_number_2, billing_id="", data_1="", data_2="",
            data_3="", mock=False):
        """Perform token based transaction with CardNumber2"""

        xml = _TRANSACTION_REQUEST.format(
            user_name=self.user_name,
            password=self.password,
            transaction_type=transaction_type,
            currency=currency,
            amount=amount,
            merchant_reference=merchant_reference,
            card_number_2=card_number_2,
            data_1=data_1,
            data_2=data_2,
            data_3=data_3,
            transaction_id=transaction_id,
            billing_id=billing_id)

        if mock:
            return xml
        else:
            response = requests.post(
                self.url,
                data=xml,
                headers={'Content-Type': 'application/xml'})
            xml_response = helper.get_xml(response)
            return helper.process_status(xml_response, True)
