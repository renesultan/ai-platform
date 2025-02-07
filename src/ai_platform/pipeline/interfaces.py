"""
Abstract interfaces for pipeline functionality.
Defines contracts for pipeline steps and pipeline composition.
"""
from abc import ABC, abstractmethod
from typing import Optional, Any

from .types import PipelineContext, PipelineStage

class PipelineStepError(Exception):
    """
    Custom exception for pipeline step errors.
    Provides detailed error information including the failing stage.
    """
    def __init__(self, message: str, stage: PipelineStage):
        self.stage = stage
        super().__init__(f"Error in {stage.value}: {message}")

class PipelineStep(ABC):
    """
    Abstract interface for pipeline steps
    Each step in the pipeline must implement this interface.

    A pipeline step:
    - Takes a PipelineContext as input
    - Processes it according to its specific logic
    - Updates the context with results
    - Returns the modified context
    - Handles errors appropriately
    """
    def __init__(self, stage: PipelineStage):
        """
        Initialize pipeline step.

        Args:
            stage: The pipeline stage this step represents
        """
        self._stage = stage

    @property
    def stage(self) -> PipelineStage:
        """
        Get the pipeline stage this step represents.
        """
        return self._stage
    
    @abstractmethod
    def process(self, context: PipelineContext) -> PipelineContext:
        """ 
        Process the pipeline context.
        Must be implemented by concrete pipeline steps.

        Args:
            context: The pipeline context to process

        Returns:
            The modified pipeline context

        Raises:
            PipelineStageError: If processing fails
        """
        pass

    def _update_context(
            self,
            context: PipelineContext,
            result: Any,
            modified_query: Optional[str] = None
    ) -> PipelineContext:
        """
        Helper method to update context with step results.

        Args:
            context: The pipeline context to update
            result: The result to store for this stage
            modified_query: Optional modified version of the query

        Returns:
            The updated context
        """
        # Store result
        context.stage_results[self._stage] = result

        # Update query if modified
        if modified_query is not None:
            context.modified_query = modified_query

        # Update stage
        context.current_stage = self._stage

        return context
    
    def _handle_error(
            self,
            context: PipelineContext,
            error: Exception
    ) -> PipelineContext:
        """
        Helper method to handle errors during processing.

        Args:
            context: The pipeline context where error occurred
            error: The exception that was raised

        Returns:
            The updated context with error information
        """
        # Update error state
        context.error = str(error)
        context.error_stage = self._stage
        context.current_stage = PipelineStage.ERROR

        return context