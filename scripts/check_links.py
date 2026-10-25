"""Check repository Markdown paths, GitHub fragments, images and source records.

Uses only Python's standard library. Network checks are opt-in because publisher
rate limits and bot protection cannot reliably determine whether a source exists.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import html
import json
import os
from pathlib import Path
import re
import sys
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen


def prose(text, hide_inline=True):
    """Hide examples without changing line numbers used in diagnostics."""
    lines, fence = [], None
    for line in text.splitlines(keepends=True):
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            lines.append("\n" if line.endswith("\n") else "")
        elif fence:
            lines.append("\n" if line.endswith("\n") else "")
        else:
            lines.append(line)
    result = "".join(lines)
    return re.sub(r"(`+).*?\1", "", result) if hide_inline else result


def slug(heading):
    heading = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", heading)
    heading = html.unescape(re.sub(r"<[^>]*>", "", heading)).lower().strip()
    return "".join(c for c in heading if c in " -_" or
                   unicodedata.category(c)[0] in "LN").replace(" ", "-")


def anchors(text):
    text = prose(text, hide_inline=False)
    found = set(re.findall(r'\b(?:id|name)=["\']([^"\']+)["\']', text))
    used = set()
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            base = slug(match[1])
            value, suffix = base, 0
            while value in used:
                suffix += 1
                value = f"{base}-{suffix}"
            used.add(value)
            found.add(value)
    return found


def links(text):
    text = prose(text)
    definitions = {m[1].strip().lower(): m[2] or m[3] for m in re.finditer(
        r'^\s{0,3}\[([^\]]+)\]:\s*(?:<([^>]+)>|(\S+))', text, re.M)}
    # Balanced parentheses support URLs such as article_(version).md.
    for match in re.finditer(r"\]\(", text):
        start, pos, depth = match.end(), match.end(), 1
        while pos < len(text) and depth:
            if text[pos] == "\\":
                pos += 2
                continue
            if text[pos] == "(":
                depth += 1
            elif text[pos] == ")":
                depth -= 1
            pos += 1
        if depth:
            yield text.count("\n", 0, match.start()) + 1, "!MALFORMED"
            continue
        dest = text[start:pos - 1].strip()
        if dest.startswith("<"):
            dest = dest[1:dest.find(">")]
        else:
            dest = re.split(r'\s+["\']', dest, maxsplit=1)[0]
        yield text.count("\n", 0, match.start()) + 1, html.unescape(dest)
    for match in re.finditer(r'\b(?:href|src)=["\']([^"\']+)["\']', text):
        yield text.count("\n", 0, match.start()) + 1, html.unescape(match[1])
    for match in re.finditer(r"!?\[([^\]\n]+)\]\[([^\]\n]*)\]", text):
        key = (match[2] or match[1]).strip().lower()
        yield text.count("\n", 0, match.start()) + 1, definitions.get(key, "!UNDEFINED:" + key)
    for match in re.finditer(r"^\s{0,3}\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))", text, re.M):
        yield text.count("\n", 0, match.start()) + 1, match[1] or match[2]
    for match in re.finditer(r"https?://[^\s<>\]\"']+", text):
        yield text.count("\n", 0, match.start()) + 1, match[0].rstrip(".,;)")


def exact_path(root, path):
    """Windows also needs case checks: GitHub paths are case sensitive."""
    current = root
    for part in path.relative_to(root).parts:
        if not current.is_dir() or part not in {p.name for p in current.iterdir()}:
            return False
        current /= part
    return True


def audit(root):
    errors, external, count, files = [], set(), 0, []
    for file in sorted(root.rglob("*.md")):
        if ".git" in file.relative_to(root).parts:
            continue
        files.append(file)
        text = file.read_text(encoding="utf-8-sig")
        if re.search(r"\[\[FN\d+\]\]", text):
            errors.append(f"{file.relative_to(root)}: unresolved editorial footnote")
        for line, dest in links(text):
            if dest.startswith("!MALFORMED") or dest.startswith("!UNDEFINED"):
                errors.append(f"{file.relative_to(root)}:{line}: {dest}")
                continue
            parsed = urlsplit(dest)
            if parsed.scheme in ("http", "https"):
                external.add(dest.split("#", 1)[0])
                continue
            if parsed.scheme in ("mailto", "tel"):
                continue
            count += 1
            raw = unquote(parsed.path)
            target = Path(os.path.abspath((root / raw.lstrip("/")) if raw.startswith("/") else
                                         (file.parent / raw) if raw else file))
            if (not target.is_relative_to(root) or not exact_path(root, target)
                    or not target.resolve().is_relative_to(root)):
                errors.append(f"{file.relative_to(root)}:{line}: missing or mis-cased path: {dest}")
            elif parsed.fragment and target.suffix.lower() == ".md":
                fragment = unquote(parsed.fragment)
                if fragment not in anchors(target.read_text(encoding="utf-8-sig")):
                    errors.append(f"{file.relative_to(root)}:{line}: missing fragment: {dest}")
    inventory = root / "research/05_Research_Source_Inventory.json"
    if inventory.exists():
        try:
            data = json.loads(inventory.read_text(encoding="utf-8-sig"))
            ids = []
            for group in data.values():
                if isinstance(group, dict):
                    for source in group.get("sources", []):
                        ids.append(source["id"])
                        if not source.get("access") or not source.get("url"):
                            errors.append(f"{source['id']}: missing source access note or URL")
                        external.add(source["url"].split("#", 1)[0])
            if len(ids) != len(set(ids)):
                errors.append("Duplicate source IDs in inventory")
        except (ValueError, KeyError) as error:
            errors.append(f"Invalid source inventory: {error}")
    return {"markdown_files": len(files), "local_links": count,
            "external_urls": sorted(external), "errors": errors}


def check_external(url):
    try:
        request = Request(url, headers={"User-Agent": "Project-Gateway-Link-Audit/1.0"})
        with urlopen(request, timeout=20) as response:
            return {"url": url, "status": response.status, "final_url": response.url}
    except HTTPError as error:
        return {"url": url, "status": error.code, "note": "Manual review required; a blocked request is not proof of a missing source."}
    except (URLError, TimeoutError, OSError) as error:
        return {"url": url, "status": "unverified", "note": str(error)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--external", action="store_true", help="Also report live URL availability; failures require manual review")
    parser.add_argument("--report", type=Path, help="Save a JSON audit report")
    args = parser.parse_args()
    result = audit(args.root.resolve())
    if args.external:
        with ThreadPoolExecutor(max_workers=6) as pool:
            result["external_checks"] = list(pool.map(check_external, result["external_urls"]))
    if args.report:
        args.report.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Checked {result['markdown_files']} Markdown files and {result['local_links']} local links/images/fragments.")
    for error in result["errors"]:
        print(error)
    if args.external:
        checks = result["external_checks"]
        available = sum(isinstance(x['status'], int) and 200 <= x['status'] < 300 for x in checks)
        print(f"Live URL checks: {available}/{len(checks)} returned HTTP 2xx. Review redirects and other results in the report.")
    print("PASS" if not result["errors"] else "FAIL")
    return bool(result["errors"])


if __name__ == "__main__":
    sys.exit(main())
