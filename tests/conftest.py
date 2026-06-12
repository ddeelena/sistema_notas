# tests/conftest.py

import pytest

from sistema_notas.services.gestion_notas_service import GestionNotasService
from sistema_notas.database.database import get_connection


@pytest.fixture
def service():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE notas")

    conn.commit()
    cursor.close()
    conn.close()

    return GestionNotasService()