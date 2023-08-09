# -*- coding: utf-8 -*-
from datetime import date
from datetime import timedelta
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from redturtle.prenotazioni.testing import (
    REDTURTLE_PRENOTAZIONI_API_FUNCTIONAL_TESTING,
)

import unittest
import transaction


class TestPrenotazioniRestAPIAdd(unittest.TestCase):
    layer = REDTURTLE_PRENOTAZIONI_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal_url = self.portal.absolute_url()
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
        for row in week_table:
            row["morning_start"] = "0700"
            row["morning_end"] = "1000"
        self.folder_prenotazioni.week_table = week_table
        api.content.transition(obj=self.folder_prenotazioni, transition="publish")
        transaction.commit()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})

    def test_description_required_validation(self):
        self.api_session.auth = None
        booking_date = "{}T09:00:00+00:00".format(
            (date.today() + timedelta(1)).strftime("%Y-%m-%d")
        )
        res = self.api_session.post(
            self.folder_prenotazioni.absolute_url() + "/@booking",
            json={
                "booking_date": booking_date,
                "booking_type": "Type A",
                "fields": [
                    {"name": "title", "value": "Mario Rossi"},
                    {"name": "email", "value": "mario.rossi@example"},
                ],
            },
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            res.json()["message"], "Required input 'description' is missing."
        )

    def test_add(self):
        self.api_session.auth = None
        booking_date = "{}T09:00:00+00:00".format(
            (date.today() + timedelta(1)).strftime("%Y-%m-%d")
        )
        res = self.api_session.post(
            self.folder_prenotazioni.absolute_url() + "/@booking",
            json={
                "booking_date": booking_date,
                "booking_type": "Type A",
                "fields": [
                    {"name": "title", "value": "Mario Rossi"},
                    {"name": "email", "value": "mario.rossi@example"},
                    {"name": "description", "value": "foo"},
                ],
            },
        )
        self.assertEqual(res.status_code, 200)
