import re
from pathlib import Path
from typing import Any, List, Optional

from cospec.agents.base import BaseAgent
from cospec.core.analyzer import ProjectAnalyzer


class HearerAgent(BaseAgent):
    def __init__(self, config: Any, tool_name: Optional[str] = None) -> None:
        super().__init__(config, tool_name)
        self.analyzer = ProjectAnalyzer()

    def extract_unclear_points(self, spec_content: str) -> List[str]:
        """
        SPEC.md から不明点を抽出するロジック（ヒント用）
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

    def create_mission_prompt(self) -> str:
        """
        AIエージェント向けの指令プロンプトを生成する
        """
        spec_path = Path("docs/SPEC.md")
        if not spec_path.exists():
            return "Error: docs/SPEC.md が見つかりません。まずは `cospec init` を実行してください。"

        spec_content = spec_path.read_text(encoding="utf-8")
        unclear_points = self.extract_unclear_points(spec_content)

        hint_text = ""
        if unclear_points:
            hint_text = "\n".join([f"- {p}" for p in unclear_points])
        else:
            hint_text = "- (正規表現による明示的な不明点は検出されませんでした。全文を精査してください)"

        # テンプレート読み込み
        # Note: パッケージ化された際のパス解決は別途考慮が必要だが、現状は相対パスで処理
        template_path = Path("src/cospec/prompts/hearer.md")
        if not template_path.exists():
            # フォールバック: パッケージルートからの相対パスで再試行
            template_path = Path(__file__).parent.parent / "prompts" / "hearer.md"

        if not template_path.exists():
            return "Error: Prompt template (src/cospec/prompts/hearer.md) not found."

        template = template_path.read_text(encoding="utf-8")
        return template.replace("{unclear_points_hint}", hint_text)
