from setuptools import setup, find_packages

setup(
    name="Topsis-Simanta-102483083",
    version="1.0.0",
    author="Simanta",
    author_email="ssaha_be23@thapar.edu",
    description="A simple package for TOPSIS implementation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'topsis=topsis_pkg.topsis:main',
        ],
    },
    python_requires='>=3.6',
)