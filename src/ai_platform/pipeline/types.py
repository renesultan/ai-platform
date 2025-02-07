"""
Core types for the pipeline system.
Defines the fundamental data structures used throughout the pipeline.
"""

from typing import Any, Dict, Optional
from enum import Enum

class PipelineStage(Enum):
    """
    Enumeration of possible pipeline stages.
    Helps track where in the pipeline a request currently is.
    """
    INIT = "initialization"
    INPUT_VALIDATION = "input_validation"
    CONTEXT_ENHANCEMENT = "context_enhancement"
    MODEL_ROUTING = "model_routing"
    GENERATION = "generation"
    OUTPUT_VALIDATION = "output_validation"
    COMPLETE = "complete"
    ERROR = "error"

class PipelineContext:
    """
    Holds the state and data for a request as it moves through the pipeline.

    This class:
    - Maintains the original query and any modified versions
    - Tracks current pipeline stage
    - Stores results from each stage
    - Maintains error state if any
    - Provides controlled access to the state and data for logging and debugging
    """
    def __init__(
            self,
            query_id: str,
            original_query: str,
            current_stage: PipelineStage = PipelineStage.INIT,
            modified_query: Optional[str] = None,
            stage_results: Optional[Dict[PipelineStage, Any]] = None,
            final_response: Optional[str] = None,
            error: Optional[str] = None,
            error_stage: Optional[PipelineStage] = None                    
    ):
        # Core request data
        self.query_id = query_id
        self.original_query = original_query
        
        # Current state
        self.current_stage = current_stage
        self.modified_query = modified_query

        # Results storage; use an empty dictionary if none provided
        if stage_results is None:
            self.stage_results = {}
        else:
            self.stage_results = stage_results

        self.final_response = final_response

        # Error tracking
        self.error = error
        self.error_stage = error_stage

    @property
    def has_error(self) -> bool:
        """
        Check if the pipeline has encountered an error.
        """
        return self.error is not None
    
    @property
    def is_complete(self):
        """
        Check if the pipeline has completed processing.
        """
        return self.current_stage in (PipelineStage.COMPLETE, PipelineStage.ERROR)
    
    def get_stage_result(self, stage: PipelineStage) -> Optional[Any]:
        """
        Safely retrieve result from a specific pipeline stage.

        Args:
            stage: The pipeline stage for which to get the results.

        Returns:
            The result of that stage if it exists, or None otherwise.
        """
        return self.stage_results.get(stage)
    
    def __str__(self) -> str:
        """
        Return a human-readable string representation for the PipelineContext.
        Useful for logging and debugging.
        """
        status = "ERROR" if self.has_error else "COMPLETE" if self.is_complete else "IN_PROGRESS"
        return(
            f"PipelineContext(id={self.query_id}, "
            f"stage={self.current_stage.value}, "
            f"status={status})"
        )