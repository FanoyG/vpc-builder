import questionary
from botocore.exceptions import ClientError
from cli.display import show_info, show_success, show_failure
from cli.access import list_accessible_vpcs
from cli.aws_client import AWSClient


def run_delete_flow(ec2):
    show_info("Delete AWS Resources")

    choice = questionary.select(
        "What would you like to delete?",
        choices=["Entire VPC", "Specific Resources"]
    ).ask()

    if choice == "Entire VPC":
        delete_entire_vpc(ec2)
    else:
        delete_specific_resources(ec2)


def choose_vpc(ec2):
    accessible_vpcs = list_accessible_vpcs(ec2)

    if not accessible_vpcs:
        show_info("No accessible VPCs found.")
        return None

    choices = [
        questionary.Choice(title=f"{vpc_id} — {vpc_name}", value=vpc_id)
        for vpc_id, vpc_name in accessible_vpcs
    ]

    vpc_id = questionary.select(
        "Select a VPC:",
        choices=choices
    ).ask()

    return vpc_id


def delete_entire_vpc(ec2):
    vpc_id = choose_vpc(ec2)
    if not vpc_id:
        return

    confirm = questionary.confirm(
        f"Are you sure you want to delete VPC {vpc_id} and all its associated resources?"
    ).ask()

    if not confirm:
        show_info("Deletion cancelled.")
        return

    try:
        delete_subnets_in_vpc(ec2, vpc_id)
        delete_route_tables_in_vpc(ec2, vpc_id)
        delete_internet_gateways_in_vpc(ec2, vpc_id)
        delete_security_groups_in_vpc(ec2, vpc_id)

        ec2.delete_vpc(VpcId=vpc_id)
        show_success(f"VPC {vpc_id} and all related resources deleted successfully.")
    except Exception as e:
        show_failure(f"Failed to delete VPC: {str(e)}")


def delete_specific_resources(ec2):
    vpc_id = choose_vpc(ec2)
    if not vpc_id:
        return

    resource_choice = questionary.select(
        "Select the resource type to delete:",
        choices=["Subnets", "Route Tables", "Internet Gateways", "Security Groups"]
    ).ask()

    try:
        if resource_choice == "Subnets":
            delete_subnets_in_vpc(ec2, vpc_id)
        elif resource_choice == "Route Tables":
            delete_route_tables_in_vpc(ec2, vpc_id)
        elif resource_choice == "Internet Gateways":
            delete_internet_gateways_in_vpc(ec2, vpc_id)
        elif resource_choice == "Security Groups":
            delete_security_groups_in_vpc(ec2, vpc_id)
        else:
            show_failure("Invalid choice.")
    except Exception as e:
        show_failure(f"Failed to delete {resource_choice}: {str(e)}")


# Generic function to list resources from a describe call with filters and key path
def list_resources(ec2, describe_func_name, filter_key, filter_values, response_key):
    """
    Calls the specified describe function on ec2 client, filters by filter_key and filter_values,
    and returns the list of resources under response_key.
    """
    describe_func = getattr(ec2, describe_func_name)
    filters = [{"Name": filter_key, "Values": filter_values}]
    response = describe_func(Filters=filters)
    return response.get(response_key, [])


# Generic deletion helper for resources with a delete function and ID key
def delete_resources(resources, id_key, delete_func, skip_condition=None, disassociate_func=None, disassociate_key=None):
    """
    resources: list of resource dicts
    id_key: key to get resource ID
    delete_func: callable to delete resource, must accept resource ID as keyword argument
    skip_condition: callable(resource) -> bool, if True, skip deletion
    disassociate_func: callable to disassociate resource (optional)
    disassociate_key: key for disassociate identifier (optional)
    """
    if not resources:
        show_info("No resources found.")
        return

    for resource in resources:
        resource_id = resource[id_key]

        if skip_condition and skip_condition(resource):
            show_info(f"Skipping {resource_id} due to skip condition.")
            continue

        try:
            if disassociate_func and disassociate_key:
                # Disassociate all associations except main, if any
                for assoc in resource.get("Associations", []):
                    if not assoc.get("Main", False):
                        disassociate_func(AssociationId=assoc[disassociate_key])
            delete_func(**{id_key: resource_id})
            show_success(f"Deleted {resource_id}")
        except ClientError as e:
            show_failure(f"Failed to delete {resource_id}: {e.response['Error']['Message']}")

def delete_subnets_in_vpc(ec2, vpc_id):
    show_info("Fetching subnets...")

    subnets = list_resources(ec2, "describe_subnets", "vpc-id", [vpc_id], "Subnets")
    if not subnets:
        show_info("No subnets found in the VPC.")
        return

    choices = []
    subnet_map = {}
    for subnet in subnets:
        subnet_id = subnet.get("SubnetId")
        subnet_map[subnet_id] = subnet
        name = None
        for tag in subnet.get("Tags", []):
            if tag["Key"] == "Name":
                name = tag["Value"]
                break
        label = f"{subnet_id} ({name})" if name else subnet_id
        choices.append(questionary.Choice(title=label, value=subnet_id))

    print("DEBUG: Choices passed to checkbox prompt:")
    for c in choices:
        print(f" - {c.title} (value={c.value})")

    selected_ids = questionary.checkbox(
        "Select subnets to delete:",
        choices=choices
    ).ask()


    # Handle None (user cancelled or prompt failed)
    if selected_ids is None or not selected_ids:
        show_info("No subnets selected for deletion.")
        print("DEBUG: No selection or user cancelled the prompt.")
        return

    show_info(f"User selected {len(selected_ids)} subnet(s) for deletion: {selected_ids}")

    for subnet_id in selected_ids:
        try:
            ec2.delete_subnet(SubnetId=subnet_id)
            show_success(f"Deleted subnet: {subnet_id}")
        except Exception as e:
            show_failure(f"Failed to delete subnet {subnet_id}: {str(e)}")


def delete_route_tables_in_vpc(ec2, vpc_id):
    show_info("Fetching route tables...")

    rtables = list_resources(ec2, "describe_route_tables", "vpc-id", [vpc_id], "RouteTables")

    # Filter out main route tables
    non_main_rtables = []
    for rt in rtables:
        is_main = any(assoc.get("Main", False) for assoc in rt.get("Associations", []))
        if not is_main:
            non_main_rtables.append(rt)

    if not non_main_rtables:
        show_info("No non-main route tables found to delete.")
        return

    # Prepare choices for selection
    choices = []
    for rt in non_main_rtables:
        rt_id = rt.get("RouteTableId")
        name = None
        for tag in rt.get("Tags", []):
            if tag["Key"] == "Name":
                name = tag["Value"]
                break
        label = f"{rt_id} ({name})" if name else rt_id
        choices.append({"name": label, "value": rt})

    selected = questionary.checkbox(
        "Select route tables to delete (excluding main):",
        choices=choices
    ).ask()

    if not selected:
        show_info("No route tables selected.")
        return

    # Disassociate and delete
    for rt in selected:
        # Disassociate associated subnets
        for assoc in rt.get("Associations", []):
            assoc_id = assoc.get("RouteTableAssociationId")
            if assoc_id:
                try:
                    ec2.disassociate_route_table(AssociationId=assoc_id)
                    show_info(f"Disassociated: {assoc_id}")
                except Exception as e:
                    show_info(f"Failed to disassociate {assoc_id}: {str(e)}")

        try:
            ec2.delete_route_table(RouteTableId=rt["RouteTableId"])
            show_info(f"Deleted: {rt['RouteTableId']}")
        except Exception as e:
            show_info(f"Failed to delete {rt['RouteTableId']}: {str(e)}")

def delete_internet_gateways_in_vpc(ec2, vpc_id):
    show_info("Deleting Internet Gateways...")
    igws = list_resources(ec2, "describe_internet_gateways", "attachment.vpc-id", [vpc_id], "InternetGateways")

    if not igws:
        show_info("No internet gateways found.")
        return

    for igw in igws:
        igw_id = igw["InternetGatewayId"]
        try:
            ec2.detach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
        except ClientError as e:
            # Ignore error if not attached
            if "not attached" not in e.response["Error"]["Message"]:
                show_failure(f"Failed to detach IGW {igw_id}: {e.response['Error']['Message']}")
                continue

        try:
            ec2.delete_internet_gateway(InternetGatewayId=igw_id)
            show_success(f"Deleted Internet Gateway: {igw_id}")
        except ClientError as e:
            show_failure(f"Failed to delete IGW {igw_id}: {e.response['Error']['Message']}")


def delete_security_groups_in_vpc(ec2, vpc_id):
    show_info("Deleting Security Groups...")
    sgs = list_resources(ec2, "describe_security_groups", "vpc-id", [vpc_id], "SecurityGroups")

    def skip_default_sg(sg):
        return sg.get("GroupName") == "default"

    delete_resources(
        resources=sgs,
        id_key="GroupId",
        delete_func=ec2.delete_security_group,
        skip_condition=skip_default_sg
    )
