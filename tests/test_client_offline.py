import os
import pytest
from demomed.client import DemoMedClient

def test_env_required(monkeypatch):
    monkeypatch.delenv("DEMOMED_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        DemoMedClient()
