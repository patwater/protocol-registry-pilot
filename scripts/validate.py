#!/usr/bin/env python3
"""
validate.py -- Protocol Registry entry validator.

Checks a protocol JSON file against the canonical schema at
schema/protocol-entry.schema.json. Used locally by contributors and
by the validate.yml GitHub Action on pull requests.

Usage:
    python scripts/validate.py protocols/my-protocol.json
    python scripts/validate.py protocols/*.json   # validate several at once
    python scripts/validate.py --all              # validate entire protocols/ dir

Exit codes:
    0 -- all files valid
    1 -- one or more files failed validation
"""

import json
import sys
import os
import argparse
import glob
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError, SchemaError
except ImportError:
    print("ERROR: jsonschema is required. Install it with: pip install jsonschema")
    sys.exit(1)


REPO_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "protocol-entry.schema.json"
PROTOCOLS_DIR = REPO_ROOT / "protocols"


def load_schema() -> dict:
    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema not found at {SCHEMA_PATH}")
        sys.exit(1)
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def validate_file(filepath: str, schema: dict) -> list[str]:
    """
    Validate a single protocol JSON file against the schema.
    Returns a list of error messages (empty list = valid).
    """
    errors = []
    path = Path(filepath)

    # 1. File must exist and be readable
    if not path.exists():
        return [f"File not found: {filepath}"]

    # 2. Must be valid JSON
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]

    # 3. Must conform to schema
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        errors.append(f"Schema validation failed: {e.message}")
        if e.path:
            errors.append(f"  at: {' -> '.join(str(p) for p in e.path)}")
    except SchemaError as e:
        errors.append(f"Schema itself is invalid: {e.message}")
        return errors

    # 4. Slug must match filename (unless in examples/)
    if "protocols/examples/" not in str(path).replace("\\", "/"):
        slug = data.get("metadata", {}).get("slug", "")
        filename_stem = path.stem
        if slug != filename_stem:
            errors.append(
                f"Slug mismatch: metadata.slug='{slug}' but filename is '{filename_stem}.json'"
            )

    # 5. Warn if pass_type is full but fewer than 23 gradients are scored
    pass_type = data.get("bicorder", {}).get("pass_type", "full")
    gradients = data.get("bicorder", {}).get("gradients", {})
    FULL_GRADIENT_COUNT = 23
    SHORTFORM_GRADIENT_COUNT = 11

    if pass_type == "full" and len(gradients) < FULL_GRADIENT_COUNT:
        errors.append(
            f"pass_type is 'full' but only {len(gradients)}/{FULL_GRADIENT_COUNT} gradients are present. "
            f"Set pass_type to 'shortform' or complete the remaining gradients."
        )
    elif pass_type == "shortform" and len(gradients) < SHORTFORM_GRADIENT_COUNT:
        errors.append(
            f"pass_type is 'shortform' but only {len(gradients)}/{SHORTFORM_GRADIENT_COUNT} gradients are present."
        )

    # 6. Warn if verified_by is set to a username but verification_date is missing
    verified_by = data.get("provenance", {}).get("verified_by", "auto")
    verification_date = data.get("provenance", {}).get("verification_date")
    if verified_by and verified_by != "auto" and not verification_date:
        errors.append(
            f"verified_by is set to '{verified_by}' but verification_date is missing."
        )

    return errors


def validate_files(filepaths: list[str], schema: dict) -> bool:
    """
    Validate a list of files. Prints results and returns True if all passed.
    """
    total = len(filepaths)
    passed = 0
    failed = 0

    for filepath in filepaths:
        errors = validate_file(filepath, schema)
        if errors:
            print(f"\n❌ FAILED: {filepath}")
            for err in errors:
                print(f"   {err}")
            failed += 1
        else:
            print(f"✅ OK: {filepath}")
            passed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} valid, {failed} failed")

    return failed == 0


def main():
    parser = argparse.ArgumentParser(
        description="Validate protocol registry JSON entries against the schema."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Protocol JSON files to validate (supports glob patterns)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all .json files in the protocols/ directory (excluding examples/)"
    )
    parser.add_argument(
        "--include-examples",
        action="store_true",
        help="When using --all, also validate files in protocols/examples/"
    )

    args = parser.parse_args()

    schema = load_schema()

    if args.all:
        pattern = str(PROTOCOLS_DIR / "**" / "*.json")
        all_files = glob.glob(pattern, recursive=True)
        if not args.include_examples:
            all_files = [f for f in all_files if "examples" not in Path(f).parts]
        filepaths = sorted(all_files)
        if not filepaths:
            print("No protocol files found.")
            sys.exit(0)
    elif args.files:
        # Expand any glob patterns passed as arguments
        filepaths = []
        for pattern in args.files:
            expanded = glob.glob(pattern)
            if expanded:
                filepaths.extend(expanded)
            else:
                filepaths.append(pattern)  # will fail with "file not found" gracefully
    else:
        parser.print_help()
        sys.exit(0)

    success = validate_files(filepaths, schema)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
