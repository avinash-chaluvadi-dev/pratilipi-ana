import logging
import os
import time

import requests

from app.core.exceptions import InternalServerError

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(levelname)s - %(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
stream_handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)


def decrypt(encrypted_txt: str) -> str:
    """
    Decrypts a config string using WorkOS config server endpoint

    :raises InternalServerError if there is an error while decrypting configs

    """
    decrypt_url = os.environ.get(
        "decryptUrl", "https://sit-interlock.anthem.com/pyutilconfig/decrypt"
    )
    cert = os.environ.get("PY_CERTS", "sit-interlock.anthem.com.cer")
    headers = {
        "Content-type": "text/plain",
        "authorization": "Basic ZG9ja2VyYWRtaW46ZDBjazNyQGRtMW4=",
    }
    try:
        decrypted_txt = requests.post(
            url=decrypt_url,
            verify=cert,
            headers=headers,
            data=encrypted_txt,
        )
        logger.info("String decrypted")
        return decrypted_txt.text
    except Exception as e:
        logger.error(f" Exception while decrypting configs {str(e)}")


def get_soa_configs() -> dict:
    """
    Loads application settings from WorkOS config server

    :raises InternalServerError if config server does not respond with 200 or
                                if there is an error while decrypting configs
    """
    config_url = os.environ.get(
        "configServerUrl",
        "https://sit-interlock.anthem.com/pyutilconfig/vmt-soa-gateway-uat,ekssit.json",
    )
    cert = os.environ.get("PY_CERTS", "sit-interlock.anthem.com.cer")
    try:
        config_bf_api_ts = time.time()
        config_resp = requests.get(url=config_url, verify=cert)
        logger.info(
            f"Total time taken for calling Config server : {time.time()-config_bf_api_ts:0.2f}s with response code : {config_resp.status_code}"
        )

    except Exception as e:
        logger.error(f" Exception while calling config endpoint {str(e)}")
        raise InternalServerError(
            "Error while loading settings from config server"
        )

    # Decrypt if any ciphers found
    if config_resp.status_code == 200:
        config_resp_json = config_resp.json()
        for (k, v) in config_resp_json.items():
            if str(v).strip().startswith("{" + "cipher" + "}"):
                decrypted_text = decrypt(v)
                config_resp_json[k] = decrypted_text

        return config_resp_json

    else:
        logger.error(
            f"Call to config server endpoint failed with status code : {config_resp.status_code} and error{config_resp.text} "
        )
