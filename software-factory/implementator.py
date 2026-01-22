"""
Implementator Agent

This agent is responsible for:
- Taking the design and code snippets from the Backend Engineer
- Writing the actual code files to disk
- Ensuring the code is structurally correct
"""

from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import tool
from typing import Dict, Any
import os

class Implementator:
    """Implementator Agent that generates the actual code files."""
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.current_working_dir = None
        self.agent = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        """Create the Implementator agent."""
        
        system_prompt = """You are a Code Implementator.

Your responsibilities:
- Read the implementation plan and code provided by the Backend Engineer
- Create the actual files on the disk using the `write_file` tool
- Ensure all necessary files are created (including __init__.py if needed, requirements.txt, etc.)
- Do NOT hallucinate new requirements, strictly follow the provided implementation

When writing files:
- Use the `write_file` tool for EVERY file mentioned in the implementation.
- You must provide 'filename' and 'content' as separate arguments.
- If the implementation has multiple files, call `write_file` multiple times.
"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Define tool using decorator for structured input
        @tool
        def write_file(filename: str, content: str) -> str:
            """
            Write code to a file.
            Args:
                filename: Name of the file (e.g., 'main.py')
                content: The code content to write to the file
            """
            try:
                # Ensure we have a working directory
                if not self.current_working_dir:
                    return "Error: Output directory not set"
                    
                # Create full path
                file_path = os.path.join(self.current_working_dir, filename)
                
                # Create parent directories if they don't exist
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Write file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                    
                return f"Successfully wrote {filename}"
                
            except Exception as e:
                return f"Error writing file: {str(e)}"

        tools = [write_file]
        
        agent = create_tool_calling_agent(self.llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)

    def generate_code(self, implementation_plan: str, output_dir: str) -> Dict[str, Any]:
        """
        Generate code files based on the implementation plan.
        
        Args:
            implementation_plan: The full text describing the implementation
            output_dir: The directory where code should be generated
            
        Returns:
            Dictionary containing the results
        """
        # Set the working directory for file operations
        self.current_working_dir = os.path.join(output_dir, "code")
        os.makedirs(self.current_working_dir, exist_ok=True)
        
        input_text = f"""Please implement the solution based on this plan. Create all necessary files in the current directory.

Implementation Plan:
{implementation_plan}
"""
        
        result = self.agent.invoke({"input": input_text})
        return {
            "output": result["output"],
            "code_dir": self.current_working_dir
        }
