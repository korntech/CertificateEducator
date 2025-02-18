from rich.console import Console
from rich.text import Text
from datetime import datetime

console = Console()

class CertificateVisualizer:
    @staticmethod
    def draw_chain(chain):
        if not chain or not chain.certificates:
            console.print("\n[yellow]Warning: No certificates to display[/yellow]")
            return

        console.print("\n[bold cyan]Certificate Chain Visualization:[/bold cyan]")

        for i, cert in enumerate(chain.certificates):
            try:
                # Create certificate box
                console.print(f"\n{'└── ' if i > 0 else ''}{cert.subject}")
                console.print("┌" + "─" * 40 + "┐")
                console.print(f"│ Subject: {cert.subject:<30} │")
                console.print(f"│ Issuer: {cert.issuer:<31} │")
                console.print(f"│ Valid From: {cert.valid_from.strftime('%Y-%m-%d'):<27} │")
                console.print(f"│ Valid To: {cert.valid_to.strftime('%Y-%m-%d'):<29} │")
                console.print(f"│ Type: {'Root' if cert.is_root else 'Intermediate' if i < len(chain.certificates)-1 else 'Leaf':<33} │")
                console.print("└" + "─" * 40 + "┘")

                if i < len(chain.certificates) - 1:
                    console.print("         │")
                    console.print("         ▼")
            except Exception as e:
                console.print(f"[red]Error displaying certificate {i+1}: {str(e)}[/red]")

    @staticmethod
    def show_validation_result(result, message):
        if result:
            console.print("\n[bold green]✓ Chain Validation Successful[/bold green]")
            console.print(f"[green]{message}[/green]")
        else:
            console.print("\n[bold red]✗ Chain Validation Failed[/bold red]")
            console.print(f"[red]{message}[/red]")