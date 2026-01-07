import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from cospec.agents.base import BaseAgent
from cospec.core.analyzer import ProjectAnalyzer
from cospec.core.config import CospecConfig


class TestGeneratorAgent(BaseAgent):
    def __init__(self, config: CospecConfig, tool_name: Optional[str] = None) -> None:
        super().__init__(config, tool_name)
        self.analyzer = ProjectAnalyzer()

    def extract_test_scenarios_from_spec(self, spec_content: str) -> List[Dict[str, Any]]:
        """
        SPEC.md からテストシナリオを抽出する
        """
        scenarios = []

        # 1. 機能要件からテストシナリオを抽出
        fr_sections = re.findall(r"## FR-\d+: (.+?)(?=\n##|\n#|\Z)", spec_content, re.DOTALL)

        for fr_section in fr_sections:
            fr_title = fr_section.split("\n")[0].strip()
            fr_body = "\n".join(fr_section.split("\n")[1:]).strip()

            # 期待される挙動を抽出
            expected_behaviors = re.findall(r"### 期待される挙動\n(.*?)(?=\n###|\n##|\Z)", fr_body, re.DOTALL)

            if expected_behaviors:
                behaviors_text = expected_behaviors[0].strip()
                # 只取以 '-' 开头的行
                for line in behaviors_text.split("\n"):
                    line = line.strip()
                    if line.startswith("-"):
                        scenario = {
                            "type": "functional",
                            "feature": fr_title,
                            "description": line.lstrip("- ").strip(),
                            "priority": "high",
                        }
                        scenarios.append(scenario)

            # 条件分岐を抽出
            conditions = re.findall(r"### ユーザー入力\n(.*?)(?=\n###|\n##|\Z)", fr_body, re.DOTALL)

            if conditions:
                conditions_text = conditions[0].strip()
                # 只取以 '-' 开头的行
                for line in conditions_text.split("\n"):
                    line = line.strip()
                    if line.startswith("-"):
                        scenario = {
                            "type": "input_validation",
                            "feature": fr_title,
                            "description": line.lstrip("- ").strip(),
                            "priority": "medium",
                        }
                        scenarios.append(scenario)

        # 2. エラー処理シナリオを抽出（重複を避ける）
        seen_errors = set()
        # 只在 "期待される挙動" 部分中查找失敗時
        behavior_sections = re.findall(r"### 期待される挙動\n(.*?)(?=\n###|\n##|\Z)", spec_content, re.DOTALL)
        for section in behavior_sections:
            error_scenarios = re.findall(r"失敗時: (.+?)(?=\n|$)", section)
            for error in error_scenarios:
                error_text = error.strip()
                if error_text and error_text not in seen_errors:
                    scenarios.append(
                        {
                            "type": "error_handling",
                            "feature": "error_handling",
                            "description": error_text,
                            "priority": "high",
                        }
                    )
                    seen_errors.add(error_text)

        # 3. 出力形式シナリオを抽出（重複を避ける）
        seen_outputs = set()
        # 只在 "出力" 部分中查找
        output_sections = re.findall(r"### 出力\n(.*?)(?=\n###|\n##|\Z)", spec_content, re.DOTALL)
        for section in output_sections:
            output_scenarios = re.findall(r"出力: (.+?)(?=\n|$)", section)
            for output in output_scenarios:
                output_text = output.strip()
                if output_text and output_text not in seen_outputs:
                    scenarios.append(
                        {
                            "type": "output_format",
                            "feature": "output_format",
                            "description": output_text,
                            "priority": "medium",
                        }
                    )
                    seen_outputs.add(output_text)

        return scenarios

    def extract_test_scenarios_from_plan(self, plan_content: str) -> List[Dict[str, Any]]:
        """
        PLAN.md からテストシナリオを抽出する
        """
        scenarios = []

        # 実装予定のタスクからテストシナリオを抽出
        todo_items = re.findall(r"- \[ \] (.+)", plan_content)

        for todo in todo_items:
            scenarios.append(
                {"type": "integration", "feature": "implementation", "description": todo.strip(), "priority": "low"}
            )

        return scenarios

    def generate_pytest_test_code(
        self, scenarios: List[Dict[str, Any]], output_dir: Optional[Path] = None
    ) -> Dict[str, str]:
        """
        pytest 形式のテストコードを生成する
        """
        test_files: Dict[str, str] = {}

        # フィーチャーごとにテストファイルを分類
        scenarios_by_feature: Dict[str, List[Dict[str, Any]]] = {}
        for scenario in scenarios:
            feature = scenario["feature"]
            if feature not in scenarios_by_feature:
                scenarios_by_feature[feature] = []
            scenarios_by_feature[feature].append(scenario)

        for feature, feature_scenarios in scenarios_by_feature.items():
            test_code = self._generate_test_file_content(feature, feature_scenarios)
            filename = f"test_{feature.lower().replace(' ', '_').replace('-', '_')}.py"
            test_files[filename] = test_code

        # 出力先ディレクトリに保存
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, content in test_files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")

        return test_files

    def _generate_test_file_content(self, feature: str, scenarios: List[Dict[str, Any]]) -> str:
        """
        個々のテストファイルの内容を生成
        """
        # テストクラス名を生成（キャメルケースにする）
        # Remove underscores and spaces, then capitalize each word
        words = feature.replace("_", " ").split()
        class_name = "Test"
        for word in words:
            if word:
                class_name += word.capitalize()

        test_methods = []
        for _i, scenario in enumerate(scenarios):
            # テストメソッド名を生成
            method_name = self._generate_method_name(scenario["description"])
            priority = scenario["priority"]

            test_method = f'''    def test_{method_name}(self):
        """{scenario["description"]} (Priority: {priority})"""
        # TODO: 実装を記述
        pass

'''

            test_methods.append(test_method)

        test_content = f'''"""
Test cases for {feature}
Generated by cospec test-gen command
"""

import pytest


class {class_name}:
{"".join(test_methods)}
'''
        return test_content

    def _generate_method_name(self, description: str) -> str:
        """
        テストメソッド名を生成
        """
        # 特殊文字を除去し、スネークケースに変換
        name = re.sub(r"[^a-zA-Z0-9\s]", "", description)
        name = re.sub(r"\s+", "_", name.lower())
        name = name.strip("_")

        # pytest の命名規則に合わせる
        if not name.startswith("test_"):
            name = f"test_{name}"

        # 重複を避けるためのサフィックスを付ける
        return f"{name}_scenario"

    def generate_tests(self, output_dir: Optional[Path] = None) -> Dict[str, Any]:
        """
        テストケースを自動生成するメインメソッド
        """
        self.analyzer.collect_context()

        # SPEC.md からシナリオを抽出
        spec_path = Path("docs/SPEC.md")
        if not spec_path.exists():
            return {"status": "error", "message": "SPEC.md ファイルが見つかりません"}

        spec_content = spec_path.read_text(encoding="utf-8")
        spec_scenarios = self.extract_test_scenarios_from_spec(spec_content)

        # PLAN.md からシナリオを抽出
        plan_path = Path("docs/PLAN.md")
        plan_scenarios = []
        if plan_path.exists():
            plan_content = plan_path.read_text(encoding="utf-8")
            plan_scenarios = self.extract_test_scenarios_from_plan(plan_content)

        # シナリオを統合
        all_scenarios = spec_scenarios + plan_scenarios

        if not all_scenarios:
            return {
                "status": "success",
                "message": "テストシナリオが見つかりませんでした",
                "scenarios": [],
                "test_files": {},
            }

        # pytest テストコードを生成
        test_files = self.generate_pytest_test_code(all_scenarios, output_dir)

        return {
            "status": "success",
            "message": f"{len(all_scenarios)} 個のテストシナリオを抽出し、"
            f"{len(test_files)} 個のテストファイルを生成しました",
            "scenarios": all_scenarios,
            "test_files": test_files,
            "output_dir": str(output_dir) if output_dir else None,
        }
