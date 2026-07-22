from setuptools import find_packages, setup

setup(
    name="StepDistanceCalculator",
    version="1.0.0",
    description="Calculate walking step counts between places or cities based on total distance and step length.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="StepDistanceCalculator Team",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "matplotlib>=3.7.0",
        "fpdf2>=2.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "stepdistance=stepdistance.cli:main",
        ],
    },
)
