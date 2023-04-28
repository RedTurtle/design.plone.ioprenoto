# -*- coding: utf-8 -*-
from datetime import date
from datetime import timedelta
from DateTime import DateTime
from dateutil import parser
from design.plone.ioprenoto.testing import (
    DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_PASSWORD
from plone.restapi.testing import RelativeSession

import transaction
import unittest


class TestPrenotazioniSearch(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        self.testing_fiscal_code = "TESTINGFISCALCODE"
        self.testing_booking_date = parser.parse("2023-04-28 16:00:00")

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
            week_table=[
                {
                    "day": "Lunedì",
                    "morning_start": "0700",
                    "morning_end": "1000",
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
                {
                    "day": "Martedì",
                    "morning_start": None,
                    "morning_end": None,
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
                {
                    "day": "Mercoledì",
                    "morning_start": None,
                    "morning_end": None,
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
                {
                    "day": "Giovedì",
                    "morning_start": None,
                    "morning_end": None,
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
                {
                    "day": "Venerdì",
                    "morning_start": None,
                    "morning_end": None,
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
                {
                    "day": "Sabato",
                    "morning_start": None,
                    "morning_end": None,
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
                {
                    "day": "Domenica",
                    "morning_start": None,
                    "morning_end": None,
                    "afternoon_start": None,
                    "afternoon_end": None,
                },
            ],
            booking_types=[
                {"name": "Type A", "duration": "30"},
            ],
            gates=["Gate A"],
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
        self.day_folder1 = api.content.create(
            container=week, type="PrenotazioniDay", title="Day"
        )
        self.day_folder2 = api.content.create(
            container=week, type="PrenotazioniDay", title="Day"
        )

        self.prenotazione_fscode = api.content.create(
            container=self.day_folder,
            type="Prenotazione",
            title="Prenotazione",
            fiscalcode=self.testing_fiscal_code,
        )
        self.prenotazione_no_fscode = api.content.create(
            container=self.day_folder,
            type="Prenotazione",
            title="Prenotazione",
        )
        self.prenotazione_datetime = api.content.create(
            container=self.day_folder,
            type="Prenotazione",
            title="Prenotazione",
            booking_date=DateTime(self.testing_booking_date.isoformat()),
            fiscalcode=self.testing_fiscal_code,
        )
        self.prenotazione_datetime_plus2 = api.content.create(
            container=self.day_folder1,
            type="Prenotazione",
            title="Prenotazione",
            booking_date=DateTime(
                (self.testing_booking_date + timedelta(days=2)).isoformat()
            ),
            fiscalcode=self.testing_fiscal_code,
        )
        self.prenotazione_datetime_plus4 = api.content.create(
            container=self.day_folder2,
            type="Prenotazione",
            title="Prenotazione",
            booking_date=DateTime(
                (self.testing_booking_date + timedelta(days=4)).isoformat()
            ),
            fiscalcode=self.testing_fiscal_code,
        )
        transaction.commit()

    def test_view_permission(self):
        self.assertEqual(
            self.api_session.get(
                f"{self.portal.absolute_url()}/@prenotazioni-search"
            ).status_code,
            200,
        )

        setRoles(self.portal, TEST_USER_ID, [])

        self.api_session.auth = (TEST_USER_ID, TEST_USER_PASSWORD)

        self.assertEqual(
            self.api_session.get(
                f"{self.portal.absolute_url()}/@prenotazioni-search"
            ).status_code,
            401,
        )

    def test_search_by_fiscalCode(self):
        result_uids = [
            i["UID"]
            for i in self.api_session.get(
                f"{self.portal.absolute_url()}/@prenotazioni-search?fiscalcode={self.testing_fiscal_code}&fullobjects=true"
            ).json()["items"]
        ]

        self.assertIn(self.prenotazione_fscode.UID(), result_uids)
        self.assertNotIn(self.prenotazione_no_fscode.UID(), result_uids)

    def test_search_by_date(self):
        # test by start date
        result_uids = [
            i["UID"]
            for i in self.api_session.get(
                f"{self.portal.absolute_url()}/@prenotazioni-search?start_date={str(self.testing_booking_date + timedelta(days=1))}&fiscalcode={self.testing_fiscal_code}&fullobjects=true"
            ).json()["items"]
        ]

        self.assertNotIn(self.prenotazione_datetime.UID(), result_uids)
        self.assertIn(self.prenotazione_datetime_plus2.UID(), result_uids)

        # test by end date
        result_uids = [
            i["UID"]
            for i in self.api_session.get(
                f"{self.portal.absolute_url()}/@prenotazioni-search?end_date={str(self.testing_booking_date + timedelta(days=3))}&fiscalcode={self.testing_fiscal_code}&fullobjects=true"
            ).json()["items"]
        ]

        self.assertIn(self.prenotazione_datetime_plus2.UID(), result_uids)
        self.assertNotIn(self.prenotazione_datetime_plus4.UID(), result_uids)

        # test btw strart and end date
        result_uids = [
            i["UID"]
            for i in self.api_session.get(
                f"{self.portal.absolute_url()}/@prenotazioni-search?start_date={str(self.testing_booking_date + timedelta(days=1))}&end_date={str(self.testing_booking_date + timedelta(days=3))}&fiscalcode={self.testing_fiscal_code}&fullobjects=true"
            ).json()["items"]
        ]

        self.assertIn(self.prenotazione_datetime_plus2.UID(), result_uids)
        self.assertNotIn(self.prenotazione_datetime_plus4.UID(), result_uids)
        self.assertNotIn(self.prenotazione_datetime.UID(), result_uids)
