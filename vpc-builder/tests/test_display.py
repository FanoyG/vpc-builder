import pytest
from cli import display

def test_show_info(capsys):
    display.show_info("Test info message")
    captured = capsys.readouterr()
    assert "Test info message" in captured.out

def test_show_success(capsys):
    display.show_success("Success message")
    captured = capsys.readouterr()
    assert "Success message" in captured.out

def test_show_failure(capsys):
    display.show_failure("Failure message")
    captured = capsys.readouterr()
    assert "Failure message" in captured.out
