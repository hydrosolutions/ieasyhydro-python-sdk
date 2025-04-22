from setuptools import setup, find_packages

setup(
    name="ieasyhydro_sdk",
    version="0.3.0",
    packages=find_packages(),
    author="Domagoj Levanić",
    author_email="domagoj.levanic@encode.hr",
    description="Python SDK for iEasyHydro Rest API",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hydrosolutions/ieasyhydro-python-sdk",
    license='MIT',
    install_requires=[
        'requests>=2.31.0',
    ],
)
