"""
Tests for pipeline orchestration
"""
import unittest
from typing import Optional

from src.ai_platform.pipeline.types import PipelineContext, PipelineStage
from src.ai_platform.pipeline.interfaces import PipelineStep, PipelineStepError
from src.ai_platform.pipeline.pipeline import Pipeline, PipelineError

class MockStep(PipelineStep):
    """
    Mock pipeline step for testing
    """
    def __init__(self, stage: PipelineStage, should_fail: bool = False):
        super().__init__(stage)
        self.should_fail = should_fail
        self.times_called = 0

    def process(self, context: PipelineContext) -> PipelineContext:
        self.times_called += 1
        if self.should_fail:
            raise PipelineStepError("Step failed", self.stage)
        return self._update_context(context, f"Result from {self.stage.value}")

class TestPipeline(unittest.TestCase):
    """
    Test cases for Pipeline orchestrator
    """
    def setUp(self):
        """
        Set up test fixtures
        """
        self.step1 = MockStep(PipelineStage.INPUT_VALIDATION)
        self.step2 = MockStep(PipelineStage.GENERATION)
        self.pipeline = Pipeline([self.step1, self.step2])

    def test_initialization_validation(self):
        """
        Test pipeline initialization validation
        """
        # Test empty steps
        with self.assertRaises(PipelineError):
            Pipeline([])

        # Test duplicate stages
        step1 = MockStep(PipelineStage.GENERATION)
        step2 = MockStep(PipelineStage.GENERATION)
        with self.assertRaises(PipelineError):
            Pipeline([step1, step2])

    def test_successful_processing(self):
        """
        Test successful pipeline execution
        """
        context = self.pipeline.process("Test query")
        
        self.assertEqual(context.current_stage, PipelineStage.COMPLETE)
        self.assertFalse(context.has_error)
        self.assertEqual(self.step1.times_called, 1)
        self.assertEqual(self.step2.times_called, 1)

    def test_step_failure(self):
        """
        Test pipeline handling of step failure
        """
        failing_step = MockStep(PipelineStage.INPUT_VALIDATION, should_fail=True)
        pipeline = Pipeline([failing_step, self.step2])
        
        context = pipeline.process("Test query")
        
        self.assertTrue(context.has_error)
        self.assertEqual(context.current_stage, PipelineStage.ERROR)
        self.assertEqual(context.error_stage, PipelineStage.INPUT_VALIDATION)
        self.assertEqual(failing_step.times_called, 1)
        self.assertEqual(self.step2.times_called, 0)  # Should not be called

    def test_get_step_by_stage(self):
        """
        Test retrieving steps by stage
        """
        step = self.pipeline.get_step_by_stage(PipelineStage.INPUT_VALIDATION)
        self.assertEqual(step, self.step1)
        
        # Test nonexistent stage
        self.assertIsNone(
            self.pipeline.get_step_by_stage(PipelineStage.CONTEXT_ENHANCEMENT)
        )

    def test_steps_property(self):
        """
        Test steps property returns copy
        """
        steps = self.pipeline.steps
        self.assertEqual(steps, self.pipeline._steps)
        self.assertIsNot(steps, self.pipeline._steps)

    def test_string_representation(self):
        """
        Test pipeline string representation
        """
        expected = "Pipeline(stages=[input_validation -> generation])"
        self.assertEqual(str(self.pipeline), expected)

if __name__ == '__main__':
    unittest.main()