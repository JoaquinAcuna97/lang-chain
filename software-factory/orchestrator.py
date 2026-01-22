"""
Multi-Agent Orchestrator

Coordinates the Requirements Engineer and Backend Software Engineer agents
to transform high-level user ideas into working backend code.
"""

from langchain_openai import ChatOpenAI
from requirements_engineer import RequirementsEngineer
from backend_engineer import BackendEngineer
from typing import Dict, Any, Optional
import os


class SoftwareFactoryOrchestrator:
    """
    Orchestrates the multi-agent software development process.
    
    Workflow:
    1. Requirements Engineer analyzes user idea
    2. Backend Software Engineer implements solution
    """
    
    def __init__(
        self,
        model_name: str = "gpt-4",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        """
        Initialize the orchestrator with agents.
        
        Args:
            model_name: OpenAI model to use
            temperature: Temperature for LLM
            api_key: OpenAI API key (if not set, uses OPENAI_API_KEY env var)
        """
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        self.requirements_engineer = RequirementsEngineer(llm)
        self.backend_engineer = BackendEngineer(llm)
    
    def build(self, user_idea: str) -> Dict[str, Any]:
        """
        Transform a user idea into working backend code.
        
        Args:
            user_idea: High-level description of the software idea
            
        Returns:
            Dictionary containing requirements and implementation
        """
        print("=" * 80)
        print("🧠 SOFTWARE FACTORY - Multi-Agent Development")
        print("=" * 80)
        print("\n📋 Phase 1: Requirements Engineering")
        print("-" * 80)
        
        # Step 1: Requirements Engineer analyzes the idea
        requirements_result = self.requirements_engineer.analyze(user_idea)
        requirements_spec = requirements_result["requirements"]
        
        print("\n✅ Requirements Specification Complete")
        print("=" * 80)
        print(requirements_spec)
        print("=" * 80)
        
        print("\n💻 Phase 2: Backend Implementation")
        print("-" * 80)
        
        # Step 2: Backend Engineer implements the solution
        implementation_result = self.backend_engineer.implement(requirements_spec)
        implementation = implementation_result["implementation"]
        
        print("\n✅ Implementation Complete")
        print("=" * 80)
        print(implementation)
        print("=" * 80)
        
        return {
            "user_idea": user_idea,
            "requirements": requirements_spec,
            "implementation": implementation,
            "requirements_raw": requirements_result,
            "implementation_raw": implementation_result
        }
    
    def save_output(self, result: Dict[str, Any], output_dir: str = "output") -> str:
        """
        Save the requirements and implementation to files.
        
        Args:
            result: Result dictionary from build() method
            output_dir: Directory to save output files
            
        Returns:
            Path to the output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Save requirements
        requirements_path = os.path.join(output_dir, "requirements.md")
        with open(requirements_path, "w", encoding="utf-8") as f:
            f.write(f"# Requirements Specification\n\n")
            f.write(f"## Original Idea\n\n{result['user_idea']}\n\n")
            f.write(result["requirements"])
        
        # Save implementation
        implementation_path = os.path.join(output_dir, "implementation.md")
        with open(implementation_path, "w", encoding="utf-8") as f:
            f.write(f"# Implementation\n\n")
            f.write(f"## Requirements\n\n{result['requirements']}\n\n")
            f.write(result["implementation"])
        
        print(f"\n💾 Output saved to {output_dir}/")
        print(f"   - requirements.md")
        print(f"   - implementation.md")
        
        return output_dir

