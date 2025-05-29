# File: cli/prompts.py

import questionary
from rich.console import Console
from rich.panel import Panel

console = Console()

def main_menu():
    return questionary.select(
        "What do you want to do?",
        choices=[
            "Create",
            "Access",
            "Modify",
            "Delete",
            "Exit"
        ]
    ).ask()

def show_success(message: str):
    panel = Panel.fit(f"[bold green]{message}[/bold green]", title="✅ SUCCESS", border_style="green")
    console.print(panel)

def show_failure(message: str):
    panel = Panel.fit(f"[bold red]{message}[/bold red]", title="❌ FAILURE", border_style="red")
    console.print(panel)

def confirm_action(message: str) -> bool:
    return questionary.confirm(message).ask()
