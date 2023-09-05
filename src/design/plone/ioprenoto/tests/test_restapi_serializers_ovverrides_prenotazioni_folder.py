# -*- coding: utf-8 -*-
from design.plone.ioprenoto.testing import DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.restapi.testing import RelativeSession
from transaction import commit

import unittest


class SummarySerializerTest(unittest.TestCase):
    layer = DESIGN_PLONE_IOPRENOTO_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()

        api.user.create(email="user@plone.org", username="user", password="secretxx")
        api.user.create(
            email="editor@plone.org", username="editor", password="secretxx"
        )

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.prenotazioni_folder = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Prenotazioni folder",
        )
        self.prenotazioni_folder2 = api.content.create(
            container=self.portal,
            type="PrenotazioniFolder",
            title="Prenotazioni folder 2",
        )

        api.user.grant_roles(
            username="editor", roles=["Editor"], obj=self.prenotazioni_folder
        )

        api.content.transition(self.prenotazioni_folder, transition="publish")
        api.content.transition(self.prenotazioni_folder2, transition="publish")

        commit()

        self.api_session_admin = RelativeSession(self.portal_url)
        self.api_session_admin.headers.update({"Accept": "application/json"})
        self.api_session_admin.auth = (TEST_USER_NAME, TEST_USER_PASSWORD)

        self.api_session_user = RelativeSession(self.portal_url)
        self.api_session_user.headers.update({"Accept": "application/json"})
        self.api_session_user.auth = ("user", "secretxx")
        self.api_session_editor = RelativeSession(self.portal_url)
        self.api_session_editor.headers.update({"Accept": "application/json"})
        self.api_session_editor.auth = ("editor", "secretxx")
        self.api_session_anon = RelativeSession(self.portal_url)
        self.api_session_anon.headers.update({"Accept": "application/json"})

    def tearDown(self):
        self.api_session_admin.close()
        self.api_session_user.close()
        self.api_session_editor.close()
        self.api_session_anon.close()

    def test_anon_redirected(self):
        # self.assertIn(
        #     "prenotazione-appuntamenti-uffici",
        #     self.api_session_anon.get(self.prenotazioni_folder.absolute_url()).url,
        # )
        res = self.api_session_anon.get(self.prenotazioni_folder.absolute_url())
        self.assertEqual(res.json()["error"], "Unauthorized")
        self.assertEqual(res.json()["anonymous"], True)

    def test_user_redirected(self):
        # self.assertIn(
        #     "prenotazione-appuntamenti-uffici",
        #     self.api_session_user.get(self.prenotazioni_folder.absolute_url()).url,
        # )
        res = self.api_session_user.get(self.prenotazioni_folder.absolute_url())
        self.assertEqual(res.json()["error"], "Unauthorized")
        self.assertEqual(res.json()["anonymous"], False)

    def test_editor_redirected_where_cant_edit(self):
        # self.assertIn(
        #     "prenotazione-appuntamenti-uffici",
        #     self.api_session_editor.get(self.prenotazioni_folder2.absolute_url()).url,
        # )
        res = self.api_session_editor.get(self.prenotazioni_folder2.absolute_url())
        self.assertEqual(res.json()["error"], "Unauthorized")
        self.assertEqual(res.json()["anonymous"], False)

    def test_editor_can_access_if_have_permission(self):
        self.assertEqual(
            self.api_session_editor.get(self.prenotazioni_folder.absolute_url()).json()[
                "@id"
            ],
            self.prenotazioni_folder.absolute_url(),
        )

    def test_admin_can_access_both(self):
        self.assertEquals(
            self.api_session_admin.get(self.prenotazioni_folder.absolute_url()).json()[
                "@id"
            ],
            self.prenotazioni_folder.absolute_url(),
        )
        self.assertEquals(
            self.api_session_admin.get(self.prenotazioni_folder2.absolute_url()).json()[
                "@id"
            ],
            self.prenotazioni_folder2.absolute_url(),
        )
