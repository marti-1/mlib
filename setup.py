#! /usr/bin/env python

DESCRIPTION = "apex: friendly data-science toolkit"
DISTNAME = 'apex'
MAINTAINER = 'Martynas Miliauskas'
MAINTAINER_EMAIL = 'martynas.miliauskas@protonmail.com'
VERSION = '0.3.0'
LICENSE = ""
URL = ""
DOWNLOAD_URL=""
INSTALL_REQUIRES = [
        'numpy>=1.16.2',
        'pandas>=0.24.1',
        'matplotlib>=3.0.3',
        'arrow>=0.15.4'
]
CLASSIFIERS =[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
]
PYTHON_REQUIRES='>=3.6'

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup

if __name__ == "__main__":

    setup(
        name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        install_requires=INSTALL_REQUIRES,
        packages=setuptools.find_packages(),
        classifiers=CLASSIFIERS,
        python_requires=PYTHON_REQUIRES
    )
