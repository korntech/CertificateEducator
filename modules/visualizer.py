from rich.console import Console
from rich.text import Text
from datetime import datetime

console = Console()

class CertificateVisualizer:
    @staticmethod
    def draw_chain(chain, show_mitm=False):
        if not chain or not chain.certificates:
            console.print("\n[yellow]Warning: No certificates to display[/yellow]")
            return

        console.print("\n[bold cyan]Certificate Chain Visualization:[/bold cyan]")

        # Display certificates in correct order (leaf at bottom)
        certs = list(reversed(chain.certificates))

        if show_mitm:
            console.print("\n[bold red]⚠️  SECURITY RISK: Man-in-the-Middle Attack Scenario[/bold red]")
            console.print("[red]When trustServerCertificate=true, traffic can be intercepted:[/red]")

            # Draw the client
            console.print("\nClient")
            console.print("┌" + "─" * 40 + "┐")
            console.print("│ Secure Connection Expected              │")
            console.print("└" + "─" * 40 + "┘")
            console.print("         │")
            console.print("         ▼")

            # Draw the attacker
            console.print("[bold red]Malicious Interceptor[/bold red]")
            console.print("┌" + "─" * 40 + "┐")
            console.print("│ ⚠️  Traffic Being Intercepted           │")
            console.print("└" + "─" * 40 + "┘")
            console.print("         │")
            console.print("         ▼")

        # Draw the certificate chain
        for i, cert in enumerate(certs):
            try:
                # Create certificate box
                console.print(f"\n{'└── ' if i > 0 else ''}{cert.subject}")
                console.print("┌" + "─" * 40 + "┐")
                console.print(f"│ Subject: {cert.subject:<30} │")
                console.print(f"│ Issuer: {cert.issuer:<31} │")
                console.print(f"│ Valid From: {cert.valid_from.strftime('%Y-%m-%d'):<27} │")
                console.print(f"│ Valid To: {cert.valid_to.strftime('%Y-%m-%d'):<29} │")
                cert_type = 'Root' if cert.is_root else ('Intermediate' if i > 0 and i < len(certs)-1 else 'Leaf')
                console.print(f"│ Type: {cert_type:<33} │")
                console.print("└" + "─" * 40 + "┘")

                # Only draw arrow if not the last certificate
                if i < len(certs) - 1:
                    console.print("         │")
                    console.print("         ▲")
            except Exception as e:
                console.print(f"[red]Error displaying certificate {i+1}: {str(e)}[/red]")

        if show_mitm:
            console.print("\n[bold red]Security Impact:[/bold red]")
            console.print("• Attacker can read all traffic")
            console.print("• Sensitive data can be stolen")
            console.print("• Actions can be modified")
            console.print("\n[bold yellow]Prevention:[/bold yellow]")
            console.print("• Never use trustServerCertificate=true in production")
            console.print("• Always validate the full certificate chain")
            console.print("• Keep root CA certificates up to date")

    @staticmethod
    def show_validation_result(result, message):
        if result:
            console.print("\n[bold green]✓ Chain Validation Successful[/bold green]")
            console.print(f"[green]{message}[/green]")
        else:
            console.print("\n[bold red]✗ Chain Validation Failed[/bold red]")
            console.print(f"[red]{message}[/red]")