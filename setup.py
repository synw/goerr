from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

version = "0.11.0"

setup(
    name="goerr",
    packages=find_packages(),
    version=version,
    description="Go style explicit errors handling",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="synw",
    author_email="synwe@yahoo.com",
    url="https://github.com/synw/goerr",
    download_url="https://github.com/synw/goerr/releases/tag/" + version,
    keywords=["errors", "error_handling"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    zip_safe=False,
)
