from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any

import requests


def build_basic_token(username: str, password: str) -> str:
    raw = f"{username}:{password}".encode("utf-8")
    return base64.b64encode(raw).decode("ascii")


@dataclass(frozen=True)
class ApiConfig:
    base_url: str


class ApiClient:
    def __init__(self, config: ApiConfig):
        self._base_url = config.base_url.rstrip("/")
        self._token: str | None = None

    def set_basic_token(self, token: str) -> None:
        self._token = token

    def clear_auth(self) -> None:
        self._token = None

    def _headers(self) -> dict[str, str]:
        if not self._token:
            return {}
        return {"Authorization": f"Basic {self._token}"}

    def get_me(self) -> dict[str, Any]:
        return self._get_json("/me/")

    def list_datasets(self, limit: int = 5) -> dict[str, Any]:
        limit = max(1, min(int(limit), 5))
        return self._get_json(f"/datasets/?limit={limit}")

    def upload_dataset(self, file_path: str) -> dict[str, Any]:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, "text/csv")}
            return self._post_multipart_json("/datasets/upload/", files=files)

    def get_summary(self, dataset_id: str) -> dict[str, Any]:
        return self._get_json(f"/datasets/{dataset_id}/summary/")

    def get_preview(self, dataset_id: str, limit: int = 50) -> dict[str, Any]:
        limit = max(1, min(int(limit), 500))
        return self._get_json(f"/datasets/{dataset_id}/preview/?limit={limit}")

    def download_report(self, dataset_id: str) -> bytes:
        url = f"{self._base_url}/datasets/{dataset_id}/report.pdf"
        res = requests.get(url, headers=self._headers(), timeout=60)
        if res.status_code == 401:
            raise RuntimeError("Unauthorized")
        if not res.ok:
            raise RuntimeError(res.text or f"Request failed ({res.status_code})")
        return res.content

    def _get_json(self, path: str) -> dict[str, Any]:
        url = f"{self._base_url}{path}"
        res = requests.get(url, headers=self._headers(), timeout=30)
        if res.status_code == 401:
            raise RuntimeError("Unauthorized")
        if not res.ok:
            raise RuntimeError(res.text or f"Request failed ({res.status_code})")
        return res.json()

    def _post_multipart_json(self, path: str, files: dict[str, Any]) -> dict[str, Any]:
        url = f"{self._base_url}{path}"
        res = requests.post(url, headers=self._headers(), files=files, timeout=120)
        if res.status_code == 401:
            raise RuntimeError("Unauthorized")
        if not res.ok:
            raise RuntimeError(res.text or f"Request failed ({res.status_code})")
        return res.json()
