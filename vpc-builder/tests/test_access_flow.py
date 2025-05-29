import pytest
from cli.access import (
    run_access_flow,
    get_vpc_by_id_or_name,
    get_vpc_by_name,
    list_acccessable_vpc,
    verify_vpc_access
)
from unittest.mock import patch


def test_run_access_flow_success():
    with patch("cli.access.verify_vpc_access") as mock_verify:
        mock_verify.return_value = True
        result = run_access_flow()
        assert result is not None or result is True  # Adjust based on your actual return


def test_get_vpc_by_id_or_name():
    vpcs = [
        {"VpcId": "vpc-123", "Tags": [{"Key": "Name", "Value": "dev"}]},
        {"VpcId": "vpc-456", "Tags": [{"Key": "Name", "Value": "prod"}]},
    ]
    assert get_vpc_by_id_or_name(vpcs, "vpc-123")["VpcId"] == "vpc-123"
    assert get_vpc_by_id_or_name(vpcs, "prod")["Tags"][0]["Value"] == "prod"


def test_get_vpc_by_name():
    vpcs = [
        {"VpcId": "vpc-1", "Tags": [{"Key": "Name", "Value": "alpha"}]},
        {"VpcId": "vpc-2", "Tags": [{"Key": "Name", "Value": "beta"}]},
    ]
    assert get_vpc_by_name(vpcs, "beta")["VpcId"] == "vpc-2"


def test_list_acccessable_vpc():
    mock_vpcs = [{"VpcId": "vpc-a"}, {"VpcId": "vpc-b"}]
    with patch("cli.access.boto3.client") as mock_boto:
        ec2 = mock_boto.return_value
        ec2.describe_vpcs.return_value = {"Vpcs": mock_vpcs}
        result = list_acccessable_vpc()
        assert result == mock_vpcs


def test_verify_vpc_access():
    vpcs = [{"VpcId": "vpc-1"}, {"VpcId": "vpc-2"}]
    assert verify_vpc_access(vpcs, "vpc-1") is True
    assert verify_vpc_access(vpcs, "vpc-x") is False
