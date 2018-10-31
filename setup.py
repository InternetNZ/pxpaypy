from setuptools import setup, find_packages

setup(
    name="PxPayPy",
    version="0.1.3a1",
    packages=find_packages(),

    install_requires=["defusedxml>=0.5", "requests>=2.20"],

    py_modules=["pxpaypy"],

    author="Kesara Rathnayake",
    author_email="kesara@internetnz.net.nz",
    description="Python library for DPS PaymentExpress PxPay 2.0 API.",
    long_description="""\
Python library for DPS PaymentExpress PxPay 2.0 API. Also supports stored
credit card payments via PaymentExpress PxPost.""",
    license="GNU AGPL v3",
    keywords="dps paymentexpress pxpay pxpost api",
    url="https://github.com/InternetNZ/pxpaypy",
)
