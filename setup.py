from setuptools import setup, find_packages


def readme():
    with open("README.md", 'r') as f:
        return f.read()


setup(
    name="mvol_api",
    description="An API for mvol project specific information, backed by the digcollretriever " +
    "and knowledge of the mvol filesystem specification.",
    version="0.0.1",
    long_description=readme(),
    author="Brian Balsamo",
    author_email="balsamo@uchicago.edu",
    packages=find_packages(
        exclude=[
        ]
    ),
    include_package_data=True,
    url='https://github.com/uchicago-library/mvol_api',
    install_requires=[
        'flask>0',
        'flask_env',
        'flask_restful',
        'jsonschema',
        'requests'
    ],
    tests_require=[
        'pytest'
    ],
    test_suite='tests'
)
