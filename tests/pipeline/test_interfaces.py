"""
Tests for pipeline interfaces
"""
import unittest
from src.ai_platform.pipeline.types import PipelineContext, PipelineStage
from src.ai_platform.pipeline.interfaces import PipelineStep, PipelineStepError

class MockPipelineStep(PipelineStep):
    """
    Mock implementation of PipelineStep for testing
    """
    def process(self, context: PipelineContext) -> PipelineContext:
        try:
            if context.original_query == "fail":
                raise PipelineStepError("Forced failure", self.stage)
            return self._update_context(context, "test result")
        except Exception as e:
            return self._handle_error(context, e)

class TestPipelineStep(unittest.TestCase):
    """
    Test cases for PipelineStep interface
    """
    def setUp(self):
        """
        Set up test fixtures
        """
        self.step = MockPipelineStep(PipelineStage.GENERATION)
        self.context = PipelineContext(
            query_id="test-123",
            original_query="Test query"
        )

    def test_initialization(self):
        """
        Test step initialization
        """
        self.assertEqual(self.step.stage, PipelineStage.GENERATION)

    def test_successful_processing(self):
        """
        Test successful step processing
        """
        result = self.step.process(self.context)
        
        self.assertEqual(result.current_stage, PipelineStage.GENERATION)
        self.assertEqual(
            result.get_stage_result(PipelineStage.GENERATION),
            "test result"
        )
        self.assertFalse(result.has_error)

    def test_error_handling(self):
        """
        Test error handling during processing
        """
        self.context.original_query = "fail"
        result = self.step.process(self.context)
        
        self.assertTrue(result.has_error)
        self.assertEqual(result.current_stage, PipelineStage.ERROR)
        self.assertEqual(result.error_stage, PipelineStage.GENERATION)
        self.assertIn("Forced failure", result.error)

    def test_update_context_with_modified_query(self):
        """
        Test context updates including query modification
        """
        result = self.step._update_context(
            self.context,
            "test result",
            modified_query="Modified query"
        )
        
        self.assertEqual(result.modified_query, "Modified query")
        self.assertEqual(
            result.get_stage_result(self.step.stage),
            "test result"
        )

    def test_pipeline_step_error(self):
        """
        Test PipelineStepError formatting
        """
        error = PipelineStepError("Test error", PipelineStage.GENERATION)
        self.assertIn("generation", str(error))
        self.assertIn("Test error", str(error))

if __name__ == '__main__':
    unittest.main()