import re
from dataclasses import dataclass
from datetime import datetime
from threading import Lock
from time import monotonic

import requests
from bs4 import BeautifulSoup

SOURCE_URL = (
    "https://polls.decisiondeskhq.com/averages/"
    "presidential-approval/donald-j.-trump-5/national/lv-rv-adults"
)
CACHE_SECONDS = 10 * 60
REQUEST_TIMEOUT = 20


class PollingDataError(RuntimeError):
    """Raised when the polling provider cannot supply usable data."""


@dataclass(frozen=True)
class PollingSnapshot:
    approve: float
    disapprove: float
    fetched_at: datetime

    @property
    def net_approval(self) -> float:
        return self.approve - self.disapprove


_cache_lock = Lock()
_cached_snapshot: PollingSnapshot | None = None
_cached_at = 0.0


def parse_polling_page(html: str) -> tuple[float, float]:
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    if "Donald Trump Approval Rating" not in text:
        raise PollingDataError("De verwachte Trump-peilingen zijn niet gevonden bij DDHQ.")

    values: dict[str, float] = {}
    for label in ("Approve", "Disapprove"):
        match = re.search(
            rf"Response {label}\s+(\d+(?:\.\d+)?)\s*%",
            text,
            flags=re.IGNORECASE,
        )
        if match is None:
            raise PollingDataError(
                f"Het percentage voor {label.lower()} kon niet uit de DDHQ-pagina worden gelezen."
            )

        value = float(match.group(1))
        if not 0 <= value <= 100:
            raise PollingDataError(
                f"DDHQ gaf een ongeldig percentage voor {label.lower()} terug."
            )
        values[label] = value

    return values["Approve"], values["Disapprove"]


def fetch_polling_snapshot() -> PollingSnapshot:
    try:
        response = requests.get(
            SOURCE_URL,
            headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise PollingDataError(
            "De peilingen konden niet worden opgehaald. Controleer je internetverbinding "
            "en probeer het later opnieuw."
        ) from error

    approve, disapprove = parse_polling_page(response.text)
    return PollingSnapshot(
        approve=approve,
        disapprove=disapprove,
        fetched_at=datetime.now().astimezone(),
    )


def get_polling_snapshot(force_refresh: bool = False) -> PollingSnapshot:
    global _cached_at, _cached_snapshot

    with _cache_lock:
        if (
            not force_refresh
            and _cached_snapshot is not None
            and monotonic() - _cached_at < CACHE_SECONDS
        ):
            return _cached_snapshot

        snapshot = fetch_polling_snapshot()
        _cached_snapshot = snapshot
        _cached_at = monotonic()
        return snapshot
