# -*- coding: utf-8 -*-
import unittest
from datetime import datetime

import transaction
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.registry.interfaces import IRegistry
from plone.stringinterp.interfaces import IContextWrapper, IStringSubstitution
from plone.volto.interfaces import IVoltoSettings
from redturtle.prenotazioni.adapters.booker import IBooker
from redturtle.prenotazioni.tests.helpers import WEEK_TABLE_SCHEMA
from z3c.relationfield.relation import RelationValue
from zope.component import getAdapter, getUtility, queryUtility
from zope.intid.interfaces import IIntIds

from design.plone.ioprenoto.testing import DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING


class TestStringinterp(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.today = datetime.now()

        self.unita_organizzativa = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO",
        )
        self.servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Servizio",
            ufficio_responsabile=[
                RelationValue(
                    to_id=queryUtility(IIntIds).getId(self.unita_organizzativa)
                )
            ],
        )
        self.folder_prenotazioni = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Prenota foo",
            description="",
            daData=self.today.date(),
            gates=["Gate A"],
            uffici_correlati=[
                RelationValue(
                    to_id=queryUtility(IIntIds).getId(self.unita_organizzativa)
                )
            ],
            week_table=WEEK_TABLE_SCHEMA,
        )
        api.content.transition(
            obj=api.content.create(
                type="PrenotazioneType",
                title="Type A",
                duration=30,
                container=self.folder_prenotazioni,
                gates=["all"],
            ),
            transition="publish",
        )

        year = api.content.create(
            container=self.folder_prenotazioni,
            type="PrenotazioniYear",
            title="Year",
        )
        week = api.content.create(container=year, type="PrenotazioniWeek", title="Week")
        self.day_folder = api.content.create(
            container=week, type="PrenotazioniDay", title="Day"
        )

        booker = IBooker(self.folder_prenotazioni)
        self.prenotazione = booker.book(
            {
                "booking_date": self.today.replace(hour=8, minute=0),
                "booking_type": "Type A",
                "title": "foo",
            }
        )

        transaction.commit()

    def test_booking_print_url_override(
        self,
    ):
        self.assertEqual(
            getAdapter(
                IContextWrapper(self.prenotazione),
                IStringSubstitution,
                "booking_print_url",
            )(),
            f"{self.portal_url}/prenotazione-appuntamenti-uffici?booking_id={self.prenotazione.UID()}",
        )

    def test_booking_print_url_with_delete_token_override(
        self,
    ):
        self.assertEqual(
            getAdapter(
                IContextWrapper(self.prenotazione),
                IStringSubstitution,
                "booking_print_url_with_delete_token",
            )(),
            f"{self.portal_url}/prenotazione-appuntamenti-uffici?booking_id={self.prenotazione.UID()}",
        )

    def test_booking_operator_url_override(self):
        self.assertEqual(
            getAdapter(
                self.prenotazione, IStringSubstitution, "booking_operator_url"
            )(),
            f"{self.portal_url}/prenota-foo?tab=search&SearchableText={self.prenotazione.getBookingCode()}&login=1",
        )

    def test_booking_print_url_override_with_custom_frontend_domain(
        self,
    ):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IVoltoSettings, prefix="volto", check=False)
        settings.frontend_domain = "http://foo.bar"

        self.assertEqual(
            getAdapter(
                IContextWrapper(self.prenotazione),
                IStringSubstitution,
                "booking_print_url",
            )(),
            f"http://foo.bar/prenotazione-appuntamenti-uffici?booking_id={self.prenotazione.UID()}",
        )

    def test_unita_organizzativa_title(self):
        self.assertEqual(
            getAdapter(
                self.prenotazione, IStringSubstitution, "unita_organizzativa_title"
            )(),
            self.unita_organizzativa.Title(),
        )
