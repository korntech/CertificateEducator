from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from modules.certificate import Certificate, CertificateChain
from modules.visualizer import CertificateVisualizer
from modules.scenarios import Scenarios
from modules.quiz import QuizManager
import sys
import argparse

console = Console()

def show_welcome():
    ascii_art = """[bold green]
     🔒 CERTIFICATE AUTHORITY LEARNING TOOL 🔒

    [cyan]ROOT CA[/cyan]    [yellow]SECURE[/yellow]    [cyan]LEAF[/cyan]
           [yellow]>>VERIFY>>[/yellow]
             [yellow]TRUST[/yellow]

    < Learn • Verify • Secure >
    """
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
    console.print(ascii_art)
    console.print(Panel(welcome_text, title="About", border_style="cyan"))

def show_menu():
    console.print("\n[bold cyan]Available Options:[/bold cyan]")
    console.print("1. Basic Valid Certificate Chain")
    console.print("2. Expired Certificate Scenario")
    console.print("3. Broken Certificate Chain")
    console.print("4. Trust Server Certificate Flag Demo")
    console.print("5. Man-in-the-Middle Attack Scenario")
    console.print("6. Take PKI Knowledge Quiz")
    console.print("7. Exit")

    return Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5", "6", "7"])

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
        """,
        "5": """
        [bold]Man-in-the-Middle Attack Scenario[/bold]

        This scenario demonstrates the dangers of using trustServerCertificate:
        - Shows how an attacker can intercept traffic
        - Demonstrates why chain validation is crucial
        - Visualizes the security risks of bypassing validation
        - [red]WARNING:[/red] Real-world implications of insecure settings
        - Explains how proper certificate validation prevents attacks
        """
    }

    console.print(Panel(explanations[scenario_num], border_style="blue"))

def run_scenario(scenario_num, non_interactive=False):
    try:
        if not non_interactive:
            explain_scenario(scenario_num)

        chain = None
        trust_server_certificate = False
        show_mitm = False

        if scenario_num == "1":
            chain = Scenarios.get_basic_chain()
        elif scenario_num == "2":
            chain = Scenarios.get_expired_cert_chain()
        elif scenario_num == "3":
            chain = Scenarios.get_broken_chain()
        elif scenario_num == "4":
            chain = Scenarios.get_untrusted_chain()
            trust_server_certificate = True
        elif scenario_num == "5":
            chain = Scenarios.get_mitm_attack_chain()
            trust_server_certificate = True
            show_mitm = True

        if chain is None:
            console.print("[red]Error: Failed to create certificate chain[/red]")
            return

        visualizer = CertificateVisualizer()
        visualizer.draw_chain(chain, show_mitm)

        if not non_interactive:
            console.print("\n[bold]Press Enter to validate the certificate chain...[/bold]")
            input()

        if scenario_num in ["4", "5"]:
            console.print("\n[yellow]Running validation with trustServerCertificate=true[/yellow]")

        result, message = chain.validate(trust_server_certificate)
        visualizer.show_validation_result(result, message)

        if scenario_num in ["4", "5"] and not non_interactive:
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
    parser.add_argument('--scenario', type=str, choices=['1', '2', '3', '4', '5'],
                       help='Run a specific scenario non-interactively')
    parser.add_argument('--quiz', action='store_true',
                       help='Start the PKI knowledge quiz directly')
    args = parser.parse_args()

    try:
        # Non-interactive mode
        if args.scenario:
            run_scenario(args.scenario, non_interactive=True)
            return
        elif args.quiz:
            quiz = QuizManager()
            quiz.run_quiz(non_interactive=True)
            return

        # Interactive mode
        show_welcome()
        while True:
            choice = show_menu()
            if choice == "7":
                console.print("\n[bold green]Thank you for using the CA Certificate Learning Tool![/bold green]")
                break
            elif choice == "6":
                quiz = QuizManager()
                quiz.run_quiz(non_interactive=False)
            else:
                run_scenario(choice)

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Program terminated by user.[/bold yellow]")
    except Exception as e:
        console.print(f"\n[red]Fatal error: {str(e)}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()