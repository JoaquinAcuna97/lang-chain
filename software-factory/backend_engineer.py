"""
Backend Software Engineer Agent

This agent is responsible for:
- Designing the system architecture
- Choosing appropriate technologies
- Generating executable code
- Providing setup and run instructions
"""

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from typing import Dict, Any
import os


class BackendEngineer:
    """Backend Software Engineer Agent that designs and implements solutions."""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.agent = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        """Create the Backend Software Engineer agent."""
        
        system_prompt = """You are a Backend Software Engineer in a software development company.

Your responsibilities:
- Design the system architecture
- Choose appropriate technologies
- Generate executable code
- Provide setup and run instructions
- Ensure the solution works from the terminal

Rules:
- Code must be minimal but production-quality
- Prefer Python unless stated otherwise
- Include error handling and basic logging
- Avoid unnecessary abstractions
- Focus on terminal-based execution (no UI, no frontend)

When you receive requirements, produce a complete solution in the following format:

## Architecture
- [System architecture description]
- [Technology choices and rationale]

## Project Structure
- [File structure and organization]

## Code
```python
# full working code here
```

## Setup Instructions
- [How to install dependencies]
- [How to run the code]

## Usage
- [How to use the software from terminal]

Generate complete, working code that can be executed immediately."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        tools = [
            Tool(
                name="generate_code",
                func=lambda x: "Code generation complete",
                description="Use this to finalize code generation"
            )
        ]
        
        agent = create_openai_tools_agent(self.llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    def implement(self, requirements: str) -> Dict[str, Any]:
        """
        Implement the solution based on requirements.
        
        Args:
            requirements: Requirements specification from Requirements Engineer
            
        Returns:
            Dictionary containing the implementation details
        """
        input_text = f"""Based on the following requirements, design and implement a complete solution:

{requirements}

Remember:
- Generate complete, executable Python code
- Include error handling and logging
- Provide clear setup and usage instructions
- Focus on terminal-based execution"""
        
        result = self.agent.invoke({"input": input_text})
        return {
            "implementation": result["output"],
            "raw_response": result
        }

