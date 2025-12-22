import datetime
import json
import re
from typing import Any, cast

from python_tools_sl.utils.typing_helpers import JSONType


def is_json_type(value: Any) -> bool:
    """Return True if the value matches the JSONType structure."""
    if value is None:
        return True

    if isinstance(value, (str, int, float, bool)):
        return True

    if isinstance(value, list):
        return all(is_json_type(item) for item in value)

    if isinstance(value, dict):
        return all(isinstance(k, str) and is_json_type(v) for k, v in value.items())

    return False


def parse_json_safe(text: str) -> JSONType | None:
    """Parse une chaîne JSON en objet Python.

    Essaie de convertir la chaîne en JSON. Si la chaîne est valide,
    retourne l'objet Python correspondant (dict, list, str, int, float,
    bool ou None). Si la chaîne n'est pas un JSON valide, retourne None
    au lieu de lever une exception.

    Args:
        text (str): Chaîne représentant un objet JSON.

    Returns:
        JSONType | None: Objet Python si le JSON est valide, sinon None.
    """
    try:
        return cast(JSONType, json.loads(text))
    except json.JSONDecodeError:
        return None


def parse_date(value: str) -> datetime.datetime:
    """Parse une chaîne en objet datetime.

    La fonction accepte plusieurs formats :
      * "YYYY-MM-DD" (ex. "2025-12-17")
      * "DD/MM/YYYY" (ex. "17/12/2025")
      * "YYYYMMDD"   (ex. "20251217")
      * Timestamp en secondes (ex. "1766016000")

    Args:
        value (str): Chaîne représentant une date ou un timestamp.

    Returns:
        datetime.datetime: Objet datetime correspondant à la valeur fournie.

    Raises:
        ValueError: Si la chaîne ne correspond à aucun des formats supportés.
    """

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y%m%d"):
        try:
            return datetime.datetime.strptime(value, fmt)
        except ValueError:
            continue
    if value.isdigit():
        return datetime.datetime.fromtimestamp(int(value))
    raise ValueError(f"Format de date non reconnu: {value}")


def parse_bool(value: str) -> bool:
    """Convertit une chaîne en booléen.

    Accepte plusieurs représentations textuelles :
      * "true", "yes", "1" → True
      * "false", "no", "0" → False

    Args:
        value (str): Chaîne représentant une valeur booléenne.

    Returns:
        bool: True ou False selon la valeur fournie.

    Raises:
        ValueError: Si la chaîne ne correspond à aucune représentation valide.
    """
    return str(value).strip().lower() in ("true", "yes", "1", "on")


def slugify(text: str) -> str:
    """Transforme une chaîne en slug.

    Convertit la chaîne en minuscules, remplace les espaces et caractères
    non alphanumériques par des tirets, et supprime les caractères invalides.

    Args:
        text (str): Chaîne à transformer.

    Returns:
        str: Slug généré à partir de la chaîne.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")
