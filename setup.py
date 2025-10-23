#!/usr/bin/env python3
"""
Setup script para o Listador de Licitações PNCP
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pncp-licitacoes",
    version="1.0.0",
    author="Thiago",
    author_email="",
    description="Script Python para listar licitações do Portal Nacional de Contratações Públicas (PNCP)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Thiag086/Licita-oes_geral",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pncp-licitacoes=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)