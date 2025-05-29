import boto3
import questionary

# Common AWS regions list (you can expand it)
AWS_REGIONS = [
    "us-east-1 (N. Virginia)",
    "us-east-2 (Ohio)",
    "us-west-1 (N. California)",
    "us-west-2 (Oregon)",
    "eu-west-1 (Ireland)",
    "eu-central-1 (Frankfurt)",
    "ap-south-1 (Mumbai)",
    "ap-northeast-1 (Tokyo)",
    "ap-southeast-1 (Singapore)",
    "ap-southeast-2 (Sydney)",
    "sa-east-1 (São Paulo)",
    "Custom Region"
]

def select_region():
    choice = questionary.select(
        "Select AWS region:",
        choices=AWS_REGIONS,
        default="us-east-1 (N. Virginia)"
    ).ask()

    if choice == "Custom Region":
        region = questionary.text("Enter custom AWS region code (e.g., eu-west-3):").ask()
        region = region.strip()
        if not region:
            print("Empty input, defaulting to us-east-1")
            return "us-east-1"
        return region
    else:
        # Extract the region code before the first space (e.g. "us-east-1")
        return choice.split()[0]

class AWSClient:
    _session = None
    _ec2 = None

    @classmethod
    def get_session(cls):
        if cls._session is None:
            region = select_region()
            cls._session = boto3.Session(region_name=region)
        return cls._session

    @classmethod
    def get_ec2_client(cls):
        if cls._ec2 is None:
            cls._ec2 = cls.get_session().client("ec2")
        return cls._ec2
