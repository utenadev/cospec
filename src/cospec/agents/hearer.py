import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from cospec.agents.base import BaseAgent
from cospec.core.analyzer import ProjectAnalyzer


class HearerAgent(BaseAgent):
    def __init__(self, config: Any, tool_name: Optional[str] = None) -> None:
        super().__init__(config, tool_name)
        self.analyzer = ProjectAnalyzer()

    def extract_unclear_points(self, spec_content: str) -> List[str]:
        """
        SPEC.md から不明点を抽出するロジック
        """
        unclear_points = []

        # 1. 条件分岐の不明点を抽出
        if_conditions = re.findall(r"- 時点: (.+)", spec_content)
        for condition in if_conditions:
            if "?" in condition or "不明" in condition or "未定" in condition:
                unclear_points.append(f"条件 '{condition}' の詳細が不明です")

        # 2. ユーザー入力の不明点を抽出
        user_inputs = re.findall(r"- 引数: (.+?)(?:\n|$)", spec_content)
        for input_desc in user_inputs:
            if "任意" in input_desc or "オプション" in input_desc:
                unclear_points.append(f"引数 '{input_desc.strip()}' の必須/任意の判断基準が不明です")

        # 3. エラー処理の不明点を抽出
        error_patterns = [r"失敗時: (.+)", r"エラー: (.+)", r"例外: (.+)"]
        for pattern in error_patterns:
            errors = re.findall(pattern, spec_content)
            for error in errors:
                if "未定義" in error or "不明" in error:
                    unclear_points.append(f"エラー処理 '{error}' の詳細が不明です")

        # 4. 出力形式の不明点を抽出
        output_patterns = [r"出力: (.+)", r"結果: (.+)"]
        for pattern in output_patterns:
            outputs = re.findall(pattern, spec_content)
            for output in outputs:
                if "?" in output or "不明" in output:
                    unclear_points.append(f"出力形式 '{output}' の詳細が不明です")

        return unclear_points

    def generate_interactive_questions(self, unclear_points: List[str]) -> str:
        """
        不明点からインタラクティブな質問を生成
        """
        questions = []
        for i, point in enumerate(unclear_points, 1):
            questions.append(f"{i}. {point} について、具体的な要件を教えてください。")

        return "\n".join(questions)

    def hear_requirements(self) -> Dict[str, Any]:
        """
        要件の曖昧さをAIが人間にヒアリングし、SPEC.mdを洗練させる
        """
        # SPEC.md から不明点を抽出
        spec_path = Path("docs/SPEC.md")
        if not spec_path.exists():
            return {"status": "error", "message": "SPEC.md ファイルが見つかりません"}

        spec_content = spec_path.read_text(encoding="utf-8")
        unclear_points = self.extract_unclear_points(spec_content)

        if not unclear_points:
            return {"status": "success", "message": "SPEC.md に不明点が見つかりませんでした", "questions": []}

        # 質問を生成
        questions = self.generate_interactive_questions(unclear_points)

        # AI に質問内容を提示し、回答を生成させる
        prompt = f"""以下の不明点について、ユーザーにインタラクティブに質問してください。

不明点:
{chr(10).join(unclear_points)}

質問例:
{questions}

ユーザーの回答を基に、SPEC.md の改善案を提案してください。
"""

        try:
            response = self.run_tool(prompt)
            return {
                "status": "success",
                "message": "ヒアリングが完了しました",
                "questions": questions,
                "ai_response": response,
                "unclear_points": unclear_points,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"ヒアリング中にエラーが発生しました: {str(e)}",
                "questions": questions,
                "unclear_points": unclear_points,
            }
