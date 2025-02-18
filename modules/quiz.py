from dataclasses import dataclass
from typing import List, Dict
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import sys

console = Console()

@dataclass
class Question:
    text: str
    options: Dict[str, str]
    correct_answer: str
    explanation: str

class QuizManager:
    def __init__(self):
        self.questions = [
            Question(
                "What is the primary purpose of a Root CA certificate?",
                {
                    "a": "To encrypt website traffic",
                    "b": "To serve as the trust anchor for the PKI system",
                    "c": "To validate user passwords",
                    "d": "To speed up HTTPS connections"
                },
                "b",
                "A Root CA certificate serves as the trust anchor in a PKI system. It's self-signed and used to issue and validate other certificates."
            ),
            Question(
                "Why are Intermediate CA certificates commonly used?",
                {
                    "a": "To save money on certificate costs",
                    "b": "To make certificates work faster",
                    "c": "To protect the Root CA by keeping it offline",
                    "d": "To support more encryption algorithms"
                },
                "c",
                "Intermediate CAs protect the Root CA by allowing it to remain safely offline while the Intermediate CA handles day-to-day certificate issuance."
            ),
            Question(
                "What happens when a leaf certificate expires?",
                {
                    "a": "Nothing, it continues to work",
                    "b": "The private key changes automatically",
                    "c": "Browsers show security warnings",
                    "d": "The certificate repairs itself"
                },
                "c",
                "When a certificate expires, browsers show security warnings because the certificate is no longer valid according to its validity period."
            ),
            Question(
                "What is the risk of using trustServerCertificate=true?",
                {
                    "a": "It makes connections slower",
                    "b": "It allows man-in-the-middle attacks",
                    "c": "It uses more memory",
                    "d": "It requires more CPU power"
                },
                "b",
                "Using trustServerCertificate=true bypasses certificate chain validation, making it possible for attackers to intercept traffic through man-in-the-middle attacks."
            ),
            Question(
                "What is certificate chain validation?",
                {
                    "a": "Checking certificate file size",
                    "b": "Verifying the website's IP address",
                    "c": "Validating the path from leaf to root certificate",
                    "d": "Measuring certificate download speed"
                },
                "c",
                "Certificate chain validation involves checking the trust path from a leaf certificate back to a trusted root certificate, ensuring each certificate was issued by its parent."
            ),
            Question(
                "Which component signs an Intermediate CA certificate?",
                {
                    "a": "The leaf certificate",
                    "b": "Another Intermediate CA",
                    "c": "The Root CA",
                    "d": "The web server"
                },
                "c",
                "Intermediate CA certificates are signed by the Root CA, establishing the chain of trust from the root to the leaf certificates."
            ),
            Question(
                "What is a common cause of certificate chain errors?",
                {
                    "a": "Using HTTPS instead of HTTP",
                    "b": "Missing intermediate certificates",
                    "c": "Network being too fast",
                    "d": "Having too many certificates"
                },
                "b",
                "Missing intermediate certificates break the chain of trust because browsers can't verify the path from the leaf certificate to a trusted root CA."
            ),
            Question(
                "How can you prevent man-in-the-middle attacks?",
                {
                    "a": "Use faster internet connections",
                    "b": "Always validate the full certificate chain",
                    "c": "Disable HTTPS entirely",
                    "d": "Use shorter passwords"
                },
                "b",
                "Proper certificate chain validation is crucial for preventing man-in-the-middle attacks by ensuring the authenticity of certificates."
            )
        ]
        self.score = 0
        self.total_questions = len(self.questions)

    def run_quiz(self, non_interactive=False):
        try:
            console.print(Panel("Welcome to the PKI Knowledge Quiz!", border_style="cyan"))
            console.print("\nTest your understanding of Public Key Infrastructure (PKI) concepts.")
            console.print("Each question has one correct answer.\n")

            for i, question in enumerate(self.questions, 1):
                console.print(f"\n[bold cyan]Question {i} of {self.total_questions}:[/bold cyan]")
                console.print(question.text)

                for option, text in question.options.items():
                    console.print(f"{option}) {text}")

                if non_interactive:
                    # In non-interactive mode, always choose the first option
                    answer = list(question.options.keys())[0]
                    console.print(f"\nAuto-selected answer: {answer}")
                else:
                    try:
                        answer = Prompt.ask("\nYour answer", choices=list(question.options.keys()))
                    except EOFError:
                        console.print("\n[yellow]Quiz terminated due to EOF[/yellow]")
                        return

                if answer.lower() == question.correct_answer.lower():
                    self.score += 1
                    console.print("\n[bold green]✓ Correct![/bold green]")
                else:
                    console.print("\n[bold red]✗ Incorrect[/bold red]")

                console.print(f"[bold]Explanation:[/bold] {question.explanation}\n")

                if not non_interactive and i < self.total_questions:
                    try:
                        Prompt.ask("Press Enter for next question")
                    except EOFError:
                        console.print("\n[yellow]Quiz terminated due to EOF[/yellow]")
                        return

            self.show_results()

        except KeyboardInterrupt:
            console.print("\n[yellow]Quiz terminated by user[/yellow]")
        except Exception as e:
            console.print(f"\n[red]An error occurred: {str(e)}[/red]")

    def show_results(self):
        percentage = (self.score / self.total_questions) * 100
        console.print("\n[bold]Quiz Complete![/bold]")
        console.print(f"Your score: {self.score}/{self.total_questions} ({percentage:.1f}%)")

        if percentage >= 80:
            console.print("[bold green]Excellent! You have a strong understanding of PKI concepts![/bold green]")
        elif percentage >= 60:
            console.print("[bold yellow]Good job! Consider reviewing some concepts to improve your knowledge.[/bold yellow]")
        else:
            console.print("[bold red]You might want to review the PKI concepts and try again.[/bold red]")