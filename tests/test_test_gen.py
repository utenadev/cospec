import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from cospec.agents.test_generator import TestGeneratorAgent
from cospec.core.config import CospecConfig


class TestTestGeneratorAgent:
    def setup_method(self):
        """各テストメソッドの実行前に設定を行う"""
        self.config = CospecConfig()
        self.config.default_tool = "qwen"
        self.config.language = "ja"

    @patch('cospec.agents.test_generator.ProjectAnalyzer')
    def test_extract_test_scenarios_from_spec(self, mock_analyzer):
        """SPEC.md からテストシナリオを正しく抽出できる"""
        agent = TestGeneratorAgent(self.config)

        spec_content = """
        ## FR-001: テスト機能

        ### 概要
        ユーザーが指定した条件でテストを行う

        ### ユーザー入力
        - 引数: --input (任意)
        - 引数: --output (必須)

        ### 期待される挙動
        - 成功時: 正常に処理
        - 失敗時: エラーを表示
        - 失敗時: 終了コード1を返す

        ### 出力
        - 出力: JSON形式で結果を出力
        """

        scenarios = agent.extract_test_scenarios_from_spec(spec_content)

        # Check that we have the expected scenarios
        assert len(scenarios) >= 5
        assert any(s['type'] == 'input_validation' and '--input (任意)' in s['description'] for s in scenarios)
        assert any(s['type'] == 'input_validation' and '--output (必須)' in s['description'] for s in scenarios)
        assert any(s['type'] == 'functional' and '正常に処理' in s['description'] for s in scenarios)
        assert any(s['type'] == 'error_handling' and 'エラーを表示' in s['description'] for s in scenarios)
        assert any(s['type'] == 'output_format' and 'JSON形式' in s['description'] for s in scenarios)

    @patch('cospec.agents.test_generator.ProjectAnalyzer')
    def test_extract_test_scenarios_from_plan(self, mock_analyzer):
        """PLAN.md からテストシナリオを正しく抽出できる"""
        agent = TestGeneratorAgent(self.config)

        plan_content = """
        ## 実装計画

        - [ ] HearerAgent の作成
        - [ ] TestGeneratorAgent の作成
        - [ ] CLI コマンドの統合
        """

        scenarios = agent.extract_test_scenarios_from_plan(plan_content)

        assert len(scenarios) == 3
        assert scenarios[0]['type'] == 'integration'
        assert 'HearerAgent の作成' in scenarios[0]['description']

    @patch('cospec.agents.test_generator.ProjectAnalyzer')
    def test_generate_pytest_test_code(self, mock_analyzer):
        """pytest 形式のテストコードを正しく生成できる"""
        agent = TestGeneratorAgent(self.config)

        scenarios = [
            {
                'type': 'functional',
                'feature': 'test_function',
                'description': '正常に処理',
                'priority': 'high'
            },
            {
                'type': 'error_handling',
                'feature': 'test_function',
                'description': 'エラーを表示',
                'priority': 'medium'
            }
        ]

        test_files = agent.generate_pytest_test_code(scenarios)

        assert len(test_files) == 1
        filename = list(test_files.keys())[0]
        content = test_files[filename]

        assert 'TestTestFunction' in content
        assert 'import pytest' in content
        assert 'def test_' in content
        assert 'Priority: high' in content
        assert 'Priority: medium' in content

    @patch('cospec.agents.test_generator.Path')
    def test_generate_tests_spec_not_found(self, mock_path):
        """SPEC.md が存在しない場合のエラーハンドリング"""
        # SPEC.md が存在しない設定
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = False

        agent = TestGeneratorAgent(self.config)

        result = agent.generate_tests()

        assert result["status"] == "error"
        assert "SPEC.md ファイルが見つかりません" in result["message"]

    @patch('cospec.agents.test_generator.Path')
    @patch('cospec.agents.test_generator.ProjectAnalyzer')
    def test_generate_tests_no_scenarios(self, mock_analyzer, mock_path):
        """テストシナリオがない場合の正常終了"""
        # SPEC.md が存在し、内容がある設定
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.read_text.return_value = """
        ## FR-001: テスト機能

        ### 概要
        明確なテスト機能
        """

        agent = TestGeneratorAgent(self.config)

        result = agent.generate_tests()

        assert result["status"] == "success"
        assert "テストシナリオが見つかりませんでした" in result["message"]
        assert result["scenarios"] == []
        assert result["test_files"] == {}

    @patch('cospec.agents.test_generator.Path')
    @patch('cospec.agents.test_generator.ProjectAnalyzer')
    def test_generate_tests_with_scenarios(self, mock_analyzer, mock_path):
        """テストシナリオがある場合の正常処理"""
        # SPEC.md が存在し、テストシナリオがある設定
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.read_text.return_value = """
        ## FR-001: テスト機能

        ### 概要
        テスト機能

        ### ユーザー入力
        - 引数: --input (必須)

        ### 期待される挙動
        - 成功時: 正常に処理
        """

        agent = TestGeneratorAgent(self.config)

        result = agent.generate_tests()

        assert result["status"] == "success"
        assert "テストシナリオを抽出し" in result["message"]
        assert len(result["scenarios"]) > 0
        assert len(result["test_files"]) > 0

    @patch('cospec.agents.test_generator.Path')
    @patch('cospec.agents.test_generator.ProjectAnalyzer')
    def test_generate_tests_with_output_dir(self, mock_analyzer, mock_path):
        """出力先ディレクトリを指定した場合のテスト"""
        # 一時ディレクトリを作成
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)

            # SPEC.md が存在し、テストシナリオがある設定
            mock_path_instance = Mock()
            mock_path.return_value = mock_path_instance
            mock_path_instance.exists.return_value = True
            mock_path_instance.read_text.return_value = """
            ## FR-001: テスト機能

            ### ユーザー入力
            - 引数: --input (必須)
            """

            agent = TestGeneratorAgent(self.config)

            result = agent.generate_tests(output_dir=output_dir)

            assert result["status"] == "success"
            assert "test_files" in result

            # 出力先にファイルが作成されていることを確認
            output_files = list(output_dir.glob("*.py"))
            assert len(output_files) > 0

    def test_generate_method_name(self):
        """テストメソッド名を正しく生成できる"""
        agent = TestGeneratorAgent(self.config)

        test_cases = [
            ("正常に処理", "test_正常に処理_scenario"),
            ("--input (必須)", "test_input_必須_scenario"),
            ("エラーを表示", "test_エラーを表示_scenario"),
            ("JSON形式で出力", "test_json形式で出力_scenario")
        ]

        for description, expected in test_cases:
            result = agent._generate_method_name(description)
            assert result.startswith("test_")
            assert "scenario" in result

    def test_generate_test_file_content(self):
        """テストファイルの内容を正しく生成できる"""
        agent = TestGeneratorAgent(self.config)

        scenarios = [
            {
                'description': '正常に処理',
                'priority': 'high'
            },
            {
                'description': 'エラーを表示',
                'priority': 'medium'
            }
        ]

        content = agent._generate_test_file_content("test_function", scenarios)

        assert "TestTestFunction" in content
        assert "import pytest" in content
        assert "def test_" in content
        assert "Priority: high" in content
        assert "Priority: medium" in content
        assert "TODO: 実装を記述" in content