# -*- coding: utf-8 -*-
from datetime import date
from design.plone.ioprenoto.testing import DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import (
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
    TEST_USER_ID,
    setRoles,
)
from plone.restapi.testing import RelativeSession
from plone.restapi.serializer.converters import json_compatible

import unittest
import transaction


class TestBookingSchema(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING
    maxDiff = None

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

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
            required_booking_fields=["email", "fiscalcode"],
        )
        week_table = self.folder_prenotazioni.week_table
        week_table[0]["morning_start"] = "0700"
        week_table[0]["morning_end"] = "1000"
        self.folder_prenotazioni.week_table = week_table

        year = api.content.create(
            container=self.folder_prenotazioni, type="PrenotazioniYear", title="Year"
        )
        week = api.content.create(container=year, type="PrenotazioniWeek", title="Week")
        self.day_folder = api.content.create(
            container=week, type="PrenotazioniDay", title="Day"
        )
        transaction.commit()

    def tearDown(self):
        self.api_session.close()

    def test_booking_schema_description_always_required(
        self,
    ):
        now = date.today()
        current_year = now.year
        sunday = 6
        current_month = now.month

        response = self.api_session.get(
            "{}/@booking-schema?booking_date={}+10%3A00".format(
                self.folder_prenotazioni.absolute_url(),
                json_compatible(date(current_year, current_month, sunday)),
            ),
        )

        self.assertEqual(response.json()["fields"][1]["name"], "description")
        self.assertTrue(response.json()["fields"][1]["required"])
