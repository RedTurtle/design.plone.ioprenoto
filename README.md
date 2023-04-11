![Latest Version](https://img.shields.io/pypi/v/design.plone.ioprenoto.svg)
![Supported - Python Versions](hhttps://img.shields.io/pypi/pyversions/design.plone.ioprenoto.svg?style=plastic)
![Number of PyPI downloads](https://img.shields.io/pypi/dm/design.plone.ioprenoto.svg)
![License](https://img.shields.io/pypi/l/design.plone.ioprenoto.svg)
![Tests](https://github.com/RedTurtle/design.plone.ioprenoto/actions/workflows/tests.yml/badge.svg)
![Coverage](https://coveralls.io/repos/github/RedTurtle/design.plone.ioprenoto/badge.svg?branch=master)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [design.plone.ioprenoto](#designploneioprenoto)
- [Features](#features)
  - [Behaviors attached to PrenotazioniFolder c.t.(redturtle.prenotazioni):](#behaviors-attached-to-prenotazionifolder-ctredturtleprenotazioni)
  - [Serializer of Servizio c.t.(design.plone.contenttypes) has additional filelds:](#serializer-of-servizio-ctdesignplonecontenttypes-has-additional-filelds)
  - [RestAPI GET of PrenotazioniFolder c.t.(redturtle.prenotazioni) returns redirect to '/prenotazione-appuntamento'(which defined in redturtle.prenotazioni)](#restapi-get-of-prenotazionifolder-ctredturtleprenotazioni-returns-redirect-to-prenotazione-appuntamentowhich-defined-in-redturtleprenotazioni)
- [Documentation](#documentation)
- [Installation](#installation)
- [Authors](#authors)
- [Contributors](#contributors)
- [Contribute](#contribute)
- [Support](#support)
- [License](#license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

design.plone.ioprenoto
======================
This product is designed to integrate `redturtle.prenotazioni` package with `design.plone.contenttypes`

# Features

## Behaviors attached to PrenotazioniFolder c.t.(redturtle.prenotazioni):
- Uffici correlati
- Punto di contatto correlato
- Orario di apertura

## Serializer of Servizio c.t.(design.plone.contenttypes) has additional filelds:
- `referenced_by_prenotazioni_folder` which idicates if it has a PrenotazioniFolder c.t.(redturtle.prenotazioni) object
between childs.

## RestAPI GET of PrenotazioniFolder c.t.(redturtle.prenotazioni) returns redirect to '/prenotazione-appuntamento'(which defined in redturtle.prenotazioni)
if the user has not edturtle.prenotazioni.ManagePrenotazioni permission which is attached to Manager SiteAdministrator and Editor roles by this add-on.


# Documentation

Not provided yet

# Installation

Install design.plone.ioprenoto by adding it to your buildout::

    [buildout]

    ...

    eggs =
        design.plone.ioprenoto


and then running ``bin/buildout``

# Authors

<a href="http://www.redturtle.it/" rel="RedTurtle Technology Site">![RedTurtle Technology Site](https://avatars1.githubusercontent.com/u/1087171?s=100&v=4)</a>

# Contributors

Put your name here, you deserve it!

- foxtrot-dfm1

# Contribute

- Issue Tracker: https://github.com/collective/design.plone.ioprenoto/issues
- Source Code: https://github.com/collective/design.plone.ioprenoto

# Support

If you are having issues, please let us know.
We have a mailing list located at: info@redturtle.it

# License

The project is licensed under the GPLv2.
