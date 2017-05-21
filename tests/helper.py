import configparser
import unittest
import uuid
from xml.etree.ElementTree import Element

from defusedxml.ElementTree import fromstring as parseXML
import requests

from src import helper, pxpay


class TestHelper(unittest.TestCase):
    """Tests for helper module"""

    def setUp(self):
        # load configurations
        self.config = configparser.ConfigParser()
        self.config.read("tests/config.ini")
        self.config = self.config["DEFAULT"]
        # intialize PxPay
        self.pxpay = pxpay.PxPay(
            url=self.config["URL"],
            user_id=self.config["UserID"],
            auth_key=self.config["AuthKey"])

    def test_get_xml(self):
        """Tests get_xml method"""
        xml = self.pxpay.make_transaction_request(
            merchant_reference="MREF-helper",
            amount=1.00,
            currency="NZD",
            url_success=self.config["URL_SUCCESS"],
            url_fail=self.config["URL_FAIL"],
            transaction_type=pxpay.TXN_PURCHASE,
            transaction_id=str(uuid.uuid4()).replace("-", "")[0:16],
            mock=True)
        response = requests.post(
            self.config["URL"],
            data=xml,
            headers={'Content-Type': 'application/xml'})
        et = helper.get_xml(response)
        self.assertIsInstance(et, Element)
        self.assertIsNotNone(et.get("valid"))
        self.assertIsInstance(et.get("valid"), str)
        self.assertIsNotNone(et.getchildren())
        self.assertIsInstance(et.getchildren(), list)
        et_uri = et.getchildren()[0]
        self.assertIsNotNone(et_uri)
        self.assertIsInstance(et_uri, Element)
        self.assertEqual(et_uri.tag, "URI")
        self.assertIsNotNone(et_uri.text)
        self.assertIsInstance(et_uri.text, str)

    def test_process_status(self):
        """Tests process_status method"""
        # valid PxPay XML output
        valid_xml = {
            """
<Request valid="1">
  <URI>https://sec.paymentexpress.com/pxmi3/EF4054F622D6C4C1B4F9AEA59DC</URI>
</Request>""",
            """
<Response valid="1">
  <Success>1</Success>
  <TxnType>Purchase</TxnType>
  <CurrencyInput>NZD</CurrencyInput>
  <MerchantReference>Purchase Example</MerchantReference>
  <TxnData1></TxnData1>
  <TxnData2></TxnData2>
  <TxnData3></TxnData3>
  <AuthCode>113837</AuthCode>
  <CardName>Visa</CardName>
  <CardHolderName>CARDHOLDER NAME</CardHolderName>
  <CardNumber>411111........11</CardNumber>
  <DateExpiry>1111</DateExpiry>
  <ClientInfo>127.0.0.1</ClientInfo>
  <TxnId>P03E57DA8A9DD700</TxnId>
  <EmailAddress></EmailAddress>
  <DpsTxnRef>000000060495729b</DpsTxnRef>
  <BillingId></BillingId>
  <DpsBillingId></DpsBillingId>
  <AmountSettlement>1.00</AmountSettlement>
  <CurrencySettlement>NZD</CurrencySettlement>
  <DateSettlement>20100924</DateSettlement>
  <TxnMac>BD43E619</TxnMac>
  <ResponseText>APPROVED</ResponseText>
  <CardNumber2></CardNumber2>
  <Cvc2ResultCode>M</Cvc2ResultCode>
</Response>""",
            """
<foo valid="1">
  <bar></bar>
</foo>""",
            """
<foo valid="1"></foo>""",
            """
<foo bar="2" valid="1"></foo>""",
            """
<foo valid="1" bar="2"></foo>""", }

        for xml in valid_xml:
            self.assertIsInstance(helper.process_status(parseXML(xml)), dict)

        # invalid PxPay XML output
        invalid_xml = {
            """
<Request valid="2">
  <URI>https://sec.paymentexpress.com/pxmi3/EF4054F622D6C4C1B4F9AEA59DC</URI>
</Request>""",
            """
<foo valid="10"></foo>""",
            """
<foo bar="1" valid="3"></foo>""",
            """
<foo valid="2" bar="1"></foo>""", }

        for xml in invalid_xml:
            with self.assertRaises(Exception, msg="Invalid request."):
                helper.process_status(parseXML(xml))

        # valid PxPost XML output
        valid_xml = {
            """
<Txn>
  <Transaction success="1" reco="00" responseText="APPROVED" pxTxn="true">
    <Authorized>1</Authorized>
    <ReCo>00</ReCo>
    <RxDate>20170519021539</RxDate>
    <RxDateLocal>20170519141539</RxDateLocal>
    <LocalTimeZone>NZT</LocalTimeZone>
    <MerchantReference>My Reference</MerchantReference>
    <CardName>Visa</CardName>
    <Retry>0</Retry>
    <StatusRequired>0</StatusRequired>
    <AuthCode>006098</AuthCode>
    <AmountBalance>0.00</AmountBalance>
    <Amount>1.00</Amount>
    <CurrencyId>840</CurrencyId>
    <InputCurrencyId>840</InputCurrencyId>
    <InputCurrencyName>USD</InputCurrencyName>
    <CurrencyRate>1.00</CurrencyRate>
    <CurrencyName>USD</CurrencyName>
    <CardHolderName>C. HOLDER</CardHolderName>
    <DateSettlement>20170519</DateSettlement>
    <TxnType>Purchase</TxnType>
    <CardNumber>411111........11</CardNumber>
    <TxnMac>2BC20210</TxnMac>
    <DateExpiry>1212</DateExpiry>
    <ProductId></ProductId>
    <AcquirerDate></AcquirerDate>
    <AcquirerTime></AcquirerTime>
    <AcquirerId>0</AcquirerId>
    <Acquirer></Acquirer>
    <AcquirerReCo>00</AcquirerReCo>
    <AcquirerResponseText>APPROVED</AcquirerResponseText>
    <TestMode>0</TestMode>
    <CardId>2</CardId>
    <CardHolderResponseText>APPROVED</CardHolderResponseText>
    <CardHolderHelpText>The Transaction was approved</CardHolderHelpText>
    <CardHolderResponseDescription>The Transact</CardHolderResponseDescription>
    <MerchantResponseText>APPROVED</MerchantResponseText>
    <MerchantHelpText>The Transaction was approved</MerchantHelpText>
    <MerchantResponseDescription>The Transaction </MerchantResponseDescription>
    <UrlFail></UrlFail>
    <UrlSuccess></UrlSuccess>
    <EnablePostResponse>0</EnablePostResponse>
    <PxPayName></PxPayName>
    <PxPayLogoSrc></PxPayLogoSrc>
    <PxPayUserId></PxPayUserId>
    <PxPayXsl></PxPayXsl>
    <PxPayBgColor></PxPayBgColor>
    <PxPayOptions></PxPayOptions>
    <Cvc2ResultCode>P</Cvc2ResultCode>
    <AcquirerPort>10000000-10001407</AcquirerPort>
    <AcquirerTxnRef>677381</AcquirerTxnRef>
    <GroupAccount>9997</GroupAccount>
    <DpsTxnRef>000000010093aa3c</DpsTxnRef>
    <AllowRetry>1</AllowRetry>
    <DpsBillingId></DpsBillingId>
    <BillingId></BillingId>
    <TransactionId>0093aa3c</TransactionId>
    <PxHostId>00000001</PxHostId>
    <RmReason></RmReason>
    <RmReasonId>0000000000000000</RmReasonId>
    <RiskScore>-1</RiskScore>
    <RiskScoreText></RiskScoreText>
  </Transaction>
  <RmReason></RmReason>
  <RmReasonId>0000000000000000</RmReasonId>
  <RiskScore>-1</RiskScore>
  <RiskScoreText></RiskScoreText>
  <ReCo>00</ReCo>
  <ResponseText>APPROVED</ResponseText>
  <HelpText>Transaction Approved</HelpText>
  <Success>1</Success>
  <DpsTxnRef>000000010093aa3c</DpsTxnRef>
  <ICCResult></ICCResult>
  <TxnRef></TxnRef>
</Txn>
""",
            """
<foo bar="1">
  <bar></bar>
</foo>""",
            """
<foo></foo>""",
            """
<foo>
  <bar>foobar</bar>
  <bar>foobar</bar>
</foo>""",
            """
<foo>
  <bar>foobar</bar>
  <foobar></foobar>
</foo>""", }

        for xml in valid_xml:
            self.assertIsInstance(
                helper.process_status(parseXML(xml), pxpost=True), dict)

    def test_xml_to_dir(self):
        """Test for xml_to_dir function."""
        xml = """
<foo>
  <bar></bar>
</foo>"""
        results = helper.xml_to_dir(parseXML(xml))
        self.assertIsInstance(results, dict)
        self.assertIn("bar", results)

        xml = """
<foo>
  <bar1></bar1>
  <bar2></bar2>
</foo>"""
        results = helper.xml_to_dir(parseXML(xml))
        self.assertIsInstance(results, dict)
        for label in ["bar1", "bar2"]:
            self.assertIn(label, results)

        xml = """
<foo>
  <bar1>foo1</bar1>
  <bar2>foo2</bar2>
</foo>"""
        results = helper.xml_to_dir(parseXML(xml))
        self.assertIsInstance(results, dict)
        self.assertEqual("foo1", results["bar1"])
        self.assertEqual("foo2", results["bar2"])
