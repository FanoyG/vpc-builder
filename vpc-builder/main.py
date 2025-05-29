from cli.display import show_title
from cli.prompts import main_menu
from cli.access import run_access_flow
from cli.create import run_create_flow
from cli.modify import run_modify_flow
from cli.delete import run_delete_flow
from cli.aws_client import AWSClient

def main():
    show_title("🚀 VPC Builder CLI")
    ec2 = AWSClient.get_ec2_client()  # get EC2 client once

    while True:
        choice = main_menu()
        if choice == "Access":
            run_access_flow()
        elif choice == "Create":
            run_create_flow()
        elif choice == "Modify":
            run_modify_flow()
        elif choice == "Delete":
            run_delete_flow(ec2)
        elif choice == "Exit":
            print("Goodbye 👋")
            break

if __name__ == "__main__":
    main()
