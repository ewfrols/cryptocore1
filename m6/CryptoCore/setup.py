from setuptools import setup, find_packages

setup(
    name="cryptocore",
    version="0.6.0",
    packages=find_packages(),
    install_requires=[
        'cryptography>=41.0.0',
    ],
    entry_points={
        'console_scripts': [
            'cryptocore=cryptocore.main:main',
        ],
    },
    author="CryptoCore Team",
    description="Educational cryptographic toolkit with full implementations",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)