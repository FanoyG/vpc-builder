import boto3
from botocore.exceptions import ClientError
import ipaddress
import questionary
from cli.display import show_info, show_success, show_failure, show_warning
from cli.prompts import confirm_action
from cli.access import list_accessible_vpcs, verify_vpc_access
from cli.aws_client import AWSClient

def run_create_flow():
    ec2 = AWSClient.get_ec2_client()
    region = AWSClient._session.region_name  # current selected region

    show_info(f"Selected AWS Region: {region}")

    resource = questionary.select(
        "Which resource do you want to create?",
        choices=["VPC", "Internet Gateway", "Subnet", "Route Table", "NAT Gateway", "Security Group", "Exit"]
    ).ask()

    if resource == "VPC":
        create_vpc_flow(ec2)
    elif resource == "Internet Gateway":
        vpcs = list_accessible_vpcs(ec2)
        if not vpcs:
            show_failure("No accessible VPCs found. Cannot create Internet Gateway.")
            return

        vpc_id = select_vpc(ec2, vpcs)
        if not vpc_id:
            return

        create_internet_gateway_flow(ec2, vpc_id)

    elif resource == "Subnet":
        vpcs = list_accessible_vpcs(ec2)
        if not vpcs:
            show_failure("No accessible VPCs found. Cannot create Subnet.")
            return

        vpc_id = select_vpc(ec2, vpcs)
        if not vpc_id:
            return

        create_subnet_flow(ec2, vpc_id)

    elif resource == "Route Table":
        vpcs = list_accessible_vpcs(ec2)
        if not vpcs:
            show_failure("No accessible VPCs found. Cannot create Route Table.")
            return

        vpc_id = select_vpc(ec2, vpcs)
        if not vpc_id:
            return

        create_route_table_flow(ec2, vpc_id)

    elif resource == "NAT Gateway":
        vpcs = list_accessible_vpcs(ec2)
        if not vpcs:
            show_failure("No accessible VPCs found. Cannot create NAT Gateway.")
            return

        vpc_id = select_vpc(ec2, vpcs)
        if not vpc_id:
            return

        create_nat_gateway_flow(ec2, vpc_id)

    elif resource == "Security Group":
        vpcs = list_accessible_vpcs(ec2)
        if not vpcs:
            show_failure("No accessible VPCs found. Cannot create Security Group.")
            return

        vpc_id = select_vpc(ec2, vpcs)
        if not vpc_id:
            return

        create_security_group_flow(ec2, vpc_id)

    else:
        show_info("Create flow exited.")

def select_vpc(ec2, vpcs):
    try:
        response = ec2.describe_vpcs()
        vpcs = []
        for vpc in response.get("Vpcs", []):
            vpc_id = vpc.get("VpcId")
            name = None
            for tag in vpc.get("Tags", []):
                if tag["Key"] == "Name":
                    name = tag["Value"]
                    break
            vpcs.append((vpc_id, name))
    except Exception as e:
        show_failure(f"Failed to fetch VPCs: {str(e)}")
        return None

    choices = [f"{vpc_id} ({name})" if name else vpc_id for vpc_id, name in vpcs]
    vpc_choice = questionary.select("Select the VPC:", choices=choices).ask()
    if not vpc_choice:
        show_info("No VPC selected, exiting.")
        return None
    vpc_id = vpc_choice.split()[0]

    if not verify_vpc_access(ec2, vpc_id):
        show_failure(f"No access to VPC {vpc_id}")
        return None

    return vpc_id


def create_vpc_flow(ec2):
    show_info("Starting VPC creation...")

    vpc_name = questionary.text("Enter a name for your VPC (optional):").ask()

    while True:
        cidr_block = questionary.text("Enter CIDR block for VPC (e.g., 10.0.0.0/16):").ask()
        if validate_cidr(cidr_block):
            break
        else:
            show_failure("Invalid CIDR block format. Try again.")

    if not confirm_action(f"Create VPC '{vpc_name}' with CIDR {cidr_block}?"):
        show_info("VPC creation cancelled.")
        return

    try:
        vpc_resp = ec2.create_vpc(CidrBlock=cidr_block)
        vpc_id = vpc_resp['Vpc']['VpcId']

        if vpc_name:
            ec2.create_tags(Resources=[vpc_id], Tags=[{"Key": "Name", "Value": vpc_name}])

        show_success(f"VPC created successfully! VPC ID: {vpc_id}")

    except ClientError as e:
        show_failure(f"Error during creation: {e.response['Error']['Message']}")

def create_internet_gateway_flow(ec2, vpc_id):
    if not confirm_action(f"🌐 Create and attach an Internet Gateway to VPC {vpc_id}?"):
        show_info("⏹️ Internet Gateway creation cancelled.")
        return

    igw_name = questionary.text("📝 Enter a name for the Internet Gateway (optional):").ask()

    try:
        igw_resp = ec2.create_internet_gateway()
        igw_id = igw_resp['InternetGateway']['InternetGatewayId']

        # Tag with Name if provided
        tags = []
        if igw_name:
            tags.append({"Key": "Name", "Value": igw_name})
        if tags:
            ec2.create_tags(Resources=[igw_id], Tags=tags)

        ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
        show_success(f"✅ Internet Gateway '{igw_name or igw_id}' created and attached to VPC {vpc_id}!")


    except ClientError as e:
        show_failure(f"⚠️ Error during Internet Gateway creation: {e.response['Error']['Message']}")


def create_subnet_flow(ec2, vpc_id):
    show_info(f"📦 Creating Subnet(s) inside VPC {vpc_id}")

    num_subnets = questionary.text("🧮 How many subnets do you want to create?").ask()
    if not num_subnets.isdigit() or int(num_subnets) <= 0:
        show_failure("❌ Please enter a valid number greater than 0.")
        return

    num_subnets = int(num_subnets)

    if num_subnets == 2:
        subnet_types = ["public", "private"]
    else:
        pub_count = questionary.text("🌐 How many **public** subnets?").ask()
        pri_count = questionary.text("🔒 How many **private** subnets?").ask()

        if not pub_count.isdigit() or not pri_count.isdigit():
            show_failure("❌ Invalid numbers. Please enter digits only.")
            return

        subnet_types = ["public"] * int(pub_count) + ["private"] * int(pri_count)

        if len(subnet_types) != num_subnets:
            show_failure("❗ Total count mismatch. Check your numbers again.")
            return

    for idx, s_type in enumerate(subnet_types, start=1):
        show_info(f"⚙️ Configuring {s_type.upper()} Subnet #{idx}")

        while True:
            cidr_block = questionary.text(f"📍 Enter CIDR block for {s_type} Subnet #{idx} (e.g., 10.0.{idx}.0/24):").ask()
            if validate_cidr(cidr_block):
                break
            else:
                show_failure("❌ Invalid CIDR block format. Try again.")

        subnet_name = questionary.text(f"📝 Enter a name for the {s_type} Subnet #{idx}:").ask()

        if not confirm_action(f"✅ Confirm: Create {s_type} Subnet '{subnet_name}' with CIDR {cidr_block}?"):
            show_info("⏹️ Subnet creation skipped by user.")
            continue

        try:
            resp = ec2.create_subnet(VpcId=vpc_id, CidrBlock=cidr_block)
            subnet_id = resp['Subnet']['SubnetId']
            if subnet_name:
                ec2.create_tags(Resources=[subnet_id], Tags=[{"Key": "Name", "Value": subnet_name}, {"Key": "Type", "Value": s_type}])
            show_success(f"✅ {s_type.capitalize()} Subnet created! Subnet ID: {subnet_id}")
        except ClientError as e:
            show_failure(f"⚠️ Error creating {s_type} Subnet: {e.response['Error']['Message']}")

def create_route_table_flow(ec2, vpc_id):
    show_info(f"🛣️ Creating Route Table(s) inside VPC {vpc_id}")

    num_rts = questionary.text("🧮 How many Route Tables do you want to create?").ask()
    if not num_rts.isdigit() or int(num_rts) <= 0:
        show_failure("❌ Please enter a valid number greater than 0.")
        return

    num_rts = int(num_rts)

    for i in range(1, num_rts + 1):
        rt_type = questionary.select(
            f"🏷️ Is Route Table #{i} for Public or Private subnet?",
            choices=["public", "private"]
        ).ask()

        rt_name = questionary.text(f"📝 Enter a name for {rt_type} Route Table #{i} (optional):").ask()

        if not confirm_action(f"✅ Confirm: Create {rt_type} Route Table '{rt_name}'?"):
            show_info("⏹️ Route Table creation skipped by user.")
            continue

        try:
            resp = ec2.create_route_table(VpcId=vpc_id)
            rt_id = resp['RouteTable']['RouteTableId']
            tags = [{"Key": "Type", "Value": rt_type}]
            if rt_name:
                tags.append({"Key": "Name", "Value": rt_name})
            ec2.create_tags(Resources=[rt_id], Tags=tags)
            show_success(f"✅ {rt_type.capitalize()} Route Table created! ID: {rt_id}")
        except ClientError as e:
            show_failure(f"⚠️ Error during Route Table creation: {e.response['Error']['Message']}")


def create_nat_gateway_flow(ec2, vpc_id):
    show_info(f"Creating NAT Gateway inside VPC {vpc_id}")

    # You can add logic here to ask for subnet ID where NAT GW will be created
    subnet_id = questionary.text("Enter Subnet ID to create NAT Gateway in:").ask()

    if not confirm_action(f"Create NAT Gateway in subnet {subnet_id}? Note: This incurs AWS costs."):
        show_info("NAT Gateway creation cancelled.")
        return

    try:
        # Allocate Elastic IP for NAT Gateway
        ec2_client = boto3.client('ec2', region_name=AWSClient._region)
        eip = ec2_client.allocate_address(Domain='vpc')
        allocation_id = eip['AllocationId']

        # Create NAT Gateway
        resp = ec2.create_nat_gateway(SubnetId=subnet_id, AllocationId=allocation_id)
        nat_gw_id = resp['NatGateway']['NatGatewayId']

        show_success(f"NAT Gateway created successfully! ID: {nat_gw_id}")
    except ClientError as e:
        show_failure(f"Error during NAT Gateway creation: {e.response['Error']['Message']}")

def create_security_group_flow(ec2, vpc_id):
    show_info(f"Creating Security Group inside VPC {vpc_id}")

    sg_name = questionary.text("Enter Security Group name:").ask()
    sg_desc = questionary.text("Enter description for the Security Group:").ask()

    if not confirm_action(f"Create Security Group '{sg_name}' in VPC {vpc_id}?"):
        show_info("Security Group creation cancelled.")
        return

    try:
        resp = ec2.create_security_group(
            GroupName=sg_name,
            Description=sg_desc,
            VpcId=vpc_id
        )
        sg_id = resp['GroupId']
        show_success(f"Security Group created successfully! ID: {sg_id}")
    except ClientError as e:
        show_failure(f"Error during Security Group creation: {e.response['Error']['Message']}")

def validate_cidr(cidr):
    try:
        ipaddress.IPv4Network(cidr)
        return True
    except ValueError:
        return False
