import questionary
from botocore.exceptions import ClientError
from cli.display import show_info, show_success, show_failure
from cli.prompts import confirm_action
from cli.access import list_accessible_vpcs
from cli.aws_client import AWSClient
from cli.create import create_subnet_flow


def run_modify_flow():
    ec2 = AWSClient.get_ec2_client()
    show_info(f"Selected AWS Region: {AWSClient._session.region_name}")

    resource = questionary.select(
        "Select a resource to modify:",
        choices=["Subnet", "Route Table", "Attach IGW to Route Table"]
    ).ask()

    if resource == "Subnet":
        modify_subnet(ec2)
    elif resource == "Route Table":
        modify_route_table(ec2)
    elif resource == "Attach IGW to Route Table":
        attach_igw_to_route_table(ec2)
    else:
        show_failure("Invalid selection.")

    show_info("Returning to main menu...")


# ---------- SUBNET ----------
def modify_subnet(ec2):
    show_info("Modify Subnet")
    vpc_id = select_vpc(ec2)
    if not vpc_id:
        return

    choice = questionary.select(
        "Choose subnet action:",
        choices=["Add Subnet(s)", "Modify Tags", "Enable Auto-assign Public IP", "Associate with Route Table"]
    ).ask()

    if choice == "Add Subnet(s)":
        create_subnet_flow(ec2, vpc_id)
    elif choice == "Modify Tags":
        subnet_id = choose_subnet(ec2, vpc_id)
        if not subnet_id:
            return
        new_name = questionary.text("Enter new name tag:").ask()
        ec2.create_tags(Resources=[subnet_id], Tags=[{"Key": "Name", "Value": new_name}])
        show_success(f"Subnet renamed to {new_name}")
    elif choice == "Enable Auto-assign Public IP":
        subnet_id = choose_subnet(ec2, vpc_id)
        if not subnet_id:
            return
        ec2.modify_subnet_attribute(SubnetId=subnet_id, MapPublicIpOnLaunch={"Value": True})
        show_success("Auto-assign Public IP enabled.")
    elif choice == "Associate with Route Table":
        associate_subnet_with_route_table(ec2, vpc_id)

def associate_subnet_with_route_table(ec2, vpc_id):
    show_info("Associate Subnet with Route Table")

    if not (subnet_id := choose_subnet(ec2, vpc_id)):
        return

    try:
        rtables = ec2.describe_route_tables(
            Filters=[{"Name": "association.subnet-id", "Values": [subnet_id]}]
        )["RouteTables"]

        if rtables:
            current_rt = rtables[0]["RouteTableId"]
            association_id = rtables[0]['Associations'][0]['RouteTableAssociationId']
            show_info(f"Subnet is currently associated with Route Table: {current_rt}")

            if not questionary.confirm("Do you want to replace the association?").ask():
                show_info("Operation cancelled.")
                return

            # Optional: Explicitly disassociate
            ec2.disassociate_route_table(AssociationId=association_id)

    except ClientError as e:
        show_failure(f"Failed to check or disassociate: {e.response['Error']['Message']}")
        return

    if not (route_table_id := choose_route_table(ec2, vpc_id)):
        return

    try:
        ec2.associate_route_table(SubnetId=subnet_id, RouteTableId=route_table_id)
        show_success(f"Subnet {subnet_id} is now associated with Route Table {route_table_id}.")
    except ClientError as e:
        show_failure(f"Association failed: {e.response['Error']['Message']}")


# ---------- ROUTE TABLE ----------
def modify_route_table(ec2):
    show_info("Modify Route Table")
    vpc_id = select_vpc(ec2)
    if not vpc_id:
        return

    rt_id = choose_route_table(ec2, vpc_id)
    if not rt_id:
        return

    choice = questionary.select(
        "Select route table action:",
        choices=["Add Route", "Delete Route", "Rename Route Table"]
    ).ask()

    try:
        if choice == "Add Route":
            cidr = questionary.text("Destination CIDR:").ask()
            target = questionary.text("Target (e.g. igw-xxx):").ask()
            ec2.create_route(RouteTableId=rt_id, DestinationCidrBlock=cidr, GatewayId=target)
            show_success("Route added.")
        elif choice == "Delete Route":
            cidr = questionary.text("CIDR to delete:").ask()
            ec2.delete_route(RouteTableId=rt_id, DestinationCidrBlock=cidr)
            show_success("Route deleted.")
        elif choice == "Rename Route Table":
            new_name = questionary.text("New name:").ask()
            ec2.create_tags(Resources=[rt_id], Tags=[{"Key": "Name", "Value": new_name}])
            show_success("Route Table renamed.")


    except ClientError as e:
        show_failure(f"Route Table update failed: {e.response['Error']['Message']}")


# ---------- IGW ATTACH ----------
def attach_igw_to_route_table(ec2):
    show_info("Attach IGW to Route Table")
    vpc_id = select_vpc(ec2)
    if not vpc_id:
        return

    rt_id = choose_route_table(ec2, vpc_id)
    igw_id = choose_igw(ec2, vpc_id)
    if not rt_id or not igw_id:
        return

    try:
        ec2.create_route(RouteTableId=rt_id, DestinationCidrBlock="0.0.0.0/0", GatewayId=igw_id)
        show_success("IGW attached successfully.")
    except ClientError as e:
        show_failure(f"Attach IGW failed: {e.response['Error']['Message']}")


# ---------- HELPERS ----------
def select_vpc(ec2):
    vpcs = list_accessible_vpcs(ec2)
    if not vpcs:
        show_failure("No VPCs found.")
        return None
    choices = [
        questionary.Choice(title=f"{vpc_id} ({name})" if name else vpc_id, value=vpc_id)
        for vpc_id, name in vpcs
    ]
    return questionary.select("Select VPC:", choices=choices).ask()


def choose_subnet(ec2, vpc_id):
    subnets = list_subnets(ec2, vpc_id)
    if not subnets:
        show_failure("No subnets found.")
        return None
    choices = [
        questionary.Choice(title=f"{subnet_id} ({name})" if name else subnet_id, value=subnet_id)
        for subnet_id, name in subnets
    ]
    return questionary.select("Select Subnet:", choices=choices).ask()


def choose_route_table(ec2, vpc_id):
    rtables = list_route_tables(ec2, vpc_id)
    if not rtables:
        show_failure("No route tables found.")
        return None
    choices = [
        questionary.Choice(title=f"{rt_id} ({name})" if name else rt_id, value=rt_id)
        for rt_id, name in rtables
    ]
    return questionary.select("Select Route Table:", choices=choices).ask()


def choose_igw(ec2, vpc_id):
    igws = list_internet_gateways(ec2, vpc_id)
    if not igws:
        show_failure("No IGWs found.")
        return None
    choices = [
        questionary.Choice(title=f"{igw_id} ({name})" if name else igw_id, value=igw_id)
        for igw_id, name in igws
    ]
    return questionary.select("Select IGW:", choices=choices).ask()


def list_subnets(ec2, vpc_id):
    try:
        subnets = ec2.describe_subnets(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])['Subnets']
        return [
            (s['SubnetId'], next((t['Value'] for t in s.get('Tags', []) if t['Key'] == 'Name'), ''))
            for s in subnets
        ]
    except ClientError as e:
        show_failure(f"List subnets failed: {e.response['Error']['Message']}")
        return []


def list_route_tables(ec2, vpc_id):
    try:
        rtables = ec2.describe_route_tables(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])['RouteTables']
        return [
            (rt['RouteTableId'], next((t['Value'] for t in rt.get('Tags', []) if t['Key'] == 'Name'), ''))
            for rt in rtables
        ]
    except ClientError as e:
        show_failure(f"List route tables failed: {e.response['Error']['Message']}")
        return []


def list_internet_gateways(ec2, vpc_id):
    try:
        igws = ec2.describe_internet_gateways(Filters=[{"Name": "attachment.vpc-id", "Values": [vpc_id]}])['InternetGateways']
        return [
            (igw['InternetGatewayId'], next((t['Value'] for t in igw.get('Tags', []) if t['Key'] == 'Name'), ''))
            for igw in igws
        ]
    except ClientError as e:
        show_failure(f"List IGWs failed: {e.response['Error']['Message']}")
        return []
