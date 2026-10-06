"""Fetch configured Chandigarh public sources directly by URL.

The URL registry is data/external/REMOTE_URLS.yaml. Nothing in this tool
creates, substitutes, interpolates, or relabels observations. Failed requests
remain unavailable and the acquisition manifest records the failure.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, urllib.request, urllib.parse
from datetime import datetime, timezone
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "external" / "REMOTE_URLS.yaml"
OUT = ROOT / "data" / "raw" / "remote"
MANIFEST = ROOT / "data" / "raw" / "remote_acquisition_manifest.json"


def load_urls() -> dict[str, str]:
    data = yaml.safe_load(REGISTRY.read_text()) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Invalid source registry: {REGISTRY}")
    return {str(k): str(v) for k, v in data.items() if v}


def extension(url: str) -> str:
    path = urllib.parse.urlparse(url).path.lower()
    if path.endswith(".csv"):
        return ".csv"
    if path.endswith(".geojson") or "f=geojson" in url.lower():
        return ".geojson"
    return ".bin"


def fetch(name: str, url: str) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{name}{extension(url)}"
    record = {
        "name": name,
        "url": url,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "unavailable",
        "path": str(dest.relative_to(ROOT)),
    }
    req = urllib.request.Request(url, headers={"User-Agent": "CITYNEXUS-Chandigarh/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            content = response.read()
            dest.write_bytes(content)
            record.update({
                "status": "fetched",
                "http_status": getattr(response, "status", None),
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            })
        print(f"FETCHED {name}: {dest}")
    except Exception as exc:
        record["error"] = f"{type(exc).__name__}: {exc}"
        print(f"UNAVAILABLE {name}: {record['error']}")
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    urls = load_urls()
    parser.add_argument("--source", choices=["all", *urls], default="all")
    args = parser.parse_args()
    selected = urls.items() if args.source == "all" else [(args.source, urls[args.source])]
    records = [fetch(name, url) for name, url in selected]
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps({"generated_at_utc": datetime.now(timezone.utc).isoformat(), "sources": records}, indent=2))
    if any(r["status"] != "fetched" for r in records):
        raise SystemExit(2)
