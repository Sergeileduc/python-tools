def format_duration(seconds: float) -> str:
    """
    Formate une durée en secondes ou millisecondes selon la valeur.

    Args:
        seconds (float): Durée en secondes.

    Returns:
        str: Durée formatée avec unité adaptée.
    """
    if seconds < 1e-3:  # moins d'une milliseconde
        return f"{seconds * 1e6:.2f}µs"
    elif seconds < 1:  # moins d'une seconde
        return f"{seconds * 1e3:.2f}ms"
    else:
        return f"{seconds:.2f}s"
