import itertools
import json

import pytest
from laz_api.catalog import build_catalog
from laz_api.static_export import (
    DIMENSIONS,
    Writer,
    export_catalog,
    feature_code,
    feature_values,
)


def test_feature_encoding_is_lossless():
    # All concrete inputs, including null objects and both prefix settings.
    for values in itertools.product(*DIMENSIONS):
        assert feature_values(feature_code(values)) == list(values)


def test_range_shards_never_split_a_key(tmp_path):
    writer = Writer(tmp_path)
    rows = [["a", [1]], ["a\u0301", [2, 3]], ["b", [4]], ["𐐀", [5]]]
    bounds = writer.shards("index", rows, 15)
    recovered = []
    for first, last, filename in bounds:
        part = json.loads((tmp_path / filename).read_text())
        assert (first, last) == (part[0][0], part[-1][0])
        recovered.extend(part)
    assert recovered == rows
    assert len(bounds) > 1


def test_public_export_requires_full_catalog_and_preserves_existing_files(tmp_path, verb):
    database = tmp_path / "test.sqlite"
    build_catalog(database, profile="core", entries=(verb("doguru"),))
    output = tmp_path / "data"
    with pytest.raises(ValueError, match="full catalog"):
        export_catalog(database, output)
    assert not output.exists()
    result = export_catalog(database, output, allow_partial=True)
    assert result["forms"] > 0
    assert result["largest_file_bytes"] < 25 * 1024 * 1024
    before = (output / "manifest.json").read_bytes()
    with pytest.raises(FileExistsError):
        export_catalog(database, output, allow_partial=True)
    assert (output / "manifest.json").read_bytes() == before


def test_export_rejects_stale_rules(tmp_path, verb, monkeypatch):
    database = tmp_path / "test.sqlite"
    build_catalog(database, profile="core", entries=(verb("doguru"),))
    monkeypatch.setattr("laz_api.static_export.engine_revision", lambda: "changed")
    with pytest.raises(ValueError, match="stale"):
        export_catalog(database, tmp_path / "data", allow_partial=True)
    assert not (tmp_path / "data").exists()
