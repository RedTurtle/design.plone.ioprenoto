from copy import deepcopy
from datetime import date
from datetime import datetime
from datetime import timedelta
from design.plone.ioprenoto.testing import DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from plone.restapi.testing import RelativeSession
from transaction import commit
from z3c.relationfield.relation import RelationValue
from zope.component import queryUtility
from zope.intid.interfaces import IIntIds

import unittest


class TestBookingInfo(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING
    maxDiff = None

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        self.today = datetime.now()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.venue = api.content.create(
            container=self.portal,
            title="Example venue",
            type="Venue",
            city="Ferrara",
            country="380",
            street="Foo Street 22",
        )
        self.unita_organizzativa = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO",
            sede=[RelationValue(to_id=queryUtility(IIntIds).getId(self.venue))],
        )
        self.unita_organizzativa2 = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO 2",
        )
        self.unita_organizzativa3 = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO 3",
        )

        self.prenotazioni_folder = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Prenotazioni Folder",
            orario_di_apertura="foo",
            descriptionAgenda=RichTextValue(
                "<h1>description agenda</h1>",
                "text/html",
                "text/html",
            ),
            gates=["Gate A"],
            uffici_correlati=[
                RelationValue(
                    to_id=queryUtility(IIntIds).getId(self.unita_organizzativa)
                )
            ],
        )
        week_table = deepcopy(self.prenotazioni_folder.week_table)
        for day in week_table:
            day["morning_start"] = "0700"
            day["morning_end"] = "1300"
        self.prenotazioni_folder.week_table = week_table

        api.content.transition(
            obj=api.content.create(
                type="PrenotazioneType",
                title="Type A",
                duration=30,
                container=self.prenotazioni_folder,
                gates=["all"],
            ),
            transition="publish",
        )

        # self.prenotazioni_folder2 = api.content.create(
        #     container=self.portal,
        #     type="PrenotazioniFolder",
        #     title="Prenotazioni Folder 2",
        #     uffici_correlati=[
        #         RelationValue(
        #             to_id=queryUtility(IIntIds).getId(self.unita_organizzativa)
        #         )
        #     ],
        # )
        # api.content.transition(
        #     obj=api.content.create(
        #         type="PrenotazioneType",
        #         title="Type A",
        #         duration=10,
        #         container=self.prenotazioni_folder2,
        #         gates=["all"],
        #     ),
        #     transition="publish",
        # )
        # api.content.transition(
        #     obj=api.content.create(
        #         type="PrenotazioneType",
        #         title="Type B",
        #         duration=30,
        #         container=self.prenotazioni_folder2,
        #         gates=["all"],
        #     ),
        #     transition="publish",
        # )
        # self.prenotazioni_folder3 = api.content.create(
        #     container=self.portal,
        #     type="PrenotazioniFolder",
        #     title="Prenotazioni Folder 3",
        #     uffici_correlati=[
        #         RelationValue(
        #             to_id=queryUtility(IIntIds).getId(self.unita_organizzativa2)
        #         )
        #     ],
        # )

        # self.prenotazioni_folder4 = api.content.create(
        #     container=self.portal,
        #     type="PrenotazioniFolder",
        #     title="Prenotazioni Folder 4",
        # )

        # self.servizio = api.content.create(
        #     container=self.portal,
        #     type="Servizio",
        #     title="Servizio",
        #     canale_fisico=[
        #         RelationValue(
        #             to_id=queryUtility(IIntIds).getId(self.unita_organizzativa)
        #         )
        #     ],
        # )

        # booker = IBooker(self.prenotazioni_folder)
        # self.prenotazione1 = booker.book(
        #     {
        #         "booking_date": self.today.replace(hour=8, minute=0),
        #         "booking_type": "Type A",
        #         "title": "foo",
        #         "other_fields": {
        #             "booking_office": self.unita_organizzativa.absolute_url(),
        #             "booking_address": self.venue.absolute_url(),
        #         },
        #     }
        # )
        commit()

    def test_get_bookings(self):
        booking_date = "{}T10:00:00+00:00".format(
            (date.today() + timedelta(3)).strftime("%Y-%m-%d")
        )
        res = self.api_session.post(
            self.prenotazioni_folder.absolute_url() + "/@booking",
            json={
                "booking_date": booking_date,
                "booking_type": "Type A",
                "other_fields": {
                    "booking_office": self.unita_organizzativa.absolute_url(),
                    "booking_address": self.venue.absolute_url(),
                },
                "fields": [
                    {"name": "title", "value": "Mario Rossi"},
                    {"name": "email", "value": "mario.rossi@example"},
                    {"name": "description", "value": "foo"},
                ],
            },
        )
        self.assertEqual(res.status_code, 200)
        booking = res.json()
        self.assertIn("@id", booking)
        self.assertEqual(booking["id"], "mario-rossi")
        self.assertEqual(
            booking["booking_folder"]["@id"],
            self.prenotazioni_folder.absolute_url(),
        )
        self.assertEqual(booking["booking_address"]["@id"], self.venue.absolute_url())
        self.assertEqual(
            booking["booking_office"]["@id"],
            self.unita_organizzativa.absolute_url(),
        )

        res = self.api_session.get(
            self.portal.absolute_url()
            + "/@bookings?fullobjects=1&from=2000-01-01T00:00:00"
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["items"]), 1)
        booking_info = res.json()["items"][0]
        self.assertIn("@id", booking_info)
        self.assertEqual(
            booking_info["booking_folder"]["@id"],
            self.prenotazioni_folder.absolute_url(),
        )
        self.assertEqual(
            booking_info["booking_address"]["@id"], self.venue.absolute_url()
        )
        self.assertEqual(
            booking_info["booking_office"]["@id"],
            self.unita_organizzativa.absolute_url(),
        )

        # TODO: andrebbe messo lo UID anche su booking_id visto che è l'attributo conosciuto come identificativo
        res = self.api_session.get(
            self.portal.absolute_url() + f"/@booking/{booking['UID']}"
        )
        booking_info = res.json()
        # self.assertEqual(booking_info["@type"], "Prenotazione")
        self.assertEqual(
            booking_info["booking_folder"]["@id"],
            self.prenotazioni_folder.absolute_url(),
        )
        self.assertEqual(
            booking_info["booking_address"]["@id"], self.venue.absolute_url()
        )
        self.assertEqual(
            booking_info["booking_office"]["@id"],
            self.unita_organizzativa.absolute_url(),
        )
        self.assertEqual(
            booking_info["notify_on_confirm"],
            False,
        )
