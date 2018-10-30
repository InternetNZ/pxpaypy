.. PxPayPy documentation master file, created by
   sphinx-quickstart on Thu May 25 15:44:34 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PxPayPy
=======

PxPayPy is a Python library for DPS PaymentExpress PxPay 2.0 API. PxPayPy has
been tested to work with Python 3.5+.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

* :ref:`features`
* :ref:`installation`
* :ref:`setting_up`
* :ref:`first_transaction`
* :ref:`stored_credit_card_transactions`
    * :ref:`token_based_rebilling_with_pxpost`
* :ref:`make_transaction_request`
* :ref:`get_transaction_status`
* :ref:`pxpost_make_token_based_transaction`
  :ref:`transaction_types`
* :ref:`errors_and_exceptions`
* :ref:`contribute`
    * :ref:`running_tests`
    * :ref:`building_documentation`
* :ref:`license`

.. _features:

========
Features
========

* PxPayPy supports DPS PxPay 2.0 API.
* PxPayPy supports DPS PxPost token based payments with *CardNumber2*.

.. _installation:

============
Installation
============

Install this library with pip::

    pip install pxpaypy

.. _setting_up:

==========
Setting Up
==========

To initialize PxPay with *URL*, *PxPay User ID* and *PxPay Key*::

    from pxpaypy.pxpay import PxPay
    pxpay = PxPay("https://<pxpay url>", "<user id>", "<pxpay key>")

.. _first_transaction:

=================
First Transaction
=================

Example purchase transaction (``TXN_PURCHASE``) of $1.00 of currency type NZD::

    response = pxpay.make_transaction_request(
        merchant_reference="<merchant reference>",
        transaction_type=TXN_PURCHASE,
        amount=1.00,
        currency="NZD",
        transaction_id="<unique transaction id>",
        url_success="<success url>",
        url_fail="<fail url>")
    url = response["url"]

``make_transaction_request`` method returns an URL which allows user to enter
credit card details and original XML content returned by DPS, depending on
success or failure of the transaction, user will be directed to either
``url_success`` or ``url_fail``.

To determine the status of the transaction, retrieve the ``result`` parameter
from the redirected URLs' query string and pass it to
``get_transaction_status`` method::

    response = pxpay.get_transaction_status(result)
    result = response["result"]

``response`` is a Python dictionary with XML tags returned by PxPay API
(``result``) and original content returned by DPS (``xml``).

.. _stored_credit_card_transactions:

===============================
Stored Credit Card Transactions
===============================

To store credit card for future billing purposes, we should make a transaction
request of type ``TXN_AUTH`` and amount of $1.00 or more::

    response = pxpay.make_transaction_request(
        merchant_reference="<merchant reference>",
        transaction_type=TXN_AUTH,
        amount=1.00,
        currency="NZD",
        add_bill_card=True,
        billing_id="<billing id>",
        transaction_id="<unique transaction id>",
        url_success="<success url>",
        url_fail="<fail url>")
    result = response["result"]

``add_bill_card`` must be set to ``True``. ``billing_id`` is optional, if
``billing_id`` is not specified we have to use ``dps_billing_id`` generated
by PxPay. The URL returned by the ``make_transaction_request`` will allow user
to enter their credit card information.

Retrieve the ``result`` parameter from the redirected URLs' query string to
determine the success or failure of the transaction::

    response = pxpay.get_transaction_status(result)
    status = response["result"]
    if int(status["Success"]) == 1:
        dps_blling_id = status["DpsBillingId"]
        # DpsBillingId requires, if billing_id not set
        card_number2 = status["CardNumber2"]
        # CardNumber2 optinal for token based automated billing via PxPost

To re-bill a stored credit card with user interaction. User will have to enter
correct CVC on PaymentExpress hosted page. We can either user ``BillingID`` or
``DpsBillingID``::

    response = pxpay.make_transaction_request(
        merchant_reference="<merchant reference>",
        transaction_type=TXN_PURCHASE,
        amount=1.00,
        currency="NZD",
        dps_billing_id = dps_blling_id, # or we could use billing_id
        transaction_id="<unique transaction id>",
        url_success="<success url>",
        url_fail="<fail url>")
    url = response["url"]

URL will present user with transaction details and allow them to enter CVC, on
the success or failure user will be directed to correct URL. Grab ``result``
from query string of the redirected URL to get transaction status::

    response = pxpay.get_transaction_status(result)
    status = response["result"]

If ``status["Success"]`` is ``1`` then transaction was a success.

.. _token_based_rebilling_with_pxpost:

---------------------------------
Token based rebilling with PxPost
---------------------------------

Automated token based transactions can be done using PaymentExpress PxPost API.
This requires ``CardNumber2`` generated by PxPay add billing card transaction
and ``BillingID`` used in that transaction.


Initiate PxPost with *URL*, *PxPost User Name* and *PxPost Password*::

    from pxpaypy.pxpost import PxPost
    pxpost = PxPost("https://<pxpost url>", "<user name>", "<password>")

To initiate token based transaction use ``make_token_based_transaction`` method::

    response = pxpost.make_token_based_transaction(
        merchant_reference="<merchant reference>",
        transaction_type=TXN_PURCHASE,
        amount=1.00,
        currency="NZD",
        card_number_2=card_number_2,
        transaction_id="<unique transaction id>",
        billing_id=billing_id)
    result = response["result"]

``result`` is a Python dictionary with XML tags returned by PaymentExpress
PxPost. ``response["xml"]`` has the original XML returned by DPS.

.. _make_transaction_request:

========================
Make Transaction Request
========================

``make_transaction_request`` method returns an URL with credit card details
form. This method can be used to make both *Auth* and *Purchase* transactions,
as well as re-billing with user interaction (i.e. user has to enter CSC).

+----------------------+------------------------------------------------------+
|Argument              |Description                                           |
+======================+======================================================+
|``merchant_reference``|Merchant reference *(required)*                       |
+----------------------+------------------------------------------------------+
|``transaction_type``  |Transaction type *(required)*                         |
|                      |                                                      |
|                      |Possible values:                                      |
|                      |    ``TXN_AUTH`` Auth transaction                     |
|                      |    ``TXN_PURCHASE`` Purchase transaction             |
+----------------------+------------------------------------------------------+
|``amount``            |Amount *(required)*                                   |
+----------------------+------------------------------------------------------+
|``currency``          |Currency type *(required)*                            |
+----------------------+------------------------------------------------------+
|``transaction_id``    |Unique transaction ID *(required)*                    |
+----------------------+------------------------------------------------------+
|``url_success``       |URL for successful transactions *(required)*          |
+----------------------+------------------------------------------------------+
|``url_fail``          |URL for failed transactions *(required)*              |
+----------------------+------------------------------------------------------+
|``add_bill_card``     |Set this to ``True`` to store the card for rebilling. |
|                      |                                                      |
|                      |Default is ``False``.                                 |
+----------------------+------------------------------------------------------+
|``billing_id``        |Billing ID *(use this when rebill a stored card)*     |
+----------------------+------------------------------------------------------+
|``dps_billing_id``    |DPS billing ID *(use this when rebill a stored card)* |
+----------------------+------------------------------------------------------+
|``data_1``            |Data 1                                                |
+----------------------+------------------------------------------------------+
|``data_2``            |Data 2                                                |
+----------------------+------------------------------------------------------+
|``data_3``            |Data 3                                                |
+----------------------+------------------------------------------------------+
|``email_address``     |email address                                         |
+----------------------+------------------------------------------------------+
|``optional_text``     |Optional text                                         |
+----------------------+------------------------------------------------------+
|``mock``              |If set to ``True``, XML string will be retunred       |
|                      |without sending it the server.                        |
|                      |                                                      |
|                      |Default is ``False``.                                 |
+----------------------+------------------------------------------------------+

.. _get_transaction_status:

======================
Get Transaction Status
======================

``get_transaction_status`` method can be used to get the status of a completed
transaction. This method requires ``result`` parameter from query string of the
redirected URL.

This method returns a Python dictionary with XML tags returned by PxPay API.

+----------------------+------------------------------------------------------+
|Argument              |Description                                           |
+======================+======================================================+
|``result``            |``result`` paramenter from the redirected URL's query |
|                      |string. *(required)*                                  |
+----------------------+------------------------------------------------------+
|``mock``              |If set to ``True``, XML string will be retunred       |
|                      |without sending it the server.                        |
|                      |                                                      |
|                      |Default is ``False``.                                 |
+----------------------+------------------------------------------------------+

.. _pxpost_make_token_based_transaction:

====================================
PxPost: Make token based transaction
====================================

``make_token_based_transaction`` method on PxPost class can be used to purform
automated token based rebill transactions. This requires ``CardNumber2`` and
``BillingId`` from the add card transaction performed using PxPay.

This method returns a Python dictionary with XML tags returned by PxPost API.

+----------------------+------------------------------------------------------+
|Argument              |Description                                           |
+======================+======================================================+
|``merchant_reference``|Merchant reference *(required)*                       |
+----------------------+------------------------------------------------------+
|``transaction_type``  |Transaction type *(required)*                         |
|                      |                                                      |
|                      |Possible values:                                      |
|                      |    ``TXN_AUTH`` Auth transaction                     |
|                      |    ``TXN_COMPLETE``  Comlete transaction             |
|                      |    ``TXN_PURCHASE`` Purchase transaction             |
|                      |    ``TXN_REFUND``  Refund transaction                |
+----------------------+------------------------------------------------------+
|``amount``            |Amount *(required)*                                   |
+----------------------+------------------------------------------------------+
|``currency``          |Currency type *(required)*                            |
+----------------------+------------------------------------------------------+
|``transaction_id``    |Unique transaction ID *(required)*                    |
+----------------------+------------------------------------------------------+
|``card_number_2``     |Card number 2 returned by PxPay *(required)*          |
+----------------------+------------------------------------------------------+
|``billing_id``        |Billing ID used in PxPay add credit card transaction  |
|                      |*(required)*                                          |
+----------------------+------------------------------------------------------+
|``data_1``            |Data 1                                                |
+----------------------+------------------------------------------------------+
|``data_2``            |Data 2                                                |
+----------------------+------------------------------------------------------+
|``data_3``            |Data 3                                                |
+----------------------+------------------------------------------------------+
|``mock``              |If set to ``True``, XML string will be retunred       |
|                      |without sending it the server.                        |
|                      |                                                      |
|                      |Default is ``False``.                                 |
+----------------------+------------------------------------------------------+

.. _transaction_types:

=================
Transaction Types
=================

PxPay transaction types:

+----------------+---------------------------+-----------------------------------------+
|Label           |Description                |Python import                            |
+================+===========================+=========================================+
|``TXN_AUTH``    |Authentication transaction |``from pxpaypy.pxpay import TXN_AUTH``   |
+----------------+---------------------------+-----------------------------------------+
|``TXN_PURCHASE``|Purchase transaction       |``from pxpaypy.pxpay import TXN_PURCHAE``|
+----------------+---------------------------+-----------------------------------------+

PxPost transaction types:

+----------------+---------------------+-------------------------------------------+
|Label           |Descritption         |Python import                              |
+================+=====================+===========================================+
|``TXN_AUTH``    |Auth transaction     |``from pxpaypy.pxpost import TXN_AUTH``    |
+----------------+---------------------+-------------------------------------------+
|``TXN_COMPLETE``|Comlete transaction  |``from pxpaypy.pxpost import TXN_COMPLETE``|
+----------------+---------------------+-------------------------------------------+
|``TXN_PURCHASE``|Purchase transaction |``from pxpaypy.pxpost import TXN_PURCHASE``|
+----------------+---------------------+-------------------------------------------+
|``TXN_REFUND``  |Refund transaction   |``from pxpaypy.pxpost import TXN_REFUND``  |
+----------------+---------------------+-------------------------------------------+

.. _errors_and_exceptions:

=====================
Errors and Exceptions
=====================

In case of any error like invalid XML, API server cannot be reached etc,
PxPayPy will throw an Exception.

.. _contribute:

==========
Contribute
==========

* Issue Tracker: https://github.com/InternetNZ/pxpaypy/issues
* Source Code: https://github.com/InternetNZ/pxpaypy

.. _running_tests:

-------------
Running tests
-------------

To run PxPayPy tests, you need an UAT PxPay and PxPost accounts from DPS.

Install required Python libraries::

  pip install -r requirements.txt
  pip install -r requirements.dev.txt

Copy example configuration file and edit configuration file with UAT
authentication details::

    cp tests/config.ini.example tests/config.ini

Run tests::

  python -m unittest discover tests -p "*.py"

Some tests needs manual intervention. If you want to skip those tests, set
environment variable ``NO_MANUAL=1``.

.. _building_documentation:

----------------------
Building Documentation
----------------------

PxPayPy uses `Sphinx <http://www.sphinx-doc.org/>`_ to generate documentation.

Install required Python libraries::

  pip install -r requirements.docs.txt

Build documentation::

  sphinx-build -nW  docs docs/_build

Resulting documentations will be available on ``docs/_build`` directory.

.. _license:

=======
License
=======

Copyright (C) 2018 `Internet New Zealand Inc <https://internetnz.nz/>`_.

The project is licensed under the 
`GNU AGPL version 3
<https://github.com/InternetNZ/pxpaypy/blob/master/LICENSE>`_.
