from setuptools import setup, find_packages

setup(
    name="PxPayPy",
    version="0.1.0a1",
    packages=find_packages(),

    install_requires=["defusedxml>=0.5", "requests>=2.13"],

    author="Kesara Rathnayake",
    author_email="kesara@nzrs.net.nz",
    description="Python library for DPS PaymentExpress PxPay 2.0 API.",
    long_description="""\
Python library for DPS PaymentExpress PxPay 2.0 API. Also supports stored
credit card payments via PaymentExpress PxPost.""",
    license="GNU GPL v3",
    keywords="dps paymentexpress pxpay pxpost api",
    url="https://github.com/NZRS/pxpaypy",
)
