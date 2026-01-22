"""
Main entry point for the Software Factory multi-agent system.

Usage:
    python main.py "Your software idea here"
    
Or run interactively:
    python main.py
"""

import sys
import argparse
from orchestrator import SoftwareFactoryOrchestrator


def main():
    """Main function to run the software factory."""
    parser = argparse.ArgumentParser(
        description="Multi-Agent Software Factory - Transform ideas into code"
    )
    parser.add_argument(
        "idea",
        nargs="?",
        help="High-level description of the software idea"
    )
    parser.add_argument(
        "--model",
        default="llama3.1",
        help="Ollama model to use (default: llama3.1)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature for LLM (default: 0.7)"
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:11434",
        help="Ollama base URL (default: http://localhost:11434)"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to save output files (default: output)"
    )
    
    args = parser.parse_args()
    
    # Get user idea
    if args.idea:
        user_idea = args.idea
    else:
        print("🧠 Software Factory - Multi-Agent Development System")
        print("=" * 80)
        print("\nEnter your software idea (or press Ctrl+C to exit):")
        print("-" * 80)
        user_idea = input("> ").strip()
        
        if not user_idea:
            print("No idea provided. Exiting.")
            sys.exit(1)
    
    try:
        # Initialize orchestrator
        orchestrator = SoftwareFactoryOrchestrator(
            model_name=args.model,
            temperature=args.temperature,
            base_url=args.base_url
        )
        
        # Build the solution
        result = orchestrator.build(user_idea)
        
        # Save output
        orchestrator.save_output(result, args.output_dir)
        
        print("\n✅ Software Factory process complete!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

