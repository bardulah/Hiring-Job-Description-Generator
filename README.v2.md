# Hiring System Generator v2.0

A comprehensive, production-ready system that creates job descriptions, hiring plans, interview rubrics, and hiring timelines using NLP analysis and intelligent insights.

## 🚀 What's New in v2.0

### Major Improvements

- **🧠 NLP-Powered Analysis**: Intelligent text analysis using spaCy for better skill extraction
- **⚡ FastAPI Web Service**: RESTful API with async processing
- **🎯 Interactive CLI**: User-friendly wizard for generation
- **✅ Pydantic Validation**: Type-safe data models with validation
- **💾 Caching System**: Performance optimization with TTL caching
- **📊 Analytics & Insights**: Track usage and hiring outcomes
- **📄 Multiple Export Formats**: JSON, Text, Markdown, and PDF
- **🔧 Configuration Management**: YAML-based configuration
- **🪵 Comprehensive Logging**: Structured logging for debugging
- **🧪 Full Test Coverage**: Unit and integration tests

## Architecture

```
Hiring-Job-Description-Generator/
├── src/
│   ├── core/              # Core functionality
│   │   ├── models.py      # Pydantic models
│   │   ├── config.py      # Configuration management
│   │   ├── exceptions.py  # Custom exceptions
│   │   ├── logging_config.py
│   │   ├── cache.py       # Caching system
│   │   └── analytics.py   # Analytics tracking
│   ├── analyzers/         # Analysis engines
│   │   └── nlp_analyzer.py
│   ├── generators/        # Content generators
│   │   ├── base_generator.py
│   │   ├── job_description_generator.py
│   │   ├── hiring_plan_generator.py
│   │   ├── interview_rubric_generator.py
│   │   └── timeline_generator.py
│   ├── exporters/         # Multi-format exporters
│   │   └── multi_format_exporter.py
│   ├── api/               # FastAPI web service
│   │   ├── server.py
│   │   └── tasks.py
│   ├── cli/               # Interactive CLI
│   │   └── interactive.py
│   └── [legacy modules]   # Original generators
├── config/                # Configuration files
│   └── default.yaml
├── templates/             # External templates
├── tests/                 # Test suite
│   ├── unit/
│   └── integration/
├── examples/              # Example data
├── output/                # Generated files
└── data/                  # Analytics data
```

## Installation

### Requirements

- Python 3.9+
- pip

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/Hiring-Job-Description-Generator.git
cd Hiring-Job-Description-Generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model (optional, for NLP features)
python -m spacy download en_core_web_sm
```

## Quick Start

### 1. Interactive Mode (Recommended)

The easiest way to get started:

```bash
python -m src.cli.interactive interactive
```

This launches an interactive wizard that guides you through:
- Company information
- Hiring goals
- Job description sources
- Output preferences

### 2. Command Line

Generate from existing files:

```bash
python -m src.cli.interactive generate \
    examples/sample_job_descriptions.json \
    examples/sample_company_info.json \
    --output ./output \
    --format json --format text --format markdown
```

### 3. Python API

```python
from src.analyzers.nlp_analyzer import NLPAnalyzer
from src.generators.job_description_generator import EnhancedJobDescriptionGenerator
from src.core.models import JobDescription, CompanyInfo

# Create analyzer
analyzer = NLPAnalyzer()

# Analyze job descriptions
job_descriptions = [
    JobDescription(
        title="Senior Product Manager",
        company="TechCorp",
        description="..."
    )
    # ... more descriptions
]

analysis = analyzer.analyze_multiple_descriptions(job_descriptions)

# Generate job description
generator = EnhancedJobDescriptionGenerator()
company_info = CompanyInfo(
    company_name="Acme Corp",
    experience_level="Senior"
)

job_desc = generator.generate(
    analysis=analysis.dict(),
    company_info=company_info.dict()
)
```

### 4. Web API

Start the FastAPI server:

```bash
python -m src.api.server
```

Then visit `http://localhost:8000/docs` for interactive API documentation.

#### API Examples

```bash
# Health check
curl http://localhost:8000/health

# Analyze job descriptions
curl -X POST http://localhost:8000/api/v1/analyze \
    -H "Content-Type: application/json" \
    -d @examples/sample_job_descriptions.json

# Generate complete hiring system
curl -X POST http://localhost:8000/api/v1/generate \
    -H "Content-Type: application/json" \
    -d '{
        "external_job_descriptions": [...],
        "company_info": {...},
        "output_formats": ["json", "text", "markdown"]
    }'

# Check generation status
curl http://localhost:8000/api/v1/status/{request_id}

# Get statistics
curl http://localhost:8000/api/v1/stats
```

## Configuration

Edit `config/default.yaml` to customize behavior:

```yaml
analysis:
  min_job_descriptions: 3
  skill_threshold: 0.3
  use_nlp: true

generation:
  default_experience_level: "Mid-Level"
  include_salary: true

interview:
  default_stages: 7
  include_technical: true

cache:
  enabled: true
  ttl: 3600
  max_size: 100

api:
  host: "0.0.0.0"
  port: 8000

analytics:
  enabled: true
  track_usage: true
```

Or set via environment variable:

```bash
export HIRING_SYSTEM_CONFIG=/path/to/custom/config.yaml
```

## Features in Detail

### NLP-Powered Analysis

The analyzer uses advanced NLP techniques to:
- Extract skills with context understanding
- Categorize skills by type (technical, business, leadership, etc.)
- Identify experience levels intelligently
- Parse salary ranges and benefits
- Detect company size and stage
- Extract education requirements

### Caching

Expensive operations are cached automatically:

```python
from src.core.cache import cached

@cached(ttl=3600)
def expensive_operation(arg):
    # Results cached for 1 hour
    return result
```

### Analytics

Track hiring outcomes and get insights:

```python
from src.core.analytics import analytics_manager

# Record hiring outcome
feedback = FeedbackRecord(
    candidate_id="123",
    role="Senior PM",
    hired=True,
    time_to_hire=45,
    performance_rating=4.5
)
analytics_manager.record_feedback(feedback)

# Get insights
stats = analytics_manager.get_usage_stats(days=30)
insights = analytics_manager.get_feedback_insights()
recommendations = analytics_manager.generate_recommendations()
```

### Export Formats

Generate output in multiple formats:

- **JSON**: Structured data for programmatic use
- **Text**: Human-readable formatted text
- **Markdown**: Documentation-friendly format
- **PDF**: Professional print-ready documents

## Testing

```bash
# Run all tests
pytest

# Run specific test types
pytest tests/unit
pytest tests/integration

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_models.py::TestJobDescription::test_valid_job_description
```

## Performance

### Caching

Results are cached automatically:
- Analysis results: 1 hour TTL
- Generated content: 1 hour TTL
- API responses: Per endpoint configuration

### Async Processing

API endpoints use async processing for long-running tasks:
- Submit request → Get request_id
- Poll status endpoint for progress
- Retrieve results when complete

## Monitoring

### Logs

Logs are written to `logs/hiring_system.log`:

```bash
# View logs
tail -f logs/hiring_system.log

# Search logs
grep "ERROR" logs/hiring_system.log
```

### Analytics Dashboard

```bash
# View statistics
python -m src.cli.interactive stats
```

## Production Deployment

### Docker (Coming Soon)

```bash
docker build -t hiring-system .
docker run -p 8000:8000 hiring-system
```

### Environment Variables

```bash
HIRING_SYSTEM_CONFIG=/path/to/config.yaml
LOG_LEVEL=INFO
API_PORT=8000
```

## Troubleshooting

### spaCy Model Not Found

```bash
python -m spacy download en_core_web_sm
```

### Import Errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### API Not Starting

Check port availability:
```bash
lsof -i :8000
```

## Migration from v1.0

The v1.0 API is still available for backward compatibility:

```python
# Old way (still works)
from src.main import HiringSystemGenerator

generator = HiringSystemGenerator()
system = generator.generate_complete_system(...)

# New way (recommended)
from src.analyzers.nlp_analyzer import NLPAnalyzer
from src.generators.job_description_generator import EnhancedJobDescriptionGenerator

analyzer = NLPAnalyzer()
generator = EnhancedJobDescriptionGenerator()
```

## Contributing

Contributions welcome! Areas for improvement:

- [ ] Additional role types beyond PM
- [ ] More NLP models and languages
- [ ] ATS integrations
- [ ] Real-time market data APIs
- [ ] Machine learning for predictions
- [ ] Docker and Kubernetes support
- [ ] More export formats

## License

MIT License - see LICENSE file

## Support

- **Documentation**: Check this README and `/docs` endpoint
- **Issues**: Open an issue on GitHub
- **Examples**: See `examples/` directory
- **API Docs**: Visit `/docs` when API is running

## Changelog

### v2.0.0 (2025-11-06)

**Major Rewrite**

- Complete architecture overhaul
- Added NLP-based analysis
- FastAPI web service
- Interactive CLI
- Pydantic validation
- Caching system
- Analytics tracking
- Multiple export formats
- Comprehensive tests
- Production-ready features

### v1.0.0 (2025-11-05)

- Initial release
- Basic generation functionality

---

Built with intelligence to help you hire amazing talent! 🚀
