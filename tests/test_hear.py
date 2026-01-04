import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from cospec.agents.hearer import HearerAgent
from cospec.core.config import CospecConfig


class TestHearerAgent:
    def setup_method(self):
        """各テストメソッドの実行前に設定を行う"""
        self.config = CospecConfig()
        self.config.default_tool = "qwen"
        self.config.language = "ja"

    @patch('cospec.agents.hearer.ProjectAnalyzer')
    def test_extract_unclear_points_when_conditions(self, mock_analyzer):
        """条件分岐の不明点を正しく抽出できる"""
        agent = HearerAgent(self.config)

        spec_content = """
        ## FR-001: テスト機能

        ### 概要
        ユーザーが指定した条件でテストを行う

        ### ユーザー入力
        - 時点: 条件が不明な場合
        - 時点: 未定の条件
        - 時点: 正しい条件
        """

        unclear_points = agent.extract_unclear_points(spec_content)

        assert len(unclear_points) == 2
        assert "条件 '条件が不明な場合' の詳細が不明です" in unclear_points
        assert "条件 '未定の条件' の詳細が不明です" in unclear_points

    @patch('cospec.agents.hearer.ProjectAnalyzer')
    def test_extract_unclear_points_user_inputs(self, mock_analyzer):
        """ユーザー入力の不明点を正しく抽出できる"""
        agent = HearerAgent(self.config)

        spec_content = """
        ## FR-001: テスト機能

        ### ユーザー入力
        - 引数: --input (任意)
        - 引数: --output (オプション)
        - 引数: --required (必須)
        """

        unclear_points = agent.extract_unclear_points(spec_content)

        assert len(unclear_points) == 2
        assert "引数 '--input (任意)' の必須/任意の判断基準が不明です" in unclear_points
        assert "引数 '--output (オプション)' の必須/任意の判断基準が不明です" in unclear_points

    @patch('cospec.agents.hearer.ProjectAnalyzer')
    def test_extract_unclear_points_error_handling(self, mock_analyzer):
        """エラー処理の不明点を正しく抽出できる"""
        agent = HearerAgent(self.config)

        spec_content = """
        ## FR-001: テスト機能

        ### 期待される挙動
        - 成功時: 正常に処理
        - 失敗時: 未定義のエラー処理
        - エラー: 不明な例外処理
        """

        unclear_points = agent.extract_unclear_points(spec_content)

        assert len(unclear_points) == 2
        assert "エラー処理 '未定義のエラー処理' の詳細が不明です" in unclear_points
        assert "エラー処理 '不明な例外処理' の詳細が不明です" in unclear_points

    @patch('cospec.agents.hearer.ProjectAnalyzer')
    def test_generate_interactive_questions(self, mock_analyzer):
        """インタラクティブな質問を正しく生成できる"""
        agent = HearerAgent(self.config)

        unclear_points = [
            "条件 '不明な条件' の詳細が不明です",
            "引数 '--input' の必須/任意の判断基準が不明です"
        ]

        questions = agent.generate_interactive_questions(unclear_points)

        assert "1. 条件 '不明な条件' の詳細が不明です について、具体的な要件を教えてください。" in questions
        assert "2. 引数 '--input' の必須/任意の判断基準が不明です について、具体的な要件を教えてください。" in questions

    @patch('cospec.agents.hearer.Path')
    def test_hear_requirements_spec_not_found(self, mock_path):
        """SPEC.md が存在しない場合のエラーハンドリング"""
        # SPEC.md が存在しない設定
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = False

        agent = HearerAgent(self.config)

        result = agent.hear_requirements()

        assert result["status"] == "error"
        assert "SPEC.md ファイルが見つかりません" in result["message"]

    @patch('cospec.agents.hearer.Path')
    @patch('cospec.agents.hearer.ProjectAnalyzer')
    def test_hear_requirements_no_unclear_points(self, mock_analyzer, mock_path):
        """不明点がない場合の正常終了"""
        # SPEC.md が存在し、内容がある設定
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.read_text.return_value = """
        ## FR-001: テスト機能

        ### 概要
        明確なテスト機能

        ### ユーザー入力
        - 引数: --required (必須)

        ### 期待される挙動
        - 成功時: 正常に処理
        """

        agent = HearerAgent(self.config)

        result = agent.hear_requirements()

        assert result["status"] == "success"
        assert "不明点が見つかりませんでした" in result["message"]
        assert result["questions"] == []

    @patch('cospec.agents.hearer.Path')
    @patch('cospec.agents.hearer.ProjectAnalyzer')
    def test_hear_requirements_with_unclear_points(self, mock_analyzer, mock_path):
        """不明点がある場合の正常処理"""
        # SPEC.md が存在し、不明点がある設定
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.read_text.return_value = """
        ## FR-001: テスト機能

        ### 概要
        不明なテスト機能

        ### ユーザー入力
        - 引数: --input (任意)
        - 時点: 条件が不明
        """

        # HearerAgent の run_tool メソッドをモック
        agent = HearerAgent(self.config)
        agent.run_tool = Mock(return_value="AIの回答")

        result = agent.hear_requirements()

        assert result["status"] == "success"
        assert "ヒアリングが完了しました" in result["message"]
        assert len(result["questions"]) > 0
        assert "ai_response" in result
        assert result["ai_response"] == "AIの回答"

    @patch('cospec.agents.hearer.Path')
    @patch('cospec.agents.hearer.ProjectAnalyzer')
    def test_hear_requirements_tool_error(self, mock_analyzer, mock_path):
        """外部ツール実行時のエラー処理"""
        # SPEC.md が存在し、不明点がある設定
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.read_text.return_value = """
        ## FR-001: テスト機能

        ### 概要
        不明なテスト機能

        ### ユーザー入力
        - 引数: --input (任意)
        """

        # HearerAgent の run_tool メソッドをエラーにする
        agent = HearerAgent(self.config)
        agent.run_tool = Mock(side_effect=Exception("ツール実行エラー"))

        result = agent.hear_requirements()

        assert result["status"] == "error"
        assert "ツール実行エラー" in result["message"]
        assert len(result["questions"]) > 0
        assert "unclear_points" in result