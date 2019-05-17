#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
from setup_utils import DIRECTORY_NAME, PACKAGE_NAME, read, read_section

URL = "https://github.com/alexseitsinger/{}-backend".format(DIRECTORY_NAME)
README_NAME = "README.md"


setup(
    name=PACKAGE_NAME,
    version=read(("src", PACKAGE_NAME, "__init__.py",), "__version__"),
    description=read_section((README_NAME,), "Description", (0,)),
    long_description=read((README_NAME,)),
    long_description_content_type="text/markdown",
    author="Alex Seitsinger",
    author_email="contact@alexseitsinger.com",
    url=URL,
    install_requires=["requests", "Django>=1.11"],
    package_dir={"": "src"},
    packages=find_packages("src", exclude=["tests"]),
    include_package_data=True,
    license="BSD 2-Clause License",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Framework :: Django",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    keywords=["django", "react", "server-side rendering"],
    project_urls={
        "Source": URL,
        "Tracker": "{}/issues".format(URL)
    }
)
