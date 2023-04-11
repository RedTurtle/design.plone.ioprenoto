.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

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

======================
design.plone.ioprenoto
======================

This product is designed to integrate `redturtle.prenotazioni` package with `design.plone.contenttypes`

Features
--------

* Behaviors attached to PrenotazioniFolder c.t.(redturtle.prenotazioni):
  - Uffici correlati
  - Punto di contatto correlato
  - Orario di apertura

* Serializer of Servizio c.t.(design.plone.contenttypes) has additional filelds:
  - `referenced_by_prenotazioni_folder` which idicates if it has a PrenotazioniFolder c.t.(redturtle.prenotazioni) object
    between childs.

* RestAPI GET of PrenotazioniFolder c.t.(redturtle.prenotazioni) returns redirect to
`/prenotazione-appuntamento`(which defined in redturtle.prenotazioni) if the user has not edturtle.prenotazioni.ManagePrenotazioni
permission which is attached to Manager SiteAdministrator and Editor roles by this add-on.


Documentation
-------------

Full documentation for end users can be found in the "docs" folder



Installation
------------

Install design.plone.ioprenoto by adding it to your buildout::

    [buildout]

    ...

    eggs =
        design.plone.ioprenoto


and then running ``bin/buildout``


Authors
-------

RedTurtle

Contributors
------------

Put your name here, you deserve it!

- foxtrot-dfm1


Contribute
----------

- Issue Tracker: https://github.com/collective/design.plone.ioprenoto/issues
- Source Code: https://github.com/collective/design.plone.ioprenoto


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: info@redturtle.it


License
-------

The project is licensed under the GPLv2.
