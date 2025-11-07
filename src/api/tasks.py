"""
Background tasks for async processing.
"""

import time
from datetime import datetime
from typing import Dict, Any

from ..core.models import GenerationRequest, GenerationResponse
from ..core.logging_config import get_logger
from ..analyzers.nlp_analyzer import NLPAnalyzer
from ..core.exceptions import HiringSystemError

logger = get_logger(__name__)


async def generate_hiring_system_async(
    request_id: str,
    request: GenerationRequest,
    job_storage: Dict[str, Dict[str, Any]]
):
    """
    Generate hiring system asynchronously.

    Args:
        request_id: Unique request identifier
        request: Generation request with all inputs
        job_storage: Storage for job status and results
    """
    start_time = time.time()

    try:
        logger.info(f"Starting async generation for request {request_id}")

        # Update progress
        job_storage[request_id]['progress'] = 10
        job_storage[request_id]['status'] = 'analyzing'

        # Step 1: Analyze job descriptions
        analyzer = NLPAnalyzer()
        analysis = analyzer.analyze_multiple_descriptions(
            request.external_job_descriptions
        )

        job_storage[request_id]['progress'] = 30

        # Step 2: Generate job description
        # Import here to avoid circular imports
        from ..generators.job_description_generator import EnhancedJobDescriptionGenerator

        jd_generator = EnhancedJobDescriptionGenerator()
        job_description = await jd_generator.generate_async(
            analysis=analysis.dict(),
            company_info=request.company_info.dict()
        )

        job_storage[request_id]['progress'] = 50

        # Step 3: Generate hiring plan
        from ..generators.hiring_plan_generator import EnhancedHiringPlanGenerator

        plan_generator = EnhancedHiringPlanGenerator()
        hiring_goals = request.hiring_goals.dict() if request.hiring_goals else {}
        hiring_plan = await plan_generator.generate_async(
            job_description=job_description,
            hiring_goals=hiring_goals
        )

        job_storage[request_id]['progress'] = 70

        # Step 4: Generate interview rubric
        from ..generators.interview_rubric_generator import EnhancedInterviewRubricGenerator

        rubric_generator = EnhancedInterviewRubricGenerator()
        hiring_config = request.hiring_config.dict() if request.hiring_config else {}
        interview_rubric = await rubric_generator.generate_async(
            job_description=job_description,
            hiring_config=hiring_config
        )

        job_storage[request_id]['progress'] = 85

        # Step 5: Generate timeline
        from ..generators.timeline_generator import EnhancedTimelineGenerator

        timeline_generator = EnhancedTimelineGenerator()
        timeline = await timeline_generator.generate_async(
            job_description=job_description,
            hiring_plan=hiring_plan,
            start_date=hiring_goals.get('start_date') if hiring_goals else None
        )

        job_storage[request_id]['progress'] = 95

        # Step 6: Export results
        from ..exporters.multi_format_exporter import MultiFormatExporter

        exporter = MultiFormatExporter()
        output_files = await exporter.export_all_async(
            {
                'analysis': analysis.dict(),
                'job_description': job_description,
                'hiring_plan': hiring_plan,
                'interview_rubric': interview_rubric,
                'timeline': timeline
            },
            formats=request.output_formats,
            request_id=request_id
        )

        # Calculate processing time
        processing_time = time.time() - start_time

        # Create response
        response = GenerationResponse(
            request_id=request_id,
            generated_at=datetime.now(),
            status='completed',
            analysis=analysis,
            job_description=None,  # Too large for response, use files
            hiring_plan=None,
            interview_rubric=None,
            timeline=None,
            output_files=output_files,
            processing_time=processing_time
        )

        # Update job storage
        job_storage[request_id].update({
            'status': 'completed',
            'progress': 100,
            'completed_at': datetime.now(),
            'result': response.dict(),
            'processing_time': processing_time
        })

        logger.info(f"Generation completed for request {request_id} in {processing_time:.2f}s")

    except HiringSystemError as e:
        logger.error(f"Hiring system error in async task {request_id}: {e}")
        job_storage[request_id].update({
            'status': 'failed',
            'error': str(e),
            'completed_at': datetime.now()
        })

    except Exception as e:
        logger.error(f"Unexpected error in async task {request_id}: {e}", exc_info=True)
        job_storage[request_id].update({
            'status': 'failed',
            'error': 'Internal server error',
            'completed_at': datetime.now()
        })
