from setuptools import setup, find_packages

version = "0.9.4"

setup(
    name='goerr',
    packages=find_packages(),
    version=version,
    description='Go style explicit errors handling',
    author='synw',
    author_email='synwe@yahoo.com',
    url='https://github.com/synw/goerr',
    download_url='https://github.com/synw/goerr/releases/tag/' + version,
    keywords=['errors', "error_handling"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    zip_safe=False
)
