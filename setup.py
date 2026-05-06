from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="banking-pipeline",
    version="1.0.0",
    author="Rajput Suraj",
    author_email="suraj.rajput@example.com",
    description="A production-ready ETL pipeline for banking transactions with fraud detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rajputsuraj11/banking-pipeline",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=5.0.0",
            "black>=22.0.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
        ],
        "performance": [
            "memory-profiler>=0.60.0",
            "psutil>=5.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "banking-pipeline=src.main:run_pipeline",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
)
