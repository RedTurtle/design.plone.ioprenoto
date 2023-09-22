# -*- coding: utf-8 -*-
"""Installer for the design.plone.ioprenoto package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="design.plone.ioprenoto",
    version="1.1.6",
    description="An add-on for Plone",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Development Status :: 5 - Production/Stable",
    ],
    keywords="Python Plone CMS",
    author="RedTurtle",
    author_email="info@redturtle.it",
    url="https://github.com/RedTurtle/design.plone.ioprenoto",
    project_urls={
        "PyPI": "https://pypi.org/project/design.plone.ioprenoto/",
        "Source": "https://github.com/RedTurtle/design.plone.ioprenoto",
        "Tracker": "https://github.com/RedTurtle/design.plone.ioprenoto/issues",
        # 'Documentation': 'https://design.plone.ioprenoto.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["design", "design.plone"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "z3c.jbot",
        "plone.api>=1.8.4",
        "plone.app.dexterity",
        "redturtle.prenotazioni>=2.0.0.rc2",
        "design.plone.policy",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
            "collective.MockMailHost",
            "redturtle.prenotazioni[test]",
            "design.plone.policy[test]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = design.plone.ioprenoto.locales.update:update_locale
    """,
)
