"""DPS PaymentExpress PxPost API (token based transactions)"""
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
            dps_response = helper.process_status(xml_response, True)
            return {"result": dps_response, "xml": response.text}
