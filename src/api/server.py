"""
FastAPI web service for the Hiring System Generator.
"""

import uuid
import time
from typing import List, Dict, Any
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ..core.models import (
    GenerationRequest, GenerationResponse, JobDescription,
    CompanyInfo, HiringGoals, AnalysisResult
)
from ..core.config import config
from ..core.logging_config import get_logger
from ..core.exceptions import HiringSystemError, ValidationError
from ..analyzers.nlp_analyzer import NLPAnalyzer
from .tasks import generate_hiring_system_async

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Hiring System Generator API",
    description="RESTful API for generating comprehensive hiring materials",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
cors_origins = config.get('api.cors_origins', ['*'])
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for async jobs (in production, use Redis or database)
job_storage: Dict[str, Dict[str, Any]] = {}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Hiring System Generator API",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "generate": "/api/v1/generate",
            "status": "/api/v1/status/{request_id}",
            "analyze": "/api/v1/analyze"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cache": config.get('cache.enabled', True),
        "nlp": config.get('analysis.use_nlp', True)
    }


@app.post("/api/v1/generate", response_model=GenerationResponse, status_code=status.HTTP_202_ACCEPTED)
async def generate_hiring_system(
    request: GenerationRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate complete hiring system asynchronously.

    This endpoint accepts a generation request and processes it in the background.
    Use the returned request_id to check status.
    """
    try:
        # Generate unique request ID
        request_id = str(uuid.uuid4())

        # Initialize job status
        job_storage[request_id] = {
            'status': 'processing',
            'created_at': datetime.now(),
            'progress': 0
        }

        # Add background task
        background_tasks.add_task(
            generate_hiring_system_async,
            request_id,
            request,
            job_storage
        )

        logger.info(f"Started generation job: {request_id}")

        return GenerationResponse(
            request_id=request_id,
            generated_at=datetime.now(),
            status='processing'
        )

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error starting generation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/v1/status/{request_id}")
async def get_generation_status(request_id: str):
    """Get status of a generation request."""
    if request_id not in job_storage:
        raise HTTPException(status_code=404, detail="Request ID not found")

    job = job_storage[request_id]

    return {
        'request_id': request_id,
        'status': job['status'],
        'progress': job.get('progress', 0),
        'created_at': job['created_at'].isoformat(),
        'completed_at': job.get('completed_at', {}).isoformat() if job.get('completed_at') else None,
        'result': job.get('result'),
        'error': job.get('error')
    }


@app.post("/api/v1/analyze", response_model=AnalysisResult)
async def analyze_job_descriptions(job_descriptions: List[JobDescription]):
    """
    Analyze job descriptions without generating full system.
    Useful for quick insights and market research.
    """
    try:
        if len(job_descriptions) < 3:
            raise ValidationError("At least 3 job descriptions required for analysis")

        analyzer = NLPAnalyzer()
        result = analyzer.analyze_multiple_descriptions(job_descriptions)

        logger.info(f"Analyzed {len(job_descriptions)} job descriptions")

        return result

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except HiringSystemError as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/api/v1/jobs/{request_id}")
async def delete_job(request_id: str):
    """Delete a completed job and its results."""
    if request_id not in job_storage:
        raise HTTPException(status_code=404, detail="Request ID not found")

    del job_storage[request_id]
    logger.info(f"Deleted job: {request_id}")

    return {"message": "Job deleted successfully"}


@app.get("/api/v1/stats")
async def get_statistics():
    """Get system statistics."""
    from ..core.cache import cache_manager

    return {
        'total_jobs': len(job_storage),
        'active_jobs': sum(1 for j in job_storage.values() if j['status'] == 'processing'),
        'completed_jobs': sum(1 for j in job_storage.values() if j['status'] == 'completed'),
        'failed_jobs': sum(1 for j in job_storage.values() if j['status'] == 'failed'),
        'cache_stats': cache_manager.get_stats(),
        'config': {
            'nlp_enabled': config.get('analysis.use_nlp', True),
            'cache_enabled': config.get('cache.enabled', True)
        }
    }


@app.exception_handler(HiringSystemError)
async def hiring_system_error_handler(request, exc: HiringSystemError):
    """Handle custom hiring system errors."""
    logger.error(f"Hiring system error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "type": type(exc).__name__}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle unexpected errors."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn

    host = config.get('api.host', '0.0.0.0')
    port = config.get('api.port', 8000)

    logger.info(f"Starting API server on {host}:{port}")

    uvicorn.run(
        "src.api.server:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
