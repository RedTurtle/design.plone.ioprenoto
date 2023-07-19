# -*- coding: utf-8 -*-
from design.plone.ioprenoto.testing import DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.testing import RelativeSession
from transaction import commit
from z3c.relationfield.relation import RelationValue
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.intid.interfaces import IIntIds
from plone.app.textfield.value import RichTextValue

import unittest


class BookableUOListTest(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING
    maxDiff = None

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()

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
            uffici_correlati=[
                RelationValue(
                    to_id=queryUtility(IIntIds).getId(self.unita_organizzativa)
                )
            ],
            booking_types=[
                {"name": "Type A", "duration": "30"},
            ],
        )
        self.prenotazioni_folder2 = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Prenotazioni Folder 2",
            uffici_correlati=[
                RelationValue(
                    to_id=queryUtility(IIntIds).getId(self.unita_organizzativa)
                )
            ],
            booking_types=[
                {"name": "Type A", "duration": "10"},
                {"name": "Type B", "duration": "30"},
            ],
        )
        self.prenotazioni_folder3 = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Prenotazioni Folder 3",
            uffici_correlati=[
                RelationValue(
                    to_id=queryUtility(IIntIds).getId(self.unita_organizzativa2)
                )
            ],
        )

        self.prenotazioni_folder4 = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Prenotazioni Folder 4",
        )

        self.servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Servizio",
            canale_fisico=[
                RelationValue(
                    to_id=queryUtility(IIntIds).getId(self.unita_organizzativa)
                )
            ],
        )

        commit()

    def tearDown(self):
        self.api_session.close()

    def test_endpoint_return_all_uo_with_related_folder_prenotazioni(self):
        resp = self.api_session.get(f"{self.portal_url}/@bookable-uo-list").json()

        self.assertEqual(len(resp["items"]), 2)
        uo_titles = [x["title"] for x in resp["items"]]
        self.assertIn(self.unita_organizzativa.title, uo_titles)
        self.assertIn(self.unita_organizzativa2.title, uo_titles)

        # this one does not have a related folder prenotazioni
        self.assertNotIn(self.unita_organizzativa3.title, uo_titles)

    def test_endpoint_return_folder_prenotazioni_for_each_uo(self):
        resp = self.api_session.get(f"{self.portal_url}/@bookable-uo-list").json()

        first = resp["items"][0]
        second = resp["items"][1]

        self.assertIn("prenotazioni_folder", first)
        self.assertIn("prenotazioni_folder", second)

        self.assertEqual(len(first["prenotazioni_folder"]), 2)
        self.assertEqual(len(second["prenotazioni_folder"]), 1)

        self.assertEqual(
            first["prenotazioni_folder"][0]["title"], self.prenotazioni_folder.title
        )
        self.assertEqual(
            first["prenotazioni_folder"][1]["title"], self.prenotazioni_folder2.title
        )
        self.assertEqual(
            second["prenotazioni_folder"][0]["title"], self.prenotazioni_folder3.title
        )

    def test_endpoint_return_folder_prenotazioni_details_for_each_uo(self):
        resp = self.api_session.get(f"{self.portal_url}/@bookable-uo-list").json()

        prenotazioni_folder = resp["items"][0]["prenotazioni_folder"][0]

        self.assertEqual(prenotazioni_folder["title"], self.prenotazioni_folder.title)
        self.assertEqual(
            prenotazioni_folder["orario_di_apertura"],
            self.prenotazioni_folder.orario_di_apertura,
        )
        self.assertEqual(
            prenotazioni_folder["address"],
            getMultiAdapter((self.venue, self.request), ISerializeToJsonSummary)(),
        )
        self.assertEqual(
            prenotazioni_folder["description_agenda"],
            {
                "content-type": "text/html",
                "data": "<h1>description agenda</h1>",
                "encoding": "utf-8",
            },
        )

    def test_endpoint_return_filtered_uo_based_on_service_uid(self):
        resp = self.api_session.get(
            f"{self.portal_url}/@bookable-uo-list?uid=foo"
        ).json()
        self.assertEqual(resp["items"], [])

        # we need to pass a servizio UID
        resp = self.api_session.get(
            f"{self.portal_url}/@bookable-uo-list?uid={self.unita_organizzativa.UID()}"
        ).json()
        self.assertEqual(resp["items"], [])

        resp = self.api_session.get(
            f"{self.portal_url}/@bookable-uo-list?uid={self.servizio.UID()}"
        ).json()
        self.assertEqual(len(resp["items"]), 1)
        self.assertEqual(resp["items"][0]["title"], self.unita_organizzativa.title)

    def test_endpoint_bookable_list(self):
        resp = self.api_session.get(f"{self.portal_url}/@bookable-list").json()
        self.assertEqual(len(resp["items"]), 3)
        self.assertEqual(
            sorted([i["url"].split("booking_type=")[1] for i in resp["items"]]),
            ["Type+A", "Type+A", "Type+B"],
        )
