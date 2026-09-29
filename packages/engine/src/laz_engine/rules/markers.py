"""Markers shared across paradigms."""


def determine_marker(subject: str, obj: str | None, marker_type: str) -> str:
    """Choose the vowel marker; agreement and stem changes happen separately."""
    if marker_type == "applicative":
        if obj is None:
            raise ValueError("An applicative requires an object")
        return "u" if obj.startswith("O3") else "i"
    if marker_type in ("causative", "simple_causative"):
        return "o"
    raise ValueError(f"Unknown marker type: {marker_type}")


def handle_marker(infinitive, root, marker, subject, obj):
    if infinitive == "doguru":
        root = root[1:]
    if infinitive in ("oç̌ǩomu", "oşǩomu") and marker == "o":
        root = "çams"
        marker = ""
    if infinitive in "oxenu" and marker in ("u", "i", "o"):
        root = "xenams"
    if infinitive in "oxvenu" and marker in ("u", "i", "o"):
        root = "xvenams"
    if infinitive in "oç̌ǩomu" and marker in ("i", "u"):
        root = "ç̌ǩomums"
    if infinitive in "oşǩomu" and marker in ("i", "u"):
        root = "şǩomums"
    if infinitive in ("gemgaru", "cebgaru"):
        if marker in ["i", "o", "u"]:
            root = root[:1] + marker + root[3:]
    if root.startswith("gyo"):
        if root[2] in ["i", "o"]:
            if marker in ["i"]:
                root = root[:1] + marker + root[3:]
            elif marker == "o":
                root = (
                    root[:1] + marker + root[3:]
                    if subject in ("S1_Singular", "S1_Plural")
                    or obj in ("O1_Singular", "O2_Singular", "O1_Plural", "O2_Plural")
                    else root[1:]
                )
            elif marker == "u":
                root = marker + root[2:]
    if root.startswith("co"):
        if root[1] in ["i", "o"]:
            if marker in ["i"]:
                root = root[:1] + marker + root[2:]
            elif marker == "o":
                root = (
                    root[:1] + marker + root[2:]
                    if subject in ("S1_Singular", "S1_Plural")
                    or obj in ("O1_Singular", "O2_Singular", "O1_Plural", "O2_Plural")
                    else marker + root[2:]
                )
            elif marker == "u":
                root = "u" + root[2:]
    if root.startswith(("i", "u", "o")):
        if marker in ["i", "o", "u"]:
            root = marker + root[1:]
        elif marker == "u":
            root = "u" + root[1:]
    else:
        root = marker + root
    return root


ivd_subject_markers = {
    "S1_Singular": "m",
    "S2_Singular": "g",
    "S3_Singular": "",
    "S1_Plural": "m",
    "S2_Plural": "g",
    "S3_Plural": "",
}
tve_subject_markers = {
    "S1_Singular": "v",
    "S2_Singular": "",
    "S3_Singular": "",
    "S1_Plural": "v",
    "S2_Plural": "",
    "S3_Plural": "",
}
presentperf_subject_markers = {
    "S1_Singular": "mi",
    "S2_Singular": "gi",
    "S3_Singular": "u",
    "S1_Plural": "mi",
    "S2_Plural": "gi",
    "S3_Plural": "u",
}
potential_subject_markers = {
    "S1_Singular": "ma",
    "S2_Singular": "ga",
    "S3_Singular": "a",
    "S1_Plural": "ma",
    "S2_Plural": "ga",
    "S3_Plural": "a",
}
