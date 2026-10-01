"""Developer tools: conjugate, publish SQLite, and serve the application."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from laz_engine.engine import conjugate
from laz_engine.lexicon import load_entries
from laz_engine.models import Dialect, Features, Person, Tense

from .catalog import BuildFailed, build_catalog


def main():
    parser = argparse.ArgumentParser(prog="lazcon")
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build", help="Build and validate an immutable SQLite release")
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--profile", choices=["core", "full"], default="full")
    build.add_argument(
        "--verb", action="append", help="Limit by exact infinitive or entry ID; repeatable"
    )
    export = commands.add_parser("export-static", help="Export a catalog for browser-only hosting")
    export.add_argument("--database", type=Path, required=True)
    export.add_argument("--output", type=Path, required=True)
    export.add_argument("--allow-partial", action="store_true")
    query = commands.add_parser("conjugate", help="Inspect a concrete engine request")
    query.add_argument("verb")
    query.add_argument("--dialect", choices=list(Dialect), default="AS")
    query.add_argument("--subject", choices=list(Person), default="1sg")
    query.add_argument("--tense", choices=list(Tense), default="present")
    serve = commands.add_parser("serve", help="Serve engine preview or a published database")
    serve.add_argument("--database", type=Path)
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    schema = commands.add_parser("openapi", help="Export the API schema for TypeScript generation")
    schema.add_argument("--output", type=Path, default=Path("apps/web/openapi.json"))
    args = parser.parse_args()
    if args.command == "build":
        entries = load_entries()
        if args.verb:
            entries = tuple(e for e in entries if e.id in args.verb or e.infinitive in args.verb)
            if not entries:
                parser.error("No matching entries")

        def progress(done, total, report):
            if done % 20 == 0 or done == total:
                print(
                    f"{done}/{total} entries · {report['form_count']:,} forms · {len(report['errors'])} errors",
                    file=sys.stderr,
                )

        try:
            report = build_catalog(args.output, args.profile, entries, progress)
        except (BuildFailed, FileExistsError) as exc:
            print(str(exc), file=sys.stderr)
            raise SystemExit(1) from exc
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.command == "export-static":
        from .static_export import export_catalog

        print(
            json.dumps(
                export_catalog(args.database, args.output, allow_partial=args.allow_partial),
                indent=2,
            )
        )
    elif args.command == "conjugate":
        entries = [e for e in load_entries() if args.verb in (e.id, e.infinitive)]
        if not entries:
            parser.error("Unknown verb")
        features = Features(Dialect(args.dialect), Person(args.subject), tense=Tense(args.tense))
        print(
            json.dumps(
                [{"entry_id": e.id, **asdict(conjugate(e, features))} for e in entries],
                ensure_ascii=False,
                indent=2,
            )
        )
    elif args.command == "serve":
        import uvicorn

        from .app import create_app

        uvicorn.run(create_app(args.database), host=args.host, port=args.port)
    elif args.command == "openapi":
        from .app import create_app

        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(create_app().openapi(), ensure_ascii=False, indent=2) + "\n"
        )


if __name__ == "__main__":
    main()
