import base64
import requests
import logging

class ClientCredentials:
    """Obtain client access token using the client_credentials grant."""

    def __init__(self, client_id: str, client_secret: str,
                 cert_crt_path: str, cert_key_path: str):
        auth_str = f"{client_id}:{client_secret}"
        self._basic_auth_header = "Basic " + base64.b64encode(auth_str.encode()).decode()
        self._cert = (cert_crt_path, cert_key_path)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("ClientCredentials initialized")

    def get_client_token(self, token_url: str) -> dict:
        """Request a client token."""
        data = {"grant_type": "client_credentials"}
        headers = {"Authorization": self._basic_auth_header}
        try:
            resp = requests.post(token_url, data=data, headers=headers, cert=self._cert)
        except Exception as exc:
            self.logger.error("Client token request failed: %s", exc)
            return {"status": None, "error": str(exc)}

        result = {"status": resp.status_code}
        if resp.status_code == 200:
            try:
                token_data = resp.json()
            except ValueError:
                token_data = {"response_xml": resp.text}
            result.update(token_data)
            self.logger.info("Client token obtained")
        else:
            result["error"] = resp.text
            self.logger.warning("Client token request failed: %s", resp.text)
        return result
