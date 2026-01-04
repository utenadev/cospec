from cospec.agents.base import BaseAgent
from cospec.core.analyzer import ProjectAnalyzer


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
            "\n"
            "IMPORTANT:\n"
            "1. Check 'docs/PLAN.md' and 'docs/WorkingLog.md' first.\n"
            "2. If a missing feature is listed in PLAN.md or\n"
            "   WorkingLog.md, do NOT report it as a 'Missing Feature'\n"
            "   failure. Instead, acknowledge it as 'Planned' or\n"
            "   'In Progress'.\n"
            "3. Focus your criticism on unimplemented features that\n"
            "   are NOT planned, or inconsistencies in what IS\n"
            "   implemented.\n"
            "\n"
            "Output a Markdown report.\n\n"
            "--- Context ---"
        )

        full_prompt = system_prompt + context
        return self.run_tool(full_prompt)
