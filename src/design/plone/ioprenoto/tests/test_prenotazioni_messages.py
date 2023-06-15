# -*- coding: utf-8 -*-
from design.plone.ioprenoto.testing import DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from transaction import commit
from redturtle.prenotazioni.adapters.booker import IBooker
from z3c.relationfield.relation import RelationValue
from zope.component import queryUtility
from zope.event import notify
from zope.intid.interfaces import IIntIds
from zope.component import getMultiAdapter
from zope.lifecycleevent import ObjectModifiedEvent
from datetime import date
from datetime import datetime
from zope.globalrequest import getRequest

import calendar
import transaction
import unittest

try:
    from design.plone.iocittadino.interfaces.store import (
        IPraticaContentStore,
        IMessageContentStore,
    )
    iocittadino_installed = True
except ImportError as e:
    iocittadino_installed = False

@unittest.skipIf(not iocittadino_installed, 'design.plone.iocittadino is not installed')
class TestPrenotazioniMessages(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING

    def setUp(self):
        # use design.plone.iocittadino(private package) store here 
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

        self.message_store = getMultiAdapter((self.portal, self.request), IMessageContentStore)

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
        now = date.today()
        current_year = now.year
        current_month = now.month
        current_day = now.day
        monday = 0

        # get next monday
        found = False
        while not found:
            for week in calendar.monthcalendar(current_year, current_month):
                # week[0] is monday and should be greater than today
                if week[0] > current_day:
                    monday = week[0]
                    found = True
                    break

            if monday == 0:
                current_month += 1
                current_day = 1
        # create a placeholder for first available monday

        self.assertEqual(self.message_store.length, 0)

        booking = self.booker.create(
            {
                "booking_date": datetime(current_year, current_month, monday, 7, 0),
                "booking_type": "Type A",
                "title": "foo",
            }
        )

        self.assertEqual(self.message_store, 1)
