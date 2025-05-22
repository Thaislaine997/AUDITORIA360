import pytest
from unittest.mock import patch, MagicMock
import src.painel as painel_mod

@pytest.fixture
def public_cfg_cliente_a():
    return {
        "RECAPTCHA_SITE_KEY": "sitekeyA",
        "client_display_name": "Cliente A",
        "branding_logo_url": "https://logoA.png"
    }

@pytest.fixture
def public_cfg_cliente_b():
    return {
        "RECAPTCHA_SITE_KEY": "sitekeyB",
        "client_display_name": "Cliente B",
        "branding_logo_url": "https://logoB.png"
    }

@patch("src.painel.fetch_public_config")
def test_white_label_config_cliente_a(mock_fetch, public_cfg_cliente_a):
    mock_fetch.return_value = public_cfg_cliente_a
    # Recarrega configs
    painel_mod.public_cfg = public_cfg_cliente_a
    painel_mod.RECAPTCHA_SITE_KEY = public_cfg_cliente_a["RECAPTCHA_SITE_KEY"]
    painel_mod.CLIENT_DISPLAY_NAME = public_cfg_cliente_a["client_display_name"]
    painel_mod.BRANDING_LOGO_URL = public_cfg_cliente_a["branding_logo_url"]
    assert painel_mod.RECAPTCHA_SITE_KEY == "sitekeyA"
    assert painel_mod.CLIENT_DISPLAY_NAME == "Cliente A"
    assert painel_mod.BRANDING_LOGO_URL == "https://logoA.png"

@patch("src.painel.fetch_public_config")
def test_white_label_config_cliente_b(mock_fetch, public_cfg_cliente_b):
    mock_fetch.return_value = public_cfg_cliente_b
    painel_mod.public_cfg = public_cfg_cliente_b
    painel_mod.RECAPTCHA_SITE_KEY = public_cfg_cliente_b["RECAPTCHA_SITE_KEY"]
    painel_mod.CLIENT_DISPLAY_NAME = public_cfg_cliente_b["client_display_name"]
    painel_mod.BRANDING_LOGO_URL = public_cfg_cliente_b["branding_logo_url"]
    assert painel_mod.RECAPTCHA_SITE_KEY == "sitekeyB"
    assert painel_mod.CLIENT_DISPLAY_NAME == "Cliente B"
    assert painel_mod.BRANDING_LOGO_URL == "https://logoB.png"
