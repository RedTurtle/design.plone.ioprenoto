
.. image:: https://img.shields.io/pypi/v/design.plone.ioprenoto.svg
    :target: https://pypi.org/project/design.plone.ioprenoto/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/design.plone.ioprenoto.svg?style=plastic
    :target: https://pypi.org/project/design.plone.ioprenoto/
    :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/dm/design.plone.ioprenoto.svg
    :target: https://pypi.org/project/design.plone.ioprenoto/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/pypi/l/design.plone.ioprenoto.svg
    :target: https://pypi.org/project/design.plone.ioprenoto/
    :alt: License

.. image:: https://github.com/RedTurtle/design.plone.ioprenoto/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/RedTurtle/design.plone.ioprenoto/actions
    :alt: Tests

.. image:: https://coveralls.io/repos/github/RedTurtle/design.plone.ioprenoto/badge.svg?branch=master
    :target: https://coveralls.io/github/RedTurtle/design.plone.ioprenoto?branch=master
    :alt: Coverage

=======================
Design Plone Io-Prenoto
=======================

This product is designed to integrate `redturtle.prenotazioni` package with `design.plone.contenttypes`

PrenotazioniFolder additional fields
====================================

There is a behavior that adds some additional fields:

- Uffici correlati
- Orario di apertura

Rest API
========

Servizio serializer
-------------------

There is a customization of Servizio serializer that adds an additional field:

- `referenced_by_prenotazioni_folder` which idicates if it has backreferences to PrenotazioniFolder 
  (design.plone.ioprenoto) throught correlated UO (with "Uffici correlati" field)

PrenotazioniFolder serializer
-----------------------------

There is a customization of PrenotazioniFolder serializer that redirects to '/prenotazione-appuntamenti-uffici'
if the user has not `design.plone.ioprenoto.ManagePrenotazioni`.

@bookable-uo-list
-----------------

Endpoint that returns a list of *UnitaOrganizzativa* contents that have at least one PrenotazioniFolder that 
relates to it (with "Uffici correlati" field).

Parameters:

- **uid**: The uid of a Servizio.

The endpoint can be called with a GET request::

   curl -i http://localhost:8080/Plone/@bookable-uo-list -H 'Accept: application/json'

Response::

    {
        "@id": "http://localhost:8080/Plone/@bookable-uo-list",
        "items": [
          {
            "@id": "...",
            "title": "...",
            "id": "...",
            "prenotazioni_folder": [
              {
                "@id": "http://localhost:8080/Plone/prenotazioni-folder",
                "address": {
                  "@id": "http://localhost:8080/Plone/a-venue",
                  "@type": "Venue",
                  "city": "Ferrara",
                  "geolocation": {
                    "latitude": 1111,
                    "longitude": 2222,
                  },
                  ...
                }
              }
            ],
          }
        ]
    }

If uid parameter is passed, only UnitaOrganizzative related to that Servizio (with *canale_fisico* relation field) will be returned.

@bookable-list
--------------

Endpoint that returns a list of *Bookable*.

The endpoint can be called with a GET request::

   curl -i http://localhost:8080/Plone/@bookable-list -H 'Accept: application/json'

Response::

    {
        "@id": "http://localhost:8080/Plone/@bookable-list",
        "items": [
          {
            "@id": "...",
            "title": "...",
            "url": "...",
            "booking_types": [],
          }
        ]
    }


Installation
============

Install design.plone.ioprenoto by adding it to your buildout::

    [buildout]

    ...

    eggs =
        design.plone.ioprenoto


and then running `bin/buildout`

Contribute
==========

- Issue Tracker: https://github.com/RedTurtle/design.plone.ioprenoto/issues
- Source Code: https://github.com/RedTurtle/design.plone.ioprenoto


Notes
=====

**design.plone.ioprenoto** has been tested with Plone 6 and works with Python 3.

Authors
=======

This product was developed by **RedTurtle Technology** team.

.. image:: https://avatars1.githubusercontent.com/u/1087171?s=100&v=4
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/

