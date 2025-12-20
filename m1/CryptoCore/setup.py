from setuptools import setup, find_packages

setup(
    name="cryptocore",
    version="1.0.0",
    description="Шифрование файлов AES-128 ECB с поддержкой русского текста",
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