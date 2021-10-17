"""
Installation script for this package
"""

from setuptools import setup, find_packages

setup(
    name='mtg-mana-simulator',
    version='0.2',
    url='https://github.com/TiesWestendorp/MTG-Mana-Simulator',
    author='Ties Westendorp',
    packages=find_packages(include=['mtg_mana_simulator', 'mtg_mana_simulator.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
