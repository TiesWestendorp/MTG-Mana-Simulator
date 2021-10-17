"""
Installation script for this package
"""

from setuptools import setup, find_packages

setup(
    name='mtg-mana-simulator',
    version='0.1',
    url='https://github.com/TiesWestendorp/MTG-Mana-Simulator',
    author='Ties Westendorp',
    py_modules=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
