"""Sync project version in `pyproject.toml` with the latest `CHANGELOG.md` one.

The latest version is taken from the first `## X.Y.Z (DD.MM.YY)` heading of
changelog (`## Unreleased` is skipped). If changelog has no released versions
yet (e.g. fresh project with only unreleased changes), the check is skipped.

If `pyproject.toml` contains another version, it is fixed in place and script
exits with non-zero code, so pre-commit aborts commit and developer can stage
the changes and commit again.

Also the latest version must have a release date. If it is missing, today's
date is set. If it is invalid or earlier than the previous version one, it
can't be fixed automatically, so only an error is reported.

"""

import datetime
import pathlib
import re
import sys

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
CHANGELOG_PATH = ROOT_DIR / "CHANGELOG.md"
PYPROJECT_PATH = ROOT_DIR / "pyproject.toml"

CHANGELOG_DATE_FORMAT = "%d.%m.%y"
CHANGELOG_VERSION_REGEX = re.compile(
    r"^## (?P<version>\d+\.\d+\.\d+)\b(?: \((?P<date>[^)]*)\))?",
    flags=re.MULTILINE,
)
PROJECT_SECTION_REGEX = re.compile(
    r"^\[project\]\n(?P<body>.*?)(?=^\[|\Z)",
    flags=re.MULTILINE | re.DOTALL,
)
PROJECT_VERSION_REGEX = re.compile(
    r'^(?P<prefix>version\s*=\s*")(?P<version>[^"]*)(?P<suffix>")',
    flags=re.MULTILINE,
)


def parse_date(date: str | None) -> datetime.date | None:
    """Parse changelog release date, return `None` if it is invalid."""
    if not date:
        return None
    try:
        return datetime.datetime.strptime(date, CHANGELOG_DATE_FORMAT).date()
    except ValueError:
        return None


def check_release_date(
    changelog: str,
    latest: re.Match[str],
    previous: re.Match[str] | None,
) -> str | None:
    """Check latest release date, return message if it is fixed or incorrect.

    Missing date is set to today's one, other errors are only reported.

    """
    version = latest["version"]
    if latest["date"] is None:
        today = datetime.date.today().strftime(CHANGELOG_DATE_FORMAT)
        version_end = latest.end("version")
        CHANGELOG_PATH.write_text(
            f"{changelog[:version_end]} ({today}){changelog[version_end:]}",
        )
        return (
            f"Set missing release date of {version} "
            f"in {CHANGELOG_PATH.name}: {today}"
        )
    latest_date = parse_date(latest["date"])
    if not latest_date:
        return (
            f"Invalid release date of {version} ({latest['date']}) "
            f"in {CHANGELOG_PATH.name}, expected format: "
            f"`## {version} (DD.MM.YY)`"
        )
    previous_date = parse_date(previous["date"]) if previous else None
    if previous and previous_date and latest_date < previous_date:
        return (
            f"Release date of {version} ({latest['date']}) "
            f"in {CHANGELOG_PATH.name} is earlier than "
            f"release date of {previous['version']} ({previous['date']})"
        )
    return None


def sync_project_version(version: str) -> str | None:
    """Fix project version in pyproject, return message if it was changed."""
    pyproject = PYPROJECT_PATH.read_text()
    section_match = PROJECT_SECTION_REGEX.search(pyproject)
    version_match = (
        PROJECT_VERSION_REGEX.search(section_match["body"])
        if section_match
        else None
    )
    if not section_match or not version_match:
        return f"No `[project]` version found in {PYPROJECT_PATH.name}"
    project_version = version_match["version"]

    if project_version == version:
        return None

    body_start = section_match.start("body")
    version_start = body_start + version_match.start("version")
    version_end = body_start + version_match.end("version")
    PYPROJECT_PATH.write_text(
        pyproject[:version_start] + version + pyproject[version_end:],
    )
    return (
        f"Fixed version in {PYPROJECT_PATH.name}: "
        f"{project_version} -> {version} "
        f"(taken from {CHANGELOG_PATH.name})"
    )


def main() -> None:
    """Check release date and sync project version.

    Messages are reported via `sys.exit`, which writes them to stderr and
    exits with code 1.

    """
    changelog = CHANGELOG_PATH.read_text()
    releases = CHANGELOG_VERSION_REGEX.finditer(changelog)
    latest = next(releases, None)
    if not latest:
        return
    previous = next(releases, None)

    messages = [
        message
        for message in (
            check_release_date(changelog, latest, previous),
            sync_project_version(latest["version"]),
        )
        if message
    ]
    if messages:
        sys.exit("\n".join(messages))


if __name__ == "__main__":
    main()
