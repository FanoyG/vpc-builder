# File: cli/display.py

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

def show_title(title: str):
    banner = Panel.fit(
        f"[bold cyan]{title}[/bold cyan]",
        title="📦 CLI TOOL",
        border_style="bright_magenta",
        box=box.DOUBLE_EDGE
    )
    console.print(banner)

def show_success(message: str):
    panel = Panel(
        Text(f"✅ {message}", style="bold green"),
        title="SUCCESS",
        border_style="green",
        box=box.ROUNDED
    )
    console.print(panel)

def show_failure(message: str):
    panel = Panel(
        Text(f"❌ {message}", style="bold red"),
        title="ERROR",
        border_style="red",
        box=box.ROUNDED
    )
    console.print(panel)

def show_warning(message: str):
    panel = Panel(
        Text(f"⚠️ {message}", style="bold yellow"),
        title="WARNING",
        border_style="yellow",
        box=box.ROUNDED
    )
    console.print(panel)

def show_info(message: str):
    panel = Panel(
        Text(f"ℹ️ {message}", style="bold blue"),
        title="INFO",
        border_style="blue",
        box=box.ROUNDED
    )
    console.print(panel)
