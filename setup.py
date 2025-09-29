import os
import setuptools

# Lire le README pour la description longue
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tassi",
    version="1.0.0",
    author="Tassi Team",
    author_email="dev@tassi.com",
    description="SDK Python officiel pour l'API Tassi - Solution de logistique et d'expédition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tassi-pro/tassi-python",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "inflection>=0.5.0"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "responses>=0.18.0",
            "black>=21.0.0",
            "flake8>=3.8.0"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Shipping",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    keywords="tassi shipping logistics api sdk python",
    project_urls={
        "Bug Reports": "https://github.com/Tassi-pro/tassi-python/issues",
        "Source": "https://github.com/Tassi-pro/tassi-python",
        "Documentation": "https://docs.tassi.com",
    },
)