import os
import setuptools

# Lire les dépendances depuis requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

# Lire le README pour la description longue
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mon-sdk",
    version="0.1.0",
    author="Votre Nom",
    author_email="votre.email@example.com",
    description="Description courte de votre SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/votre-username/mon-sdk-python",
    packages=setuptools.find_packages(),
    install_requires=required,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)