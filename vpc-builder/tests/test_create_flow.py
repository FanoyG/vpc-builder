import pytest
from unittest.mock import MagicMock, patch
from cli.create import create_vpc_flow, run_create_flow

def test_run_create_flow_creates_vpc():
    ec2_mock = MagicMock()
    with patch("cli.create.create_vpc") as mock_create_vpc, \
         patch("questionary.select") as mock_select:

        mock_select.return_value.ask.return_value = "VPC"
        mock_create_vpc.return_value = None

        run_create_flow(ec2_mock)

        mock_create_vpc.assert_called_once_with(ec2_mock)

def test_create_vpc_success(capsys):
    ec2_mock = MagicMock()
    create_vpc_flow = {"Vpc": {"VpcId": "vpc-1234"}}

    create_vpc_flow(ec2_mock)
    captured = capsys.readouterr()
    assert "VPC created with ID: vpc-1234" in captured.out
