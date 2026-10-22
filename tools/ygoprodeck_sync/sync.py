#!/usr/bin/env python3
"""
Jo-Ey-Sim - YGOProDeck sync skeleton.

Checks DB version, paginates cardinfo, prepares image queues.
Does NOT yet write the final CDB (v1 work in progress).

License: MIT (this file only). See ../../LICENSING.md.
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any, Iterator, Optional

import requests

LOG = logging.getLogger("ygoprodeck_sync")

DEFAULT_CONFIG = {
    "api": {
        "base_url": "https://db.ygoprodeck.com/api/v7",
        "rate_limit_per_second": 15,
    },
    "paths": {
        "official_data": "data/official",
        "images": "data/images/ygoprodeck",
        "logs": "logs",
    },
}


def load_config(path: Optional[Path]) -> dict:
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    if path and path.exists():
        deep_merge(cfg, json.loads(path.read_text(encoding="utf-8")))
    return cfg


def deep_merge(dst: dict, src: dict) -> None:
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            deep_merge(dst[k], v)
        else:
            dst[k] = v


def setup_logging(log_dir: Path) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "ygoprodeck_sync.log", encoding="utf-8"),
        ],
    )


class RateLimiter:
    def __init__(self, per_second: int) -> None:
        self.min_interval = 1.0 / per_second
        self._last = 0.0

    def wait(self) -> None:
        now = time.monotonic()
        delta = now - self._last
        if delta < self.min_interval:
            time.sleep(self.min_interval - delta)
        self._last = time.monotonic()


class YgoProDeckClient:
    def __init__(self, cfg: dict) -> None:
        self.base = cfg["api"]["base_url"].rstrip("/")
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "Jo-Ey-Sim/0.2 (ygoprodeck_sync)"
        self.limiter = RateLimiter(int(cfg["api"].get("rate_limit_per_second", 15)))

    def get(self, path: str, params: Optional[dict] = None) -> requests.Response:
        url = self.base + "/" + path.lstrip("/")
        last_resp = None
        for attempt in range(4):
            self.limiter.wait()
            resp = self.session.get(url, params=params, timeout=30)
            last_resp = resp
            if resp.status_code >= 500:
                backoff = 2 ** attempt
                LOG.warning("Server %s for %s, retrying in %ss", resp.status_code, url, backoff)
                time.sleep(backoff)
                continue
            if resp.status_code == 429:
                LOG.warning("Rate limited, sleeping 60s")
                time.sleep(60)
                continue
            resp.raise_for_status()
            return resp
        if last_resp is not None:
            last_resp.raise_for_status()
        raise RuntimeError("unreachable")

    def check_db_version(self) -> dict:
        return self.get("checkDBVer.php").json()

    def iter_cardinfo(self, page_size: int = 100) -> Iterator[list]:
        offset = 0
        while True:
            LOG.info("Fetching cardinfo offset=%s num=%s", offset, page_size)
            resp = self.get("cardinfo.php", {"num": page_size, "offset": offset})
            payload = resp.json()
            data = payload.get("data", [])
            if not data:
                return
            yield data
            meta = payload.get("meta") or {}
            if not meta.get("next_page"):
                return
            offset = int(meta.get("next_page_offset", offset + page_size))


def cmd_check(cfg: dict) -> int:
    client = YgoProDeckClient(cfg)
    LOG.info("YGOProDeck DB version: %s", json.dumps(client.check_db_version()))
    return 0


def cmd_full(cfg: dict) -> int:
    client = YgoProDeckClient(cfg)
    out_dir = Path(cfg["paths"]["official_data"])
    out_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    for page in client.iter_cardinfo():
        total += len(page)
        LOG.info("Page received: %s cards (total=%s)", len(page), total)
        (out_dir / ("cardinfo.page.%06d.json" % total)).write_text(
            json.dumps(page, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    manifest = {
        "total_cards": total,
        "source": "ygoprodeck",
        "version": client.check_db_version(),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (out_dir / "sync.manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    LOG.info("Sync finished: %s cards", total)
    return 0


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="YGOProDeck sync for Jo-Ey-Sim")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--cards-only", action="store_true")
    parser.add_argument("--images-only", action="store_true")
    args = parser.parse_args(argv)

    cfg = load_config(args.config)
    setup_logging(Path(cfg["paths"]["logs"]))

    if args.check:
        return cmd_check(cfg)
    if args.full or args.cards_only:
        return cmd_full(cfg)
    if args.images_only:
        LOG.error("Image sync not implemented yet (v1). See tools/image_fetch/.")
        return 2

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
