import pytest
from unittest.mock import patch
import cli.prompts as prompts

def test_select_vpc_prompt(monkeypatch):
    # Mock questionary.select().ask() to return a fixed vpc_id
    with patch("questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "vpc-1234"
        result = prompts.choose_vpc_prompt(["vpc-1234", "vpc-5678"])
        assert result == "vpc-1234"

def test_confirm_deletion_prompt(monkeypatch):
    with patch("questionary.confirm") as mock_confirm:
        mock_confirm.return_value.ask.return_value = True
        assert prompts.confirm_deletion("vpc-1234") is True

def test_select_resource_prompt(monkeypatch):
    with patch("questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "Subnets"
        resource = prompts.select_resource_prompt()
        assert resource == "Subnets"
