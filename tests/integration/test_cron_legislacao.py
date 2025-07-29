from automation.cron_legislacao import buscar_legislacao_diaria


def test_buscar_legislacao_diaria(monkeypatch, tmp_path):
    class MockResponse:
        text = '{"lei": "Teste"}'

    def mock_get(url):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    tmp_file = tmp_path / "2025-07-23.json"
    # Monkeypatch open para salvar no tmp_path
    monkeypatch.setattr("builtins.open", lambda f, mode: tmp_file.open(mode))
    buscar_legislacao_diaria()
    assert tmp_file.read_text() == '{"lei": "Teste"}'
