"""
Pipeline orchestration for managing sequence of processing steps.
"""
from typing import List, Optional
from uuid import uuid4

from .types import PipelineContext, PipelineStage
from .interfaces import PipelineStep, PipelineStepError

class PipelineError(Exception):
    """
    Custom exception for pipeline-level errors.
    Distinct from step-specific errors.
    """
    pass

class Pipeline:
    """
    Orchestrates the execution of multiple pipeline steps.

    The pipeline:
    - Maintains ordered sequence of processing steps
    - Executes steps in order on provided context
    - Handles errors at both step and pipeline levels
    - Ensures proper state transitions
    - Provides execution status and results
    """
    def __init__(self, steps: List[PipelineStep]):
        """
        Initialize a pipeline with sequence of steps.

        Args:
            steps: Ordered list of pipeline steps to execute

        Raises:
            PipelineError: If steps list is empty or contains duplicates
        """
        if not steps:
            raise PipelineError("Pipeline must contain at least one step")
        
        # Check for duplicate stages
        stages = [step.stage for step in steps]
        if len(stages) != len(set(stages)):
            raise PipelineError("Pipeline cannot contain duplicate stages")
        
        self._steps = steps

    def process(
            self,
            query: str,
            query_id: Optional[str] = None
    ) -> PipelineContext:
        """
        Process a query through the pipeline.

        Args:
            query: The query to process
            query_id: Optional identifier for the query

        Returns: 
            The final pipeline context after processing

        Raises:
            PipelineError: If pipeline execution fails
        """
        try:
            # Create initial context
            context = PipelineContext(
                query_id=query_id or str(uuid4),
                original_query=query
            )

            # Process through each step
            for step in self._steps:
                if context.has_error:
                    break

                try:
                    context = step.process(context)
                except Exception as e:
                    # Convert any exception to PipelineStepError
                    if not isinstance(e, PipelineStepError):
                        e = PipelineStepError(str(e), step.stage)
                    context = step._handle_error(context, e)

            # Mark as complete if no errors
            if not context.has_error:
                context.current_stage = PipelineStage.COMPLETE

            return context
        
        except Exception as e:
            raise PipelineError(f"Pipeline execution failed: {str(e)}")
        
    @property
    def steps(self) -> List[PipelineStep]:
        """
        Get the pipeline's steps.
        Returns a copy to prevent modification.
        """
        return self._steps.copy()
    
    def get_step_by_stage(self, stage: PipelineStage) -> Optional[PipelineStep]:
        """
        Find a step by its stage.

        Args:
            stage: The stage to find

        Returns:
            The matching step if found, None otherwise
        """
        for step in self._steps:
            if step.stage == stage:
                return step
        return None
    
    def __str__(self) -> str:
        """
        Human-readable string representation.
        Useful for debugging pipeline configuration.
        """
        stages = [step.stage.value for step in self._steps]
        return f"Pipeline(stages=[{' -> '.join(stages)}])"