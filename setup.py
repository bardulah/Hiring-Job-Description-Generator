"""
Setup configuration for Hiring System Generator.
"""

from setuptools import setup, find_packages

with open("README.v2.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hiring-system-generator",
    version="2.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Comprehensive system for generating job descriptions, hiring plans, and interview rubrics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Hiring-Job-Description-Generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Human Resources",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "spacy>=3.7.0",
        "nltk>=3.8.1",
        "pyyaml>=6.0.1",
        "python-multipart>=0.0.6",
        "markdown>=3.5",
        "reportlab>=4.0.0",
        "aiofiles>=23.2.1",
        "cachetools>=5.3.0",
        "python-dateutil>=2.8.2",
        "click>=8.1.7",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "httpx>=0.25.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "hiring-system=src.cli.interactive:cli",
            "hiring-api=src.api.server:main",
        ],
    },
)
