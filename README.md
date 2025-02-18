### Broken Chain Example
```
Root CA
┌────────────────────────────────────────┐
│ Subject: Root CA                        │
│ Issuer: Root CA                         │
│ Type: Root                              │
└────────────────────────────────────────┘
         ▲
         │
Intermediate CA
┌────────────────────────────────────────┐
│ Subject: Intermediate CA                │
│ Issuer: Root CA                         │
│ Type: Intermediate                      │
└────────────────────────────────────────┘
         ╳  (Chain broken - wrong issuer)
         │
wrong.example.com
┌────────────────────────────────────────┐
│ Subject: wrong.example.com              │
│ Issuer: Wrong Issuer                    │
│ Type: Leaf                              │
└────────────────────────────────────────┘
```

## Installation 🚀

1. Clone the repository
2. Install dependencies:
```bash
pip install rich
```

## Usage 💻

### Interactive Mode
Run the tool with full interactive interface:
```bash
python cert_game.py
```
Then select option 6 to start the quiz mode.

### Non-interactive Mode
Run specific scenarios or quiz directly:
```bash
# Run basic valid chain scenario
python cert_game.py --scenario 1

# Run expired certificate scenario
python cert_game.py --scenario 2

# Run broken chain scenario
python cert_game.py --scenario 3

# Run trust server certificate demo
python cert_game.py --scenario 4

# Run man-in-the-middle attack demo
python cert_game.py --scenario 5

# Start the PKI knowledge quiz
python cert_game.py --quiz
```

## Available Scenarios 📚

1. **Basic Valid Certificate Chain**
   - Demonstrates a proper certificate chain
   - Shows Root CA → Intermediate CA → Leaf certificate relationship
   - Explains chain validation process

2. **Expired Certificate Scenario**
   - Shows how expired certificates affect chain validation
   - Demonstrates date-based validation checks
   - Common real-world scenario in production environments

3. **Broken Certificate Chain**
   - Illustrates a chain with mismatched issuers
   - Shows how trust is broken when certificates don't properly chain
   - Common misconfiguration scenario

4. **Trust Server Certificate Flag Demo**
   - Demonstrates the implications of trustServerCertificate flag
   - Shows security risks of bypassing chain validation
   - Important for development vs. production considerations
   - ⚠️ WARNING: Using trustServerCertificate=true in production is dangerous!

## Educational Value 📖

This tool helps users understand:
- Certificate chain validation process
- Root and intermediate certificate roles
- Common certificate-related issues
- Security implications of different configurations
- Best practices for certificate management

### Interactive Quiz Mode 📝
Test your PKI knowledge with our built-in quiz feature:
- Multiple-choice questions covering key PKI concepts
- Immediate feedback and explanations
- Score tracking and performance assessment
- Interactive learning experience

## Technical Details 🛠️

- Built with Python 3.x
- Uses Rich library for terminal UI
- Modular design for easy scenario additions
- Support for both interactive and automated usage

## Project Structure 📁
```
├── modules/
│   ├── certificate.py    # Core certificate logic
│   ├── scenarios.py      # Different certificate scenarios
│   ├── visualizer.py     # Chain visualization
│   └── quiz.py          # PKI knowledge quiz module
└── cert_game.py          # Main application