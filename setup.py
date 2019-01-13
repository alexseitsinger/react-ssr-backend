#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# https://setuptools.readthedocs.io/en/latest/setuptools.html

from __future__ import absolute_import
from __future__ import print_function
from glob import glob
from setuptools import setup, find_packages
from os.path import abspath, basename, dirname, join, splitext

here = abspath(dirname(__file__))

with open(join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install sampleproject
    #
    # And where it will live on PyPI: https://pypi.org/project/sampleproject/
    #
    # There are some restrictions on what makes a valid project name
    # specification here:
    # https://packaging.python.org/specifications/core-metadata/#name
    #
    # Required
    name="react-ssr",

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    #
    # Required
    version="0.2.3",

    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    #
    # Required
    description="Backend service for server-side rendering react applications with django.",

    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    #
    # Often, this is the same as your README, so you can just read it in from
    # that file directly (as we have already done above)
    #
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    #
    # Optional
    long_description=long_description,

    # Denotes that our long_description is in Markdown; valid values are
    # text/plain, text/x-rst, and text/markdown
    #
    # Optional if long_description is written in reStructuredText (rst) but
    # required for plain-text or Markdown; if unspecified, "applications should
    # attempt to render [the long_description] as text/x-rst; charset=UTF-8 and
    # fall back to text/plain if it is not valid rst" (see link below)
    #
    # This field corresponds to the "Description-Content-Type" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    #
    # Optional (see note above)
    long_description_content_type="text/markdown",

    # This should be a valid link to your project"s main homepage.
    #
    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    #
    # Optional
    url="https://www.github.com/alexseitsinger/react-ssr-backend",

    # This should be your name or the name of the organization which owns the
    # project.
    #
    # Optional
    author="Alex Seitsinger",

    # This should be a valid email address corresponding to the author listed
    # above.
    #
    # Optional
    author_email="alexseitsinger@gmail.com",

    # Classifiers help users find your project by categorizing it.
    #
    # classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    #
    # Optional
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",

        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Utilities",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",

        # Pick your license as you wish
        "License :: OSI Approved :: BSD License",
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Optional
    keywords=[
        # eg:
        #   "sample", "test"
    ],

    py_modules=[
        splitext(basename(path))[0] for path in glob("src/*.py")
    ],

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    # Required
    packages=find_packages("src"),

    # Tell distutils packages are under "./src"
    # Required if we store packages under a "src" directory.
    #
    # Optional
    package_dir={"": "src"},

    # A file or a string to specify the type of license for this package.
    #
    # Optional
    license="BSD 2-Clause License",

    # Whether the project can be safely installed and run from a zip file. If
    # this argument is not supplied, the bdist_egg command will have to
    # analyze all of your project’s contents for possible problems each time
    # it builds an egg.
    #
    # Optional
    zip_safe=False,

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip"s requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    #
    # Optional
    install_requires=[
        # eg:
        #   "six", or "six>=1.7",
        "requests",
        "django>=2.0",
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    #
    # Optional
    extras_require={
        # eg:
        #   "rst": ["docutils>=0.11"],
        #   ":python_version=="2.6"": ["argparse"],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    #
    # You do not need to use this option if you are using
    # include_package_data, unless you need to add e.g. files that are
    # generated by your setup script and build process. (And are therefore not
    # in source control or are files that you don’t want to include in your
    # source distribution.)
    #
    # Optional
    package_data={
        # eg:
        #   "sample": ["package_data.dat"],
    },

    # This tells setuptools to automatically include any data files it finds
    # inside your package directories that are specified by your MANIFEST.in
    # file.
    include_package_data=True,

    # Although "package_data" is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, "data_file" will be installed into "<sys.prefix>/my_data"
    #
    # Optional
    data_files=[
        # eg:
        #   ("my_data", ["data/data_file"]),
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    #
    # Optional
    entry_points={
        # eg:
        #   "console_scripts": [
        #       "sample=sample:main",
        #   ],
    },

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what"s used to render the link text on PyPI.
    #
    # Optional
    project_urls={
        # eg:
        #   "Bug Reports": "https://github.com/pypa/sampleproject/issues",
        #   "Funding": "https://donate.pypi.org",
        #   "Say Thanks!": "http://saythanks.io/to/example",
        #   "Source": "https://github.com/pypa/sampleproject/",
    },
)
