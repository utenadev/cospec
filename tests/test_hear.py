from unittest.mock import Mock, patch

from cospec.agents.hearer import HearerAgent
from cospec.core.config import CospecConfig


class TestHearerAgent:
    def setup_method(self):
        """各テストメソッドの実行前に設定を行う"""
        self.config = CospecConfig()
        self.config.default_tool = "qwen"
        self.config.language = "ja"

    def test_extract_unclear_points_when_conditions(self):
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

    def test_extract_unclear_points_user_inputs(self):
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

    def test_extract_unclear_points_error_handling(self):
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

    @patch("cospec.agents.hearer.Path")
    def test_create_mission_prompt_spec_not_found(self, mock_path):
        """SPEC.md が存在しない場合のエラーハンドリング"""
        # SPEC.md が存在しない設定
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        # 最初の呼び出し(SPEC.md)でFalseを返す
        mock_path_instance.exists.side_effect = [False]

        agent = HearerAgent(self.config)
        prompt = agent.create_mission_prompt()

        assert "Error: docs/SPEC.md が見つかりません" in prompt

    @patch("cospec.agents.hearer.Path")
    def test_create_mission_prompt_no_unclear_points(self, mock_path):
        """不明点がない場合のプロンプト生成"""
        mock_spec_path = Mock()
        mock_spec_path.exists.return_value = True
        mock_spec_path.read_text.return_value = """
        ## FR-001: テスト機能
        明確なテスト機能
        """

        mock_template_path = Mock()
        mock_template_path.exists.return_value = True
        mock_template_path.read_text.return_value = "Prompt Template: {unclear_points_hint}"

        # Path(...) の呼び出し順序に応じてモックを返す
        def side_effect(path):
            if str(path) == "docs/SPEC.md":
                return mock_spec_path
            return mock_template_path

        mock_path.side_effect = side_effect

        agent = HearerAgent(self.config)
        prompt = agent.create_mission_prompt()

        assert "Prompt Template:" in prompt
        assert "(正規表現による明示的な不明点は検出されませんでした" in prompt

    @patch("cospec.agents.hearer.Path")
    def test_create_mission_prompt_with_unclear_points(self, mock_path):
        """不明点がある場合のプロンプト生成"""
        mock_spec_path = Mock()
        mock_spec_path.exists.return_value = True
        mock_spec_path.read_text.return_value = """
        - 時点: 条件が不明
        """

        mock_template_path = Mock()
        mock_template_path.exists.return_value = True
        mock_template_path.read_text.return_value = "Prompt Template: {unclear_points_hint}"

        def side_effect(path):
            if str(path) == "docs/SPEC.md":
                return mock_spec_path
            return mock_template_path

        mock_path.side_effect = side_effect

        agent = HearerAgent(self.config)
        prompt = agent.create_mission_prompt()

        assert "Prompt Template:" in prompt
        assert "- 条件 '条件が不明' の詳細が不明です" in prompt
