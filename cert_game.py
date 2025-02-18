from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from modules.certificate import Certificate, CertificateChain
from modules.visualizer import CertificateVisualizer
from modules.scenarios import Scenarios
import sys
import argparse

console = Console()

def show_welcome():
    welcome_text = """
    Welcome to the Certificate Authority (CA) Learning Tool!

    This interactive tool will help you understand:
    - How certificate chains work
    - The role of root and intermediate certificates
    - Certificate validation processes
    - Common certificate-related scenarios
    - The impact of trust flags

    Use this tool to explore different certificate scenarios and learn about PKI.
    """
    console.print(Panel(welcome_text, title="CA Certificate Learning Tool", border_style="cyan"))

def show_menu():
    console.print("\n[bold cyan]Available Scenarios:[/bold cyan]")
    console.print("1. Basic Valid Certificate Chain")
    console.print("2. Expired Certificate Scenario")
    console.print("3. Broken Certificate Chain")
    console.print("4. Trust Server Certificate Flag Demo")
    console.print("5. Exit")

    return Prompt.ask("\nSelect a scenario", choices=["1", "2", "3", "4", "5"])

def explain_scenario(scenario_num):
    explanations = {
        "1": """
        [bold]Basic Valid Certificate Chain[/bold]

        This scenario shows a typical valid certificate chain:
        - Root CA (self-signed certificate)
        - Intermediate CA (signed by Root CA)
        - Leaf certificate (signed by Intermediate CA)

        This is the most common and secure setup used in production environments.
        The chain is validated from leaf to root, ensuring trust at each step.
        """,
        "2": """
        [bold]Expired Certificate Scenario[/bold]

        This scenario demonstrates an expired certificate:
        - The leaf certificate has passed its validity period
        - Even with valid Root and Intermediate certificates, the chain is invalid
        - In production, this would trigger security warnings
        - Certificate expiration is checked before chain validation
        """,
        "3": """
        [bold]Broken Certificate Chain[/bold]

        This scenario shows a broken certificate chain:
        - The leaf certificate's issuer doesn't match the intermediate CA
        - This breaks the chain of trust
        - Common in misconfigured servers or incomplete certificate installations
        - Chain validation fails regardless of valid dates
        """,
        "4": """
        [bold]Trust Server Certificate Flag Demo[/bold]

        This scenario demonstrates the trustServerCertificate flag:
        - A standalone certificate without proper chain
        - Normally this would fail chain validation
        - With trustServerCertificate=true, only dates are checked
        - [red]WARNING:[/red] Using this flag bypasses important security checks
        - Common in development but [red]dangerous in production[/red]
        """
    }

    console.print(Panel(explanations[scenario_num], border_style="blue"))

def run_scenario(scenario_num, non_interactive=False):
    try:
        if not non_interactive:
            explain_scenario(scenario_num)

        chain = None
        trust_server_certificate = False

        if scenario_num == "1":
            chain = Scenarios.get_basic_chain()
        elif scenario_num == "2":
            chain = Scenarios.get_expired_cert_chain()
        elif scenario_num == "3":
            chain = Scenarios.get_broken_chain()
        elif scenario_num == "4":
            chain = Scenarios.get_untrusted_chain()
            trust_server_certificate = True

        if chain is None:
            console.print("[red]Error: Failed to create certificate chain[/red]")
            return

        visualizer = CertificateVisualizer()
        visualizer.draw_chain(chain)

        if not non_interactive:
            console.print("\n[bold]Press Enter to validate the certificate chain...[/bold]")
            input()

        if scenario_num == "4":
            console.print("\n[yellow]Running validation with trustServerCertificate=true[/yellow]")

        result, message = chain.validate(trust_server_certificate)
        visualizer.show_validation_result(result, message)

        if scenario_num == "4" and not non_interactive:
            console.print("\n[yellow]Running validation with trustServerCertificate=false[/yellow]")
            result, message = chain.validate(False)
            visualizer.show_validation_result(result, message)

    except Exception as e:
        console.print(f"\n[red]An error occurred: {str(e)}[/red]")
    finally:
        if not non_interactive:
            console.print("\n[bold]Press Enter to continue...[/bold]")
            input()

def main():
    parser = argparse.ArgumentParser(description='CA Certificate Learning Tool')
    parser.add_argument('--scenario', type=str, choices=['1', '2', '3', '4'],
                       help='Run a specific scenario non-interactively')
    args = parser.parse_args()

    try:
        # Non-interactive mode - skip welcome and menu
        if args.scenario:
            run_scenario(args.scenario, non_interactive=True)
            return

        # Interactive mode
        show_welcome()
        while True:
            choice = show_menu()
            if choice == "5":
                console.print("\n[bold green]Thank you for using the CA Certificate Learning Tool![/bold green]")
                break
            run_scenario(choice)

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Program terminated by user.[/bold yellow]")
    except Exception as e:
        console.print(f"\n[red]Fatal error: {str(e)}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()