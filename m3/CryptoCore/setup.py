from setuptools import setup, find_packages

setup(
    name="cryptocore",
    version="2.0.0",
    description="Шифрование файлов AES с поддержкой режимов ECB, CBC, CFB, OFB, CTR",
    author="Разработчик",
    packages=find_packages(),
    install_requires=[
        "pycryptodome>=3.10.0",
    ],
    entry_points={
        "console_scripts": [
            "cryptocore=cryptocore.main:main",
        ],
    },
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)