from setuptools import setup, find_packages

setup(
    name="od_lib",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy==1.26.0",
        "pandas==2.1.2",
        "lxml==4.9.3",
        "regex==2023.10.3",
        "dicttoxml==1.7.4",
        "beautifulsoup4==4.12.2"
    ],
)
