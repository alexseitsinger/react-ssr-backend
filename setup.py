#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
from setup_utils import read, read_section

PACKAGE_NAME = "react-ssr"
SOURCE_DIR_NAME = "react_ssr"
GITHUB_URL = "https://github.com/alexseitsinger/{}-backend".format(PACKAGE_NAME)
HOMEPAGE_URL = GITHUB_URL
README_NAME = "README.md"

setup(
    name=PACKAGE_NAME,
    version=read(("src", SOURCE_DIR_NAME, "__init__.py"), "__version__"),
    description=read_section((README_NAME,), "Description", (0,)),
    long_description=read((README_NAME,)),
    long_description_content_type="text/markdown",
    author="Alex Seitsinger",
    author_email="software@alexseitsinger.com",
    url=HOMEPAGE_URL,
    install_requires=["requests", "Django>=1.11", "click"],
    package_dir={"": "src"},
    packages=find_packages("src", exclude=["tests"]),
    include_package_data=True,
    license="BSD 2-Clause License",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Framework :: Django",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    keywords=["django", "react", "server-side rendering"],
    project_urls={
        "Documentation": HOMEPAGE_URL,
        "Source": GITHUB_URL,
        "Tracker": "{}/issues".format(GITHUB_URL),
    },
)
