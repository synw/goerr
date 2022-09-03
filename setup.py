from setuptools import setup, find_packages

version = "0.10.0"

setup(
    name="goerr",
    packages=find_packages(),
    version=version,
    description="Go style explicit errors handling",
    author="synw",
    author_email="synwe@yahoo.com",
    url="https://github.com/synw/goerr",
    download_url="https://github.com/synw/goerr/releases/tag/" + version,
    keywords=["errors", "error_handling"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
    ],
    zip_safe=False,
)
