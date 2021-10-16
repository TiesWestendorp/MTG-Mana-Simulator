"""
Installation script for this package
"""

from setuptools import setup, find_packages
from mtg_mana_simulator import __version__

setup(
    name='mtg-mana-simulator',
    version=__version__,
    url='https://github.com/TiesWestendorp/MTG-Mana-Simulator',
    author='Ties Westendorp',
    py_modules=find_packages(),
)
