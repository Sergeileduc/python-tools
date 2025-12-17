import pytest

# Configure pytest-asyncio pour utiliser une boucle "auto" par défaut


def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio: mark test as async")


@pytest.fixture(scope="session")
def event_loop():
    """
    Crée une boucle d'événements unique pour toute la session de tests.
    Évite que pytest recrée une boucle à chaque test.
    """
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
