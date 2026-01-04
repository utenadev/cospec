from pathlib import Path
from typing import List

class ProjectAnalyzer:
    def __init__(self, root_dir: Path = Path(".")):
        self.root_dir = root_dir

    def collect_context(self) -> str:
        """
        Collects content from key files (docs and source) to form the context for the LLM.
        """
        context_parts = []
        
        # 1. Read Documentation
        docs_dir = self.root_dir / "docs"
        if docs_dir.exists():
            for doc_file in docs_dir.glob("*.md"):
                # Skip large files or logs if necessary
                if doc_file.name == "WorkingLog.md":
                    continue
                context_parts.append(f"--- File: {doc_file} ---\n{doc_file.read_text(encoding='utf-8')}\n")

        # 2. List Source Files & Read Content (Limit size)
        # Reading src/cospec/**/*.py
        src_files = list(self.root_dir.glob("src/cospec/**/*.py"))
        
        context_parts.append("--- Source Code ---")
        for src_file in src_files:
            try:
                content = src_file.read_text(encoding="utf-8")
                context_parts.append(f"--- File: {src_file} ---\n{content}\n")
            except Exception as e:
                context_parts.append(f"--- File: {src_file} (Error reading: {e}) ---\n")

        return "\n".join(context_parts)
