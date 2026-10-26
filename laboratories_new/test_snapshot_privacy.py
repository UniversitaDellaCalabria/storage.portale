"""
Test di privacy sugli snapshot dei laboratori.

Verifica che nel JSON dello snapshot non finiscano dati utente
(password, codice fiscale, email, permessi, ecc.).

Esecuzione:
    python manage.py test laboratories_new.tests.test_snapshot_privacy

Il controllo sugli snapshot gia' presenti nel database (classe
ExistingSnapshotsPrivacyCheck) e' pensato per essere lanciato sul DB reale
(le tabelle LABORATORIO_* sono managed=False e non esistono nel DB di test):
    SNAPSHOT_PRIVACY_REAL_DB=1 python manage.py test --keepdb ...
oppure, piu' semplicemente, dalla shell con find_sensitive_keys().
"""

import json
import os
import unittest

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase

from laboratories_new import snapshot_exporter
from laboratories_new.models import LaboratorioDatiBase, LaboratorioSnapshot

# Chiavi che non devono MAI comparire in uno snapshot
FORBIDDEN_KEYS = {
    "password",
    "cod_fis",
    "taxpayer_id",
    "username",
    "last_login",
    "is_superuser",
    "is_staff",
    "is_active",
    "date_joined",
    "user_permissions",
    "groups",
    "first_name",
    "last_name",
    "email",
    "origin",
    "manual_user_update",
}

# Eccezione consapevole: Personale e' whitelistato e lo snapshot aggiunge
# volutamente l'email istituzionale (snapshot_email). "email" esatta resta vietata.
ALLOWED_KEYS = {"snapshot_email"}


def find_sensitive_keys(data, path="", forbidden=FORBIDDEN_KEYS):
    """Restituisce la lista dei percorsi in cui compare una chiave vietata."""
    found = []
    if isinstance(data, dict):
        for key, value in data.items():
            here = f"{path}/{key}"
            if key in forbidden and key not in ALLOWED_KEYS:
                found.append(here)
            found.extend(find_sensitive_keys(value, here, forbidden))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            found.extend(find_sensitive_keys(item, f"{path}[{i}]", forbidden))
    return found


class FindSensitiveKeysTests(SimpleTestCase):
    """Il controllo stesso funziona (non serve il database)."""

    def test_clean_data_has_no_findings(self):
        data = {"id": 1, "user_mod": 10, "figli": [{"id": 2, "id_user_mod": None}]}
        self.assertEqual(find_sensitive_keys(data), [])

    def test_finds_nested_keys_in_dicts_and_lists(self):
        data = {
            "user_mod": {"id": 10, "password": "x"},
            "figli": [{"ricerca": {"user_ins": {"username": "AAA"}}}],
        }
        self.assertEqual(
            sorted(find_sensitive_keys(data)),
            sorted(
                [
                    "/user_mod/password",
                    "/figli[0]/ricerca/user_ins/username",
                ]
            ),
        )

    def test_snapshot_email_is_allowed_but_email_is_not(self):
        self.assertEqual(find_sensitive_keys({"snapshot_email": []}), [])
        self.assertEqual(find_sensitive_keys({"email": "a@b.it"}), ["/email"])


class SerializerDoesNotLeakUsersTests(TestCase):
    """_serialize non deve espandere gli utenti, nemmeno se li incontra."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="RSSMRA80A01H501U",
            password="segreta-123",
            email="mario.rossi@example.it",
            first_name="Mario",
            last_name="Rossi",
            is_staff=True,
            is_superuser=True,
        )

    def test_user_serialized_directly_exposes_only_id(self):
        data = snapshot_exporter._serialize(self.user)
        self.assertEqual(set(data.keys()), {"id"})

    def test_fk_to_user_is_only_an_id(self):
        # istanza non salvata: non serve la tabella LABORATORIO_DATI_BASE
        lab = LaboratorioDatiBase(id=1, nome_laboratorio="Lab", user_mod=self.user)
        data = snapshot_exporter._serialize(lab)

        self.assertEqual(data["user_mod"], self.user.pk)
        self.assertEqual(find_sensitive_keys(data), [])

    def test_serialized_json_contains_no_user_secrets(self):
        lab = LaboratorioDatiBase(id=1, nome_laboratorio="Lab", user_mod=self.user)
        payload = json.dumps(snapshot_exporter._serialize(lab), cls=snapshot_exporter._Encoder)

        for secret in (
            "segreta-123",
            "pbkdf2_sha256",
            "RSSMRA80A01H501U",
            "mario.rossi@example.it",
        ):
            self.assertNotIn(secret, payload)


@unittest.skipUnless(
    os.environ.get("SNAPSHOT_PRIVACY_REAL_DB") == "1",
    "Eseguire solo su un DB reale con le tabelle LABORATORIO_* (SNAPSHOT_PRIVACY_REAL_DB=1)",
)
class ExistingSnapshotsPrivacyCheck(TestCase):
    """Controlla tutti gli snapshot gia' salvati nel database."""

    def test_no_snapshot_contains_sensitive_keys(self):
        problems = {}
        for snap in LaboratorioSnapshot.objects.all().iterator():
            found = find_sensitive_keys(snap.data)
            if found:
                problems[snap.id] = found[:5]
        self.assertEqual(
            problems,
            {},
            f"Snapshot con dati sensibili (id: percorsi): {problems}",
        )