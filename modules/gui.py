import tkinter as tk
from tkinter import ttk, scrolledtext
from rich.console import Console
import io
from .certificate import Certificate, CertificateChain
from .scenarios import Scenarios
from .quiz import QuizManager
from .visualizer import CertificateVisualizer

class CertificateAuthorityGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Certificate Authority Learning Tool")
        self.root.geometry("800x600")
        
        # Configure the style
        style = ttk.Style()
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))
        style.configure("Title.TLabel", font=("Helvetica", 12, "bold"))
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)
        
        header_label = ttk.Label(
            header_frame,
            text="🔒 Certificate Authority Learning Tool 🔒",
            style="Header.TLabel"
        )
        header_label.pack()
        
        # Main content area
        content_frame = ttk.Frame(self.root, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for buttons
        button_frame = ttk.Frame(content_frame, padding="5")
        button_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(button_frame, text="Scenarios", style="Title.TLabel").pack(pady=5)
        
        # Scenario buttons
        scenarios = [
            ("Basic Valid Chain", lambda: self.run_scenario("1")),
            ("Expired Certificate", lambda: self.run_scenario("2")),
            ("Broken Chain", lambda: self.run_scenario("3")),
            ("Trust Server Flag", lambda: self.run_scenario("4")),
            ("MITM Attack", lambda: self.run_scenario("5")),
            ("Take Quiz", self.start_quiz)
        ]
        
        for text, command in scenarios:
            ttk.Button(button_frame, text=text, command=command).pack(pady=2, fill=tk.X)
        
        # Right panel for display
        self.display_frame = ttk.Frame(content_frame, padding="5")
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Text area for output
        self.output_text = scrolledtext.ScrolledText(
            self.display_frame,
            wrap=tk.WORD,
            width=60,
            height=30,
            font=("Courier", 10)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Welcome message
        self.show_welcome()
    
    def show_welcome(self):
        welcome_text = """
        Welcome to the Certificate Authority (CA) Learning Tool!

        This interactive tool will help you understand:
        • How certificate chains work
        • The role of root and intermediate certificates
        • Certificate validation processes
        • Common certificate-related scenarios
        • The impact of trust flags

        Select a scenario from the left panel to begin learning about PKI.
        """
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, welcome_text)
    
    def run_scenario(self, scenario_num):
        # Capture rich console output
        console = Console(file=io.StringIO(), force_terminal=True)
        
        # Clear previous output
        self.output_text.delete(1.0, tk.END)
        
        # Get the scenario
        scenario_map = {
            "1": Scenarios.get_basic_chain,
            "2": Scenarios.get_expired_cert_chain,
            "3": Scenarios.get_broken_chain,
            "4": Scenarios.get_untrusted_chain,
            "5": Scenarios.get_mitm_attack_chain
        }
        
        chain = scenario_map[scenario_num]()
        visualizer = CertificateVisualizer()
        
        # Capture the visualization output
        output_buffer = io.StringIO()
        console = Console(file=output_buffer, force_terminal=True)
        
        with console.capture() as capture:
            visualizer.draw_chain(chain, show_mitm=(scenario_num == "5"))
            result, message = chain.validate(trust_server_certificate=(scenario_num in ["4", "5"]))
            visualizer.show_validation_result(result, message)
        
        # Display the output
        self.output_text.insert(tk.END, output_buffer.getvalue())
    
    def start_quiz(self):
        quiz = QuizManager()
        QuizDialog(self.root, quiz)

class QuizDialog(tk.Toplevel):
    def __init__(self, parent, quiz_manager):
        super().__init__(parent)
        self.title("PKI Knowledge Quiz")
        self.geometry("600x400")
        
        self.quiz = quiz_manager
        self.current_question = 0
        self.selected_answer = tk.StringVar()
        
        self.setup_ui()
        self.show_question()
    
    def setup_ui(self):
        # Question area
        self.question_label = ttk.Label(
            self,
            wraplength=550,
            justify="left",
            padding="10"
        )
        self.question_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Options frame
        self.options_frame = ttk.Frame(self, padding="10")
        self.options_frame.pack(fill=tk.X, padx=10)
        
        # Navigation buttons
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.next_button = ttk.Button(
            button_frame,
            text="Next",
            command=self.next_question
        )
        self.next_button.pack(side=tk.RIGHT, padx=5)
    
    def show_question(self):
        question = self.quiz.questions[self.current_question]
        
        # Update question text
        self.question_label.config(
            text=f"Question {self.current_question + 1} of {len(self.quiz.questions)}:\n\n{question.text}"
        )
        
        # Clear old options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Create new option buttons
        for option, text in question.options.items():
            ttk.Radiobutton(
                self.options_frame,
                text=f"{option}) {text}",
                value=option,
                variable=self.selected_answer
            ).pack(anchor=tk.W, pady=2)
    
    def next_question(self):
        if self.selected_answer.get():
            question = self.quiz.questions[self.current_question]
            correct = self.selected_answer.get() == question.correct_answer
            
            if correct:
                self.quiz.score += 1
            
            # Show explanation
            explanation = ttk.Label(
                self.options_frame,
                text=f"\n{'✓ Correct!' if correct else '✗ Incorrect'}\n{question.explanation}",
                wraplength=500,
                padding="10"
            )
            explanation.pack(pady=10)
            
            self.next_button.config(text="Next Question" if self.current_question < len(self.quiz.questions) - 1 else "Finish")
            
            if self.current_question < len(self.quiz.questions) - 1:
                self.current_question += 1
                self.selected_answer.set("")
                self.after(2000, self.show_question)
            else:
                self.after(2000, self.show_results)
    
    def show_results(self):
        # Clear the window
        for widget in self.winfo_children():
            widget.destroy()
        
        # Calculate and show results
        percentage = (self.quiz.score / len(self.quiz.questions)) * 100
        
        result_text = f"""
        Quiz Complete!
        
        Your score: {self.quiz.score}/{len(self.quiz.questions)} ({percentage:.1f}%)
        
        {self.get_feedback(percentage)}
        """
        
        ttk.Label(
            self,
            text=result_text,
            wraplength=500,
            justify="center",
            padding="20"
        ).pack(expand=True)
        
        ttk.Button(
            self,
            text="Close",
            command=self.destroy
        ).pack(pady=10)
    
    def get_feedback(self, percentage):
        if percentage >= 80:
            return "Excellent! You have a strong understanding of PKI concepts!"
        elif percentage >= 60:
            return "Good job! Consider reviewing some concepts to improve your knowledge."
        else:
            return "You might want to review the PKI concepts and try again."
