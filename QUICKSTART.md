# Quick Start Guide

Get up and running in 60 seconds.

## Option 1: Zero Setup (Use v1.0)

The original system works with ZERO dependencies:

```bash
# Just run it
python -m src.main

# Output appears in output/ directory
ls output/
```

**Output**: 5 files (JSON, text formats for JD, plan, rubric, timeline)

---

## Option 2: Enhanced (Recommended)

Get 78% more skills detected:

```bash
# Step 1: Install minimal dependencies
pip install pydantic pyyaml cachetools click

# Step 2: Run enhanced system
python -m src.main

# Step 3: See the improvement
python benchmark.py
```

**Benefit**: Finds more skills, adds salary insights, market comparison

---

## Option 3: Use CLI

More control over inputs/outputs:

```bash
# Install CLI deps
pip install pydantic pyyaml cachetools click

# Generate with custom files
python -m src.cli.interactive generate \
    your_job_descriptions.json \
    your_company_info.json \
    --output custom_output/

# See all options
python -m src.cli.interactive --help
```

---

## Option 4: Run as API

For programmatic access:

```bash
# Install API deps
pip install fastapi uvicorn aiofiles pydantic pyyaml cachetools

# Start server
python -m src.api.server

# Visit http://localhost:8000/docs for API docs

# Or use curl
curl http://localhost:8000/health
```

---

## Input File Format

### Job Descriptions (`job_descriptions.json`):

```json
[
  {
    "title": "Senior Product Manager",
    "company": "TechCorp",
    "location": "San Francisco",
    "salary_range": "$150k - $180k",
    "description": "Full job description text here..."
  }
]
```

**Minimum**: 3 job descriptions (recommended: 5-10)

### Company Info (`company_info.json`):

```json
{
  "company_name": "Your Company",
  "department": "Product",
  "experience_level": "Senior",
  "location": "Remote",
  "salary_range": "$160k - $190k",
  "mission": "Your company mission"
}
```

**See**: `examples/` directory for complete examples

---

## What You Get

After running, you'll have:

1. **Job Description** - Ready to post
2. **Hiring Plan** - Strategy, sourcing, budget
3. **Interview Rubric** - 7 stages with questions
4. **Timeline** - Week-by-week plan
5. **Complete JSON** - All data structured

---

## Troubleshooting

### "No module named 'pydantic'"

```bash
pip install pydantic pyyaml cachetools click
```

### "Config file not found"

```bash
# Config is optional, system uses defaults
# If you want custom config:
cp config/default.yaml config/custom.yaml
export HIRING_SYSTEM_CONFIG=config/custom.yaml
```

### "Tests failing"

```bash
# Install test deps
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

---

## Next Steps

1. **Review Output**: Check `output/` directory
2. **Customize**: Edit company info JSON
3. **Iterate**: Run again with different inputs
4. **Benchmark**: Run `python benchmark.py` to see improvements

---

## Help

- **Examples**: `examples/` directory
- **Tests**: `pytest tests/` to verify setup
- **Features**: `WORKING_FEATURES.md` for details
- **Issues**: Check logs at `logs/hiring_system.log`

---

**Time to first output**: < 60 seconds

**That's it!** Simple, fast, practical.
