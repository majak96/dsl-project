import codecs
import os

from setuptools import find_packages, setup

PACKAGE_NAME = "tx-survey"
VERSION = "0.1.0"
AUTHOR = "Tim 3"
AUTHOR_EMAIL = "timisaprojekat@gmail.com"
DESCRIPTION = "A domain-specific language for definining web-based surveys"
KEYWORDS = "textX DSL python domain specific languages survey questions"
LICENSE = "MIT"
URL = "https://github.com/majak96/dsl-project"

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    keywords=KEYWORDS,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["*.tx"]},
    install_requires=["textx_ls_core"],
    entry_points={"textx_languages": ["srvy = grammar:srvy"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
