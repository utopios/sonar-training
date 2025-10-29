"""Setup configuration for the project."""

from setuptools import setup, find_packages

# Read long description from README
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Python project with SonarQube integration"

setup(
    name="my-python-project",  # Change this to your project name
    version="0.1.0",
    author="Your Name",  # Change this
    author_email="your.email@example.com",  # Change this
    description="A short description of your project",  # Change this
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/yourproject",  # Change this

    # Package configuration
    packages=find_packages(where="src"),
    package_dir={"": "src"},

    # Python version requirement
    python_requires=">=3.8",

    # Dependencies
    install_requires=[
        # Add your production dependencies here
        # Example:
        # "requests>=2.31.0",
        # "flask>=3.0.0",
    ],

    # Development dependencies
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "pylint>=2.17.0",
            "mypy>=1.4.0",
        ],
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },

    # Classifiers for PyPI
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # Entry points (if you have CLI commands)
    # entry_points={
    #     "console_scripts": [
    #         "mycommand=src.app.main:main",
    #     ],
    # },
)
