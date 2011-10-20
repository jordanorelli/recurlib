import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "recurlib",
    version = "0.0.1",
    author = "Jordan Orelli",
    author_email = "jordanorelli@gmail.com",
    description = ("A client for interacting with Recurly, a subscription \
                   billing service."),
    license = "MIT",
    keywords = "subscriptions billing payments ecommerce",
    packages = ['recurly', 'tests'],
    long_description = read('README'),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
)
