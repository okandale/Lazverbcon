"""Reproduce the private rule snapshot and lexical import from this checkout.

No linguistic transformations are performed. Rule bodies are retained verbatim;
their module-level data dependencies become an explicit per-call context.
"""

import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "laz_verb_conjugator/backend"
TARGET = ROOT / "packages/engine/src/laz_engine"
GLOBALS = ("verbs", "regions", "co_verbs", "gyo_verbs", "no_verbs")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    legacy = ROOT / "migration/reference/rules"
    data = TARGET / "data"
    legacy.mkdir(parents=True, exist_ok=True)
    data.mkdir(parents=True, exist_ok=True)
    (legacy / "__init__.py").write_text('"""Private reference rules; see migration/README.md."""\n')
    manifest = {"source_commit": "0b3c9cd", "files": {}}
    for path in sorted((SOURCE / "notebooks").glob("*.py")):
        if path.name == "__init__.py":
            continue
        source = path.read_text()
        lines = source.splitlines()
        blocks = ['"""Mechanically extracted legacy rules; edit through reviewed migrations."""']
        for node in ast.parse(source).body:
            if isinstance(node, ast.ImportFrom) and node.module == "utils":
                blocks.append(
                    "\n".join(lines[node.lineno - 1 : node.end_lineno]).replace("..utils", ".utils")
                )
            elif isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "preverbs_rules" for t in node.targets
            ):
                blocks.append("\n".join(lines[node.lineno - 1 : node.end_lineno]))
            elif isinstance(node, ast.FunctionDef) and not node.name.startswith(
                ("collect_", "format_", "process_imperative")
            ):
                block = lines[node.lineno - 1 : node.end_lineno]
                if node.name.startswith("conjugate_"):
                    block[0] = block[0].removesuffix("):") + ", *, context):"
                    used = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
                    bindings = [f"    {name} = context.{name}" for name in GLOBALS if name in used]
                    block[1:1] = bindings
                # Debug printing has no linguistic effect and leaks into CLI JSON.
                block = [line for line in block if not line.lstrip().startswith("print(")]
                blocks.append("\n".join(block))
        (legacy / path.name).write_text("\n\n".join(blocks) + "\n")
        manifest["files"][str(path.relative_to(ROOT))] = digest(path)
    (legacy / "utils.py").write_text((SOURCE / "utils.py").read_text())
    manifest["files"][str((SOURCE / "utils.py").relative_to(ROOT))] = digest(SOURCE / "utils.py")
    rows = json.loads((SOURCE / "data/verb_data.json").read_text())
    entries = []
    for number, row in enumerate(rows, 1):
        variants = []
        issues = []
        for suffix in ("", " Alternative 1", " Alternative 2"):
            form = row.get("Laz 3rd Person Singular Present" + suffix)
            regions = row.get("Region" + suffix)
            if form or regions:
                variants.append(
                    {
                        "form": form or "",
                        "dialects": [
                            "AS" if r.strip() == "AŞ" else r.strip()
                            for r in (regions or "").split(",")
                            if r.strip()
                        ],
                    }
                )
                if not (form and regions):
                    issues.append(f"Unpaired principal part/dialect: {suffix.strip() or 'base'}")
        entries.append(
            {
                "id": f"verb-{number:04d}",
                "infinitive": row["Laz Infinitive"],
                "verb_class": row["Category"],
                "english": row.get("English Translation") or "",
                "turkish": row.get("Turkish Verb") or "",
                "variants": variants,
                "source_row": number,
                "issues": issues,
            }
        )
    (data / "entries.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n")
    manifest["files"][str((SOURCE / "data/verb_data.json").relative_to(ROOT))] = digest(
        SOURCE / "data/verb_data.json"
    )
    (data / "provenance.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Imported {len(entries)} entries and 12 rule modules.")


if __name__ == "__main__":
    main()
