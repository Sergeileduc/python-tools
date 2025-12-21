import time
from contextlib import contextmanager
from itertools import islice
from typing import Iterable, Iterator, List, TypeVar

T = TypeVar("T")


def chunks(iterable: Iterable[T], size: int) -> Iterator[List[T]]:
    """
    Génère des sous-ensembles d'un itérable de taille fixe.

    Args:
        iterable (Iterable[T]): Toute source itérable (liste, range, fichier, générateur...).
        size (int): Nombre d'éléments par chunk.

    Yields:
        List[T]: Un sous-ensemble de l'itérable de longueur `size` (sauf le dernier
                 qui peut être plus court).

    Exemple:
        >>> list(chunks(range(10), 3))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    if size <= 0:
        raise ValueError("size doit être un entier positif")

    it = iter(iterable)
    while True:
        batch: List[T] = list(islice(it, size))
        if not batch:
            break
        yield batch


@contextmanager
def timer(name: str = "block"):  # type: ignore
    """
    Mesure le temps d'exécution d'un bloc de code.

    Args:
        name (str): Nom du bloc à afficher dans la sortie.

    Exemple:
        >>> with timer("scraping"):
        ...     do_scraping()
        # [scraping] terminé en 2.34s
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        duration = end - start
        print(f"[{name}] terminé en {duration:.2f}s")


if __name__ == "__main__":
    #  ####### chunks ##############
    # Test avec une liste
    print("-" * 50)

    print("Test avec range(10), size=3 :")
    for batch in chunks(range(10), 3):
        print(batch)

    print("\n" + "-" * 15)
    # Test avec un générateur infini (on coupe après 3 chunks)
    print("Test avec générateur infini, size=5 :")

    def infinite_numbers() -> Iterator[int]:
        n = 0
        while True:
            yield n
            n += 1

    for i, batch in enumerate(chunks(infinite_numbers(), 5)):
        print(batch)
        if i == 2:  # stop après 3 chunks
            break

    print("\n" + "-" * 50)

    #  ####### timer ##############
    with timer("sleep test"):
        time.sleep(1.5)

    with timer("boucle"):
        total = 0
        for i in range(1000000):
            total += i
