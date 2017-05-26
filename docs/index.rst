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
* :ref:`make_transaction_request`
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

Example purchase transaction of $1.00 of currency type NZD::

    url = pxpay.make_transaction_request(
        merchant_reference="<merchant reference>",
        transaction_type=pxpay.TXN_PURCHASE,
        amount=1.00,
        currency="NZD",
        transaction_id="<transaction id>",
        url_success="<success url>",
        url_fail="<fail url>")

``make_transaction_request`` method returns an URL which allows user to enter
credit card details, depending on success or failure of the transaction, user
will be directed to either ``url_success`` or ``url_fail``.

To determind the status of the transaction, retrieve the ``result`` parameter
from the redirected URL's query string and pass it to
``get_transaction_status`` method::

    status = pxpay.get_transaction_status(result)

``status`` is a Python dictionary with XML tags returns by PxPay API.

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
|                      |    ``pxpay.TXN_AUTH`` Auth transaction               |
|                      |    ``pxpay.TXN_PURCHASE`` Purchase transaction       |
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
