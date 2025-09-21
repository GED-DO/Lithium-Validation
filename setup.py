from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Lithium-Validation",
    version="2.0.0",  # Updated for automatic validation
    author="Guillermo Espinosa",
    author_email="hola@ged.do",
    description="Automatic AI output validation with zero configuration - detects content type and validates intelligently",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GED-DO/Lithium-Validation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",  # Updated from Beta
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "mcp>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "notebooks": [
            "jupyter>=1.0.0",
            "matplotlib>=3.5.0",
            "pandas>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "lithium-validate=lithium_validation.cli.validate:main",
            "lithium-report=lithium_validation.cli.validate:report",
            "lithium-auto=lithium_validation.cli.auto:main",  # New auto CLI
        ],
    },
    include_package_data=True,
    package_data={
        "lithium_validation": [
            "config/*.json",
            "mcp/*.py",
        ],
    },
    keywords="ai validation llm hallucination detection automatic zero-config claude anthropic mcp consulting framework McKinsey BCG Bain",
    project_urls={
        "Bug Reports": "https://github.com/GED-DO/Lithium-Validation/issues",
        "Source": "https://github.com/GED-DO/Lithium-Validation",
        "Documentation": "https://github.com/GED-DO/Lithium-Validation/blob/main/README.md",
    },
)
