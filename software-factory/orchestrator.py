"""
Multi-Agent Orchestrator

Coordinates the Requirements Engineer and Backend Software Engineer agents
to transform high-level user ideas into working backend code.
"""

from langchain_ollama import ChatOllama
from requirements_engineer import RequirementsEngineer
from backend_engineer import BackendEngineer
from implementator import Implementator
from typing import Dict, Any, Optional
import os
import re


class SoftwareFactoryOrchestrator:
    """
    Orchestrates the multi-agent software development process.
    
    Workflow:
    1. Requirements Engineer analyzes user idea
    2. Backend Software Engineer implements solution
    """
    
    def __init__(
        self,
        model_name: str = "llama3.1",
        temperature: float = 0.7,
        base_url: str = "http://localhost:11434"
    ):
        """
        Initialize the orchestrator with agents.
        
        Args:
            model_name: Ollama model to use
            temperature: Temperature for LLM
            base_url: Ollama base URL
        """
        llm = ChatOllama(
            model=model_name,
            temperature=temperature,
            base_url=base_url
        )
        
        self.requirements_engineer = RequirementsEngineer(llm)
        self.backend_engineer = BackendEngineer(llm)
        self.implementator = Implementator(llm)
    
    def _get_project_name(self, user_idea: str) -> str:
        """Generate a valid directory name from the user idea."""
        # Simple extraction: take first few words, or use a default if too complex
        # Ideally, we could ask the LLM, but let's keep it simple and deterministic for now.
        # Take first 3-5 words, lowercase, replace spaces with underscores
        short_desc = " ".join(user_idea.split()[:4]).lower()
        clean_name = re.sub(r'[^a-z0-9]', '_', short_desc)
        clean_name = re.sub(r'_+', '_', clean_name).strip('_')
        return clean_name or "generated_project"

    def build(self, user_idea: str, base_output_dir: str = "output") -> Dict[str, Any]:
        """
        Transform a user idea into working backend code.
        
        Args:
            user_idea: High-level description of the software idea
            base_output_dir: Base directory where project folder will be created
            
        Returns:
            Dictionary containing requirements, implementation, and code generation results
        """
        project_name = self._get_project_name(user_idea)
        project_dir = os.path.join(base_output_dir, project_name)
        
        print("=" * 80)
        print(f"🧠 SOFTWARE FACTORY - Project: {project_name}")
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
        
        print("\n⚙️  Phase 3: Code Generation")
        print("-" * 80)
        
        # Step 3: Implementator generates the files
        print(f"Generating code in {project_dir}/code/ ...")
        code_gen_result = self.implementator.generate_code(implementation, project_dir)
        
        print(f"\n✅ Code Generation Complete: {code_gen_result['code_dir']}")
        print("=" * 80)
        
        result = {
            "user_idea": user_idea,
            "project_name": project_name,
            "project_dir": project_dir,
            "requirements": requirements_spec,
            "implementation": implementation,
            "code_generation": code_gen_result,
            "requirements_raw": requirements_result,
            "implementation_raw": implementation_result,
            "code_generation_raw": code_gen_result
        }
        
        return result
    
    def save_output(self, result: Dict[str, Any], base_output_dir: str = "output") -> str:
        """
        Save the requirements and implementation to files in the project folder.
        
        Args:
            result: Result dictionary from build() method
            base_output_dir: Base directory (ignored if project_dir is in result)
            
        Returns:
            Path to the project directory
        """
        # Use project_dir from result if available, otherwise construct it
        if "project_dir" in result:
            project_dir = result["project_dir"]
        else:
            project_name = self._get_project_name(result["user_idea"])
            project_dir = os.path.join(base_output_dir, project_name)
            
        os.makedirs(project_dir, exist_ok=True)
        
        # Save requirements
        requirements_path = os.path.join(project_dir, "requirements.md")
        with open(requirements_path, "w", encoding="utf-8") as f:
            f.write(f"# Requirements Specification\n\n")
            f.write(f"## Original Idea\n\n{result['user_idea']}\n\n")
            f.write(result["requirements"])
        
        # Save implementation
        implementation_path = os.path.join(project_dir, "implementation.md")
        with open(implementation_path, "w", encoding="utf-8") as f:
            f.write(f"# Implementation\n\n")
            f.write(f"## Requirements\n\n{result['requirements']}\n\n")
            f.write(result["implementation"])
        
        print(f"\n💾 Output saved to {project_dir}/")
        print(f"   - requirements.md")
        print(f"   - implementation.md")
        print(f"   - code/ (generated by Implementator)")
        
        return project_dir

