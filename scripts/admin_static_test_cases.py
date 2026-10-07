"""Create an editorial export containing a deliberate generator-disallowed form."""

import json
import sys
from dataclasses import asdict
from pathlib import Path

from laz_admin.archive import unpack
from laz_admin.publish import export_release
from laz_admin.store import Store
from laz_engine.lexicon import load_entries


def build(directory):
    store = Store(directory / "project")
    original = next(e for e in load_entries() if e.infinitive == "doguru")
    entry = store.save_entry(
        {**asdict(original), "id": "editorial-new", "infinitive": "editorial", "verb_class": "TVM"},
        "Test",
        "",
    )
    item = {
        "entry_id": entry["id"],
        "features": {"dialect": "AS", "subject": "1sg", "object": "2sg", "optional_prefix": "ko"},
        "value": {
            "status": "ok",
            "forms": [
                {
                    "spelling": "author-exception",
                    "frame": "Nominative",
                    "subject_pronoun": "reviewed-subject",
                    "object_pronoun": "reviewed-object",
                }
            ],
        },
    }
    store.propose([item], "Test", "")
    store.review([store.proposals()["proposals"][0]["id"]], True, "Test")
    item["value"]["forms"][0]["spelling"] = "private-draft"
    store.propose([item], "Test", "")
    info = export_release(store, "Test")
    unpack(store.directory / "exports" / info["filename"], directory / "data")
    (directory / "selection.json").write_text(
        json.dumps({"entry_id": entry["id"], **item["features"], "dialects": ["AS"]})
    )


if __name__ == "__main__":
    build(Path(sys.argv[1]))
