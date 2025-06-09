import requests
import logging

class Api:
    """Interact with PG&E usage data endpoints."""

    def __init__(self, cert_crt_path: str, cert_key_path: str):
        self._cert = (cert_crt_path, cert_key_path)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Api initialized")

    def sync_request(self, base_url: str, subscription_id: str, usage_point_id: str,
                     published_min: str, published_max: str, access_token: str) -> dict:
        url = f"{base_url}/Subscription/{subscription_id}/UsagePoint/{usage_point_id}"
        url += f"?published-min={published_min}&published-max={published_max}"
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            resp = requests.get(url, headers=headers, cert=self._cert)
        except Exception as exc:
            self.logger.error("Sync request failed: %s", exc)
            return {"status": None, "error": str(exc)}

        result = {"status": resp.status_code}
        if resp.status_code == 200:
            result["data"] = resp.text
            self.logger.info("Sync data retrieved")
        else:
            result["error"] = resp.text
            self.logger.warning("Sync request failed: %s", resp.text)
        return result

    def async_request(self, base_url: str, subscription_id: str,
                      published_min: str, published_max: str, access_token: str) -> dict:
        url = f"{base_url}/Subscription/{subscription_id}"
        url += f"?published-min={published_min}&published-max={published_max}"
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            resp = requests.get(url, headers=headers, cert=self._cert)
        except Exception as exc:
            self.logger.error("Async request failed: %s", exc)
            return {"status": None, "error": str(exc)}

        result = {"status": resp.status_code}
        if resp.status_code in (200, 202):
            result["data"] = resp.text
            self.logger.info("Async request initiated")
        else:
            result["error"] = resp.text
            self.logger.warning("Async request failed: %s", resp.text)
        return result
