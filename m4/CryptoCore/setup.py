from setuptools import setup, find_packages

setup(
    name="cryptocore",
    version="0.4.0",  # Updated for Sprint 4
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'cryptocore=cryptocore.main:main',
        ],
    },
    description="Cryptographic toolkit with encryption and hashing capabilities",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
)