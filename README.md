# python-tools-sl

Petits utilitaires Python pour fiabiliser les tests et améliorer l’ergonomie (décorateurs, helpers, etc.).

## Installation

Tu peux installer directement depuis GitHub :

    pip install git+https://github.com/Sergeileduc/python-tools.git@main

Ou bien ajouter la dépendance dans ton `requirements.txt` :

    git+https://github.com/Sergeileduc/python-tools.git@main

## Utilisation

### Importer les décorateurs

    from python_tools_sl.decorators.pauses import with_pause, with_pause_async

### Exemple avec un test synchrone

    @with_pause(2, message="ouais, pause de 2 secondes pour pas se faire timeout")
    @pytest.mark.parametrize("backend", ["playwright", "requests"])
    def test_make_soup_twitter(backend):
        soup = make_soup("https://x.com/login", backend=backend, timeout=120)
        assert soup.title is not None

### Exemple avec un test asynchrone

    @pytest.mark.asyncio
    @with_pause_async(2, message="pause async de 2 secondes pour souffler")
    async def test_amake_soup_twitter():
        soup = await amake_soup("https://x.com/login", backend="aiohttp", timeout=120)
        assert soup.title is not None

### Résultat attendu

Lors de l’exécution des tests, tu verras apparaître les messages définis dans tes décorateurs :

    pause après chaque test backend
    pause async de 2 secondes pour souffler
    ouais, pause de 2 secondes pour pas se faire timeout

Et tes tests seront espacés de quelques secondes pour éviter les timeouts.

## Roadmap

- Ajouter d’autres décorateurs (`retry`, `log_time`, etc.)
- Helpers réseau (timeouts par défaut, gestion des headers)
- Marqueurs pytest (`slow`, `network`) pour catégoriser les tests
