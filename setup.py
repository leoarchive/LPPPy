#!/usr/bin/env python3
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text('utf-8')

setup(
    name="LPPPy",
    version='0.1.0',
    description="A compiler to Python of Manzano's LPP",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/leozamboni/LPPPy",
    author="Zamboni Leonardo",
    author_email="leonardonunes169@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=['lpppy'],
    package_dir={'lpppy': 'lpppy'},
    package_data={'lpppy': ['lpppy/compiler/*']},
    include_package_data=True,
    install_requires=[
        # Universal dependencies
        'setuptools',
    ],
    entry_points={
        "console_scripts": [
            "lpppy=lpppy.main:LPP",
        ]
    },
)