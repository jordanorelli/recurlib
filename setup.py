import os
from setuptools import setup

setup(
    name="recurlib",
    version="0.0.7",
    author="Jordan Orelli",
    author_email="jordanorelli@gmail.com",
    description=("A client for interacting with Recurly, a subscription \
                   billing service."),
    license="MIT",
    keywords="subscriptions billing payments ecommerce",
    url="https://github.com/jordanorelli/recurlib",
    packages=['recurly', 'recurly.managers', 'recurly.models', 'tests'],
    install_requires=['python-dateutil < 2.0', 'requests'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
)
