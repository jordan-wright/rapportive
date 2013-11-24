"""setup.py controls the build, testing, and distribution of the egg"""

from setuptools import setup, find_packages
import re
import os.path


PROJECT = "rapportive"
VERSION_REGEX = re.compile(r"""
    ^__version__\s=\s
    ['"](?P<version>.*?)['"]
""", re.MULTILINE | re.VERBOSE)

VERSION_FILE = os.path.join(PROJECT, "version.py")


def get_version():
    """Reads the version from the package"""
    with open(VERSION_FILE) as handle:
        lines = handle.read()
        result = VERSION_REGEX.search(lines)
        if result:
            return result.groupdict()["version"]
        else:
            raise ValueError("Unable to determine __version__")


def get_requirements():
    """Reads the installation requirements from requirements.pip"""
    with open("requirements.pip") as f:
        return [line.rstrip() for line in f if not line.startswith("#")]


setup(
    name=PROJECT,
    version=get_version(),
    description="Check list of emails using Rapportive API",
    # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='rapportive',
    author='Jordan Wright',
    author_email='jmwright798@gmail.com',
    url='https://github.com/jordan-wright/rapportive',
    license='MIT License',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    scripts=[
        'scripts/rapportive_cmd',
    ],
    install_requires=get_requirements(),
)
