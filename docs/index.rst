.. PxPayPy documentation master file, created by
   sphinx-quickstart on Thu May 25 15:44:34 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PxPayPy
=======

PxPayPy is a Python library for DPS PaymentExpress PxPay 2.0 API.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

* :ref:`features`
* :ref:`installation`
* :ref:`setting_up`
* :ref:`first_transaction`
* :ref:`stored_credit_card_transactions`
* :ref:`make_transaction_request`
* :ref:`get_transaction_status`
* :ref:`contribute`
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

    pxpay = PxPay("https://<pxpay url>", "<user id>", "<pxpay key>")

.. _first_transaction:

=================
First Transaction
=================

Example purchase transaction (``TXN_PURCHASE``) of $1.00 of currency type NZD::

    url = pxpay.make_transaction_request(
        merchant_reference="<merchant reference>",
        transaction_type=pxpay.TXN_PURCHASE,
        amount=1.00,
        currency="NZD",
        transaction_id="<unique transaction id>",
        url_success="<success url>",
        url_fail="<fail url>")

``make_transaction_request`` method returns an URL which allows user to enter
credit card details, depending on success or failure of the transaction, user
will be directed to either ``url_success`` or ``url_fail``.

To determind the status of the transaction, retrieve the ``result`` parameter
from the redirected URL's query string and pass it to
``get_transaction_status`` method::

    status = pxpay.get_transaction_status(result)

``status`` is a Python dictionary with XML tags returned by PxPay API.

.. _stored_credit_card_transactions:

===============================
Stored Credit Card Transactions
===============================

To store credit card for future billing purpases, we should make a transaction
request of type ``TXN_AUTH`` and amount of $1.00 or more::

    url = pxpay.make_transaction_request(
        merchant_reference="<merchant reference>",
        transaction_type=pxpay.TXN_AUTH,
        amount=1.00,
        currency="NZD",
        add_bill_card=True,
        billing_id="<billing id>",
        transaction_id="<unique transaction id>",
        url_success="<success url>",
        url_fail="<fail url>")

``add_bill_card`` must be set to ``True``. ``billing_id`` is optional, if
``billing_id`` is not specified we have to use ``dps_billing_id`` generated
by PxPay. The URL returened by the ``make_transaction_request`` will allow user
to enter their credit card information.

Retrieve the ``result`` parameter from the redirected URL's query string to
determeind the success or failure of the transaction::

    status = pxpay.get_transaction_status(result)
    if int(status["Success"]) == 1:
        dps_blling_id = status["DpsBillingId"]
        # DpsBillingId requires, if billing_id not set
        card_number2 = status["CardNumber2"]
        # CardNumber2 optinal for token based automated billing via PxPost

Rebill a stored credit card with user interation. User will have to enter
correct CVC on PaymentExpress hosted page. We can either user ``BillingID`` or
``DpsBillingID``::

    url = pxpay.make_transaction_request(
        merchant_reference="<merchant reference>",
        transaction_type=pxpay.TXN_PURCHASE,
        amount=1.00,
        currency="NZD",
        dps_billing_id = dps_blling_id, # or we could use billing_id
        transaction_id="<unique transaction id>",
        url_success="<success url>",
        url_fail="<fail url>")

URL will present user with transaction details and allow them to enter CVC, on
the success or failure user will be directed to correct URL. Grab ``result``
from query string of the redirected URL to get transaction status::

    status = pxpay.get_transaction_status(result)

If ``status["Success"]`` is ``1`` then transaction was a success.

.. _make_transaction_request:

========================
Make Transaction Request
========================

``make_transaction_request`` method returns an URL with credit card details
form. This method can be used to make both *Auth* and *Purchase* transactions,
as well as rebilling with user insteraction (i.e. user has to enter CSC).

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
|``url_success``       |URL for suceessful transactions *(required)*          |
+----------------------+------------------------------------------------------+
|``url_fail``          |URL for failed transactions *(required)*              |
+----------------------+------------------------------------------------------+
|``add_bill_card``     |Set this to ``True`` to store the card for rebilling. |
|                      |                                                      |
|                      |Default is ``False``.                                 |
+----------------------+------------------------------------------------------+
|``billing_id``        |Billing ID                                            |
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

.. _contribute:

==========
Contribute
==========

* Issue Tracker: https://github.com/NZRS/pxpaypy/issues
* Source Code: https://github.com/NZRS/pxpaypy

.. _license:

=======
License
=======

Copyright (C) 2017 NZRS Ltd.
The project is licensed under the 
`GNU GPL version 3 <https://github.com/NZRS/pxpaypy/blob/master/LICENSE>`_.
