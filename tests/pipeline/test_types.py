"""
Tests for pipeline type definitions
"""
import unittest
from src.ai_platform.pipeline.types import PipelineContext, PipelineStage

class TestPipelineStage(unittest.TestCase):
    """
    Test cases for PipelineStage enumeration
    """
    def test_stage_values(self):
        """
        Test that all pipeline stages have correct string values
        """
        self.assertEqual(PipelineStage.INIT.value, "initialization")
        self.assertEqual(PipelineStage.INPUT_VALIDATION.value, "input_validation")
        self.assertEqual(PipelineStage.CONTEXT_ENHANCEMENT.value, "context_enhancement")
        self.assertEqual(PipelineStage.MODEL_ROUTING.value, "model_routing")
        self.assertEqual(PipelineStage.GENERATION.value, "generation")
        self.assertEqual(PipelineStage.OUTPUT_VALIDATION.value, "output_validation")
        self.assertEqual(PipelineStage.COMPLETE.value, "complete")
        self.assertEqual(PipelineStage.ERROR.value, "error")

class TestPipelineContext(unittest.TestCase):
    """
    Test cases for PipelineContext class
    """
    def setUp(self):
        """
        Create a sample context for use in tests
        """
        self.context = PipelineContext(
            query_id="test-123",
            original_query="Test query"
        )

    def test_initialization(self):
        """
        Test context initialization with default values
        """
        self.assertEqual(self.context.query_id, "test-123")
        self.assertEqual(self.context.original_query, "Test query")
        self.assertEqual(self.context.current_stage, PipelineStage.INIT)
        self.assertIsNone(self.context.modified_query)
        self.assertEqual(self.context.stage_results, {})
        self.assertIsNone(self.context.final_response)
        self.assertIsNone(self.context.error)
        self.assertIsNone(self.context.error_stage)

    def test_has_error_property(self):
        """
        Test error state detection
        """
        self.assertFalse(self.context.has_error)
        self.context.error = "Test error"
        self.assertTrue(self.context.has_error)

    def test_is_complete_property(self):
        """
        Test completion state detection
        """
        self.assertFalse(self.context.is_complete)
        
        self.context.current_stage = PipelineStage.COMPLETE
        self.assertTrue(self.context.is_complete)
        
        self.context.current_stage = PipelineStage.ERROR
        self.assertTrue(self.context.is_complete)

    def test_get_stage_result(self):
        """
        Test retrieving stage results
        """
        # Test nonexistent stage
        self.assertIsNone(self.context.get_stage_result(PipelineStage.GENERATION))

        # Test existing stage
        self.context.stage_results[PipelineStage.GENERATION] = "test result"
        self.assertEqual(
            self.context.get_stage_result(PipelineStage.GENERATION),
            "test result"
        )

    def test_string_representation(self):
        """
        Test string representation of context
        """
        # Normal state
        self.assertIn("IN_PROGRESS", str(self.context))
        
        # Complete state
        self.context.current_stage = PipelineStage.COMPLETE
        self.assertIn("COMPLETE", str(self.context))
        
        # Error state
        self.context.error = "Test error"
        self.assertIn("ERROR", str(self.context))

if __name__ == '__main__':
    unittest.main()