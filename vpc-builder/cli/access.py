from botocore.exceptions import ClientError
from cli.aws_client import AWSClient
from cli.prompts import confirm_action
from cli.display import show_info, show_success, show_failure

def run_access_flow():
    show_info("You chose to access an existing VPC.")

    ec2 = AWSClient.get_ec2_client()
    region = AWSClient._session.region_name  # current selected region

    vpc_input = input("Enter the VPC ID or Name: ").strip()
    if not vpc_input:
        show_failure("VPC ID or Name cannot be empty.")
        return

    show_info(f"Searching for VPC: {vpc_input} in region {region}...")

    vpc = get_vpc_by_id_or_name(ec2, vpc_input)

    if vpc:
        show_success(f"✅ Found VPC: {vpc['VpcId']} (CIDR: {vpc['CidrBlock']})")
    else:
        show_failure("❌ VPC not found.")

def get_vpc_by_id_or_name(ec2_client, vpc_input: str):
    try:
        # Try lookup by VPC ID first
        response = ec2_client.describe_vpcs(VpcIds=[vpc_input])
        return response["Vpcs"][0] if response["Vpcs"] else None
    except ClientError as e:
        if "InvalidVpcID.NotFound" in str(e):
            return get_vpc_by_name(ec2_client, vpc_input)
        else:
            show_failure(f"AWS Error: {str(e)}")
            return None

def get_vpc_by_name(ec2_client, name: str):
    try:
        response = ec2_client.describe_vpcs(
            Filters=[{"Name": "tag:Name", "Values": [name]}]
        )
        return response["Vpcs"][0] if response["Vpcs"] else None
    except ClientError as e:
        show_failure(f"AWS Error: {str(e)}")
        return None

def list_accessible_vpcs(ec2):
    """Return list of (vpc_id, vpc_name) tuples user can access in selected region."""
    vpcs = []
    try:
        response = ec2.describe_vpcs()
        for vpc in response['Vpcs']:
            vpc_id = vpc['VpcId']
            name_tag = next((t['Value'] for t in vpc.get('Tags', []) if t['Key'] == 'Name'), '')
            vpcs.append((vpc_id, name_tag))
    except ClientError as e:
        show_failure(f"Error fetching VPCs: {e.response['Error']['Message']}")
    return vpcs

def verify_vpc_access(ec2, vpc_id: str) -> bool:
    # Dummy for now, assume access granted
    return True

