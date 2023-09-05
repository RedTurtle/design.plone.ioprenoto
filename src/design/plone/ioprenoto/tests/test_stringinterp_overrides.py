# -*- coding: utf-8 -*-
from datetime import date
from plone import api
from plone.app.testing import (
    TEST_USER_ID,
    setRoles,
)
from design.plone.ioprenoto.testing import (
    DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING,
)
from datetime import datetime
from plone.registry.interfaces import IRegistry
from plone.stringinterp.interfaces import IStringSubstitution
from plone.stringinterp.interfaces import IContextWrapper
from plone.volto.interfaces import IVoltoSettings
from redturtle.prenotazioni.adapters.booker import IBooker
from zope.component import getAdapter
from zope.component import getUtility

import unittest
import transaction


class TestStringinterpOverrides(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.folder_prenotazioni = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Prenota foo",
            description="",
            daData=date.today(),
            booking_types=[
                {"name": "Type A", "duration": "30"},
            ],
            gates=["Gate A"],
        )
        week_table = self.folder_prenotazioni.week_table
        week_table[0]["morning_start"] = "0700"
        week_table[0]["morning_end"] = "1000"
        self.folder_prenotazioni.week_table = week_table

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
        self.prenotazione = booker.create(
            {
                "booking_date": datetime.now(),
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
