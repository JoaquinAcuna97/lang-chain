"""
Requirements Engineer Agent

This agent is responsible for:
- Clarifying the problem and scope
- Identifying functional and non-functional requirements
- Producing a final, explicit requirements specification
"""

from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import Tool
from typing import Dict, Any


class RequirementsEngineer:
    """Requirements Engineer Agent that analyzes user ideas and produces specifications."""
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.agent = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        """Create the Requirements Engineer agent."""
        
        system_prompt = """You are a Requirements Engineer in a software development company.

Your responsibilities:
- Clarify the problem and scope
- Ask concise, essential questions only if absolutely required
- Identify functional and non-functional requirements
- Produce a final, explicit requirements specification
- Decide when requirements are "good enough" to proceed

Rules:
- Prefer assumptions over excessive questioning
- Clearly list assumptions if information is missing
- Output must be deterministic and unambiguous

When you receive a user idea, analyze it and produce a requirements specification in the following format:

## Final Requirements
### Functional
- [List functional requirements]
### Non-Functional
- [List non-functional requirements like performance, security, etc.]
### Assumptions
- [List any assumptions made]
### Constraints
- [List constraints and limitations]

Be thorough but concise. Only ask questions if critical information is missing."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create a simple tool for the agent to use if needed
        tools = [
            Tool(
                name="analyze_requirements",
                func=lambda x: "Requirements analysis complete",
                description="Use this to finalize requirements analysis"
            )
        ]
        
        agent = create_tool_calling_agent(self.llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    def analyze(self, user_idea: str) -> Dict[str, Any]:
        """
        Analyze user idea and produce requirements specification.
        
        Args:
            user_idea: High-level description of the software idea
            
        Returns:
            Dictionary containing the requirements specification
        """
        result = self.agent.invoke({"input": user_idea})
        return {
            "requirements": result["output"],
            "raw_response": result
        }

