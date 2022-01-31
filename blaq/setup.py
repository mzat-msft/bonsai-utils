from setuptools import find_namespace_packages, setup

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    author="Marco Zatta",
    author_email="marco.zatta@microsoft.com",
    url="https://docs.microsoft.com/bonsai",
    keywords=["bonsai", "autonomous systems"],
    name="blaq",
    version="0.0.1",
    description="LogAnalytics queries collection for Bonsai",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(include=["blaq.*"]),
    license_files=('LICENSE.txt',),
    install_requires=[
        "azure-identity",
        "azure-monitor-query",
        "pandas>=1.3",
    ],
)
