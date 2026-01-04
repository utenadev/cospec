from cospec.agents.base import BaseAgent
from cospec.core.analyzer import ProjectAnalyzer
from cospec.core.config import CospecConfig

class ReviewerAgent(BaseAgent):
    def review_project(self) -> str:
        """
        Analyzes the project and returns a review report.
        """
        analyzer = ProjectAnalyzer()
        context = analyzer.collect_context()
        
        system_prompt = (
            "You are a strict code reviewer. Compare the documentation and code provided below.\n"
            "Identify inconsistencies, missing features, and guideline violations.\n"
            "Output a Markdown report.\n\n"
            "--- Context ---"
        )
        
        full_prompt = system_prompt + context
        return self.run_tool(full_prompt)
