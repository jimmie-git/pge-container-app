import base64
import requests
import logging

class OAuth2:
    """Handle PG&E OAuth2 authorization code and refresh flows."""

    def __init__(self, client_id: str, client_secret: str,
                 cert_crt_path: str, cert_key_path: str):
        auth_str = f"{client_id}:{client_secret}"
        self._basic_auth_header = "Basic " + base64.b64encode(auth_str.encode()).decode()
        self._cert = (cert_crt_path, cert_key_path)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("OAuth2 initialized")

    def get_access_token(self, token_url: str, auth_code: str, redirect_uri: str) -> dict:
        """Exchange authorization code for access token."""
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri
        }
        headers = {"Authorization": self._basic_auth_header}
        try:
            resp = requests.post(token_url, data=data, headers=headers, cert=self._cert)
        except Exception as exc:
            self.logger.error("Access token request failed: %s", exc)
            return {"status": None, "error": str(exc)}

        result = {"status": resp.status_code}
        if resp.status_code == 200:
            try:
                token_data = resp.json()
            except ValueError:
                token_data = {"response_xml": resp.text}
            result.update(token_data)
            self.logger.info("Access token obtained")
        else:
            result["error"] = resp.text
            self.logger.warning("Access token request failed: %s", resp.text)
        return result

    def get_refresh_token(self, token_url: str, refresh_token: str) -> dict:
        """Use refresh token to obtain new access token."""
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        headers = {"Authorization": self._basic_auth_header}
        try:
            resp = requests.post(token_url, data=data, headers=headers, cert=self._cert)
        except Exception as exc:
            self.logger.error("Refresh token request failed: %s", exc)
            return {"status": None, "error": str(exc)}

        result = {"status": resp.status_code}
        if resp.status_code == 200:
            try:
                token_data = resp.json()
            except ValueError:
                token_data = {"response_xml": resp.text}
            result.update(token_data)
            self.logger.info("Token refreshed")
        else:
            result["error"] = resp.text
            self.logger.warning("Refresh token request failed: %s", resp.text)
        return result
