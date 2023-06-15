# -*- coding: utf-8 -*-
from design.plone.ioprenoto.testing import DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from redturtle.prenotazioni.adapters.booker import IBooker
from zope.component import getMultiAdapter
from datetime import date
from datetime import datetime, timedelta

import transaction
import unittest

try:
    from design.plone.iocittadino.interfaces.store import (
        IMessageContentStore,
    )

    iocittadino_installed = True
except ImportError:
    iocittadino_installed = False


@unittest.skipIf(not iocittadino_installed, "design.plone.iocittadino is not installed")
class TestPrenotazioniMessages(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_FUNCTIONAL_TESTING

    def setUp(self):
        # use design.plone.iocittadino(private package) store here
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

        self.message_store = getMultiAdapter(
            (self.portal, self.request), IMessageContentStore
        )

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        api.user.create(
            email="user@example.com",
            username="user",
            password="secret!!!",
        )
        api.user.create(
            email="user@example.com",
            username="user2",
            password="secret!!!",
        )

        self.portal_url = self.portal.absolute_url()
        self.folder_prenotazioni = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Folder",
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

        self.view = api.content.get_view(
            name="confirm-delete",
            context=self.folder_prenotazioni,
            request=self.request,
        )
        self.booker = IBooker(self.folder_prenotazioni)
        self.today = datetime.now().replace(hour=8)

        api.content.transition(obj=self.folder_prenotazioni, transition="publish")
        transaction.commit()

    def tearDown(self):
        self.message_store.clear()

    def test_message_created(
        self,
    ):
        self.booker.create(
            {
                "booking_date": self.today + timedelta(1),  # tomorrow
                "booking_type": "Type A",
                "title": "foo",
            }
        )

        self.assertEqual(self.message_store.length, 1)
