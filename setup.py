#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

tests_require = [
    'coverage',
    'coveralls'
]

setup(
    name='law-service',
    version='0.1.1',
    description='Law API and crawler',
    keywords=[
        'provenance', 'graph', 'model', 'PROV', 'PROV-DM', 'PROV-JSON', 'JSON',
        'PROV-XML', 'PROV-N'
    ],
    author='Stefan Bieliauskas',
    author_email='open@conts.de',
    url='https://github.com/DLR-SC/prov-db-connector',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6'
    ],
    license="Apache License 2.0",

    packages=find_packages(),
    package_dir={
        'law': 'law'
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==1.0.2',
        'Scrapy==1.7.2',
        'neo4j==1.7.1',
        'multi-rake==0.0.1'
    ],
    extras_require={
        'test': tests_require,
        'dev': tests_require
    },

    test_suite='law.test',
)
