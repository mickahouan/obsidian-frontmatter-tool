SUPPORTED_EXTENSIONS = ["*.md", "*.txt", "*.html", "*.yaml", "*.yml"]


def is_supported_file(filename: str) -> bool:
    """
    Prüft, ob die Datei eine unterstützte Erweiterung hat.
    """
    if not filename:  # Sicherstellen, dass filename nicht None oder leer ist
        return False
    return any(filename.lower().endswith(ext[1:]) for ext in SUPPORTED_EXTENSIONS)


def value_matches(a, b, match_all_in_list=False) -> bool:
    """
    Vergleicht zwei Werte (String oder Liste) flexibel.
    - a: Wert 1 (String oder Liste)
    - b: Wert 2 (String oder Liste)
    - match_all_in_list: Wenn True, müssen bei Listen alle Elemente übereinstimmen (Reihenfolge egal).
        Wenn False, reicht ein Match eines Elements.

    Beispiele:
    - value_matches("foo", "foo") -> True
    - value_matches(["foo", "bar"], "foo") -> True
    - value_matches("foo", ["foo", "bar"]) -> True
    - value_matches(["foo", "bar"], ["bar", "foo"]) -> True (wenn match_all_in_list=True)
    - value_matches(["foo", "bar"], ["bar", "baz"]) -> False
    """

    def to_list(val):
        if isinstance(val, list):
            return val
        if val is None:
            return []
        return [val]

    list_a = to_list(a)
    list_b = to_list(b)

    if match_all_in_list:
        return set(str(x) for x in list_a) == set(str(y) for y in list_b)
    else:
        set_a = set(str(x) for x in list_a)
        set_b = set(str(y) for y in list_b)
        return not set_a.isdisjoint(set_b)
