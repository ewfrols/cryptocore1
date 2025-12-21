from setuptools import setup, find_packages

setup(
    name="cryptocore",
    version="0.5.0",
    packages=find_packages(include=['cryptocore', 'cryptocore.*']),
    package_dir={'': '.'},
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'cryptocore=cryptocore.main:main',
        ],
    },
    description="Cryptographic toolkit with encryption, hashing, and MAC capabilities",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
    ],
    python_requires='>=3.6',
)