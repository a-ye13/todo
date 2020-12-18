"""
Todolist python package configuration.

Austin Ye
"""

from setuptools import setup

setup(
    name='todolist',
    version='0.1.0',
    packages=['todolist'],
    include_package_data=True,
    install_requires=[
        'arrow',
        'bs4',
        'Flask',
        'requests',
    ],
    python_requires='>=3.6',
)
