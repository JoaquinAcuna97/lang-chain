# Software Factory - Multi-Agent System

A LangChain-based multi-agent system that transforms high-level user ideas into working backend code. The system consists of two collaborating agents:

1. **Requirements Engineer** - Analyzes ideas and produces requirements specifications
2. **Backend Software Engineer** - Designs architecture and generates executable code
3. **Implementator** - Generates the actual code files on disk

## Features

- 🤖 Multi-agent collaboration using LangChain
- 📋 Automated requirements analysis
- 💻 Code generation with architecture design
- 🎯 Terminal-based execution focus
- 📝 Production-ready code output

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ollama and pull a model (e.g., llama3.1):
```bash
ollama serve
ollama pull llama3.1
```

## Usage

### Command Line

```bash
python main.py "Create a command-line tool that counts words in a file"
```

### Interactive Mode

```bash
python main.py
```

Then enter your idea when prompted.

### Advanced Options

```bash
python main.py "Your idea" --model llama3.1 --temperature 0.7 --output-dir my_output
```

## Project Structure

```
software-factory/
├── main.py                    # Entry point
├── orchestrator.py            # Multi-agent coordination
├── requirements_engineer.py   # Requirements Engineer agent
├── backend_engineer.py        # Backend Software Engineer agent
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## How It Works

1. **Requirements Phase**: The Requirements Engineer agent analyzes the user's idea and produces a structured requirements specification with:
   - Functional requirements
   - Non-functional requirements
   - Assumptions
   - Constraints

2. **Implementation Phase**: The Backend Software Engineer agent receives the requirements and generates:
   - System architecture
   - Project structure
   - Complete executable code
   - Setup and usage instructions

3. **Code Generation Phase**: The Implementator agent reads the implementation plan and creates:
   - Complete source code files
   - Configuration files

4. **Output**: Results are saved to `output/{project_name}/`:
   - `requirements.md` - Requirements specification
   - `implementation.md` - Complete implementation
   - `code/` - Directory containing the generated source code

## Example

```bash
python main.py "Build a simple CLI calculator"
```

The system will:
1. Analyze the idea and create requirements
2. Design the architecture
3. Generate working Python code
4. Save everything to `output/build_a_simple_cli_calculator/` directory

## Requirements

- Python 3.8+
- Ollama installed and running (with a model pulled)
- LangChain and dependencies (see `requirements.txt`)

## Notes

- The system focuses on terminal-based, backend software only
- Code is generated in Python by default
- All output is production-ready with error handling and logging
- The agents prefer assumptions over excessive questioning

