# Hiring System Generator

A comprehensive system that creates job descriptions, hiring plans, interview rubrics, and hiring timelines by analyzing your company's PM hiring materials and similar role descriptions from other companies.

## Overview

The Hiring System Generator is an intelligent tool that helps you build a complete hiring infrastructure for Product Manager roles. By analyzing existing job descriptions from top companies and combining them with your company's specific requirements, it generates:

1. **Job Descriptions** - Comprehensive, well-structured job descriptions tailored to your company
2. **Hiring Plans** - Strategic hiring plans with sourcing strategies, budgets, and success metrics
3. **Interview Rubrics** - Detailed interview guides with questions, evaluation criteria, and scoring frameworks
4. **Hiring Timelines** - Week-by-week timelines with milestones, dependencies, and risk mitigation

## Features

### 🔍 Job Description Analysis
- Analyzes multiple job descriptions to extract common patterns
- Identifies key skills, responsibilities, and qualifications
- Determines experience levels and salary ranges
- Extracts remote work policies and company culture indicators

### 📝 Job Description Generation
- Creates structured job descriptions for all experience levels (Entry, Mid, Senior, Lead/Principal)
- Customizable sections: responsibilities, qualifications, skills, compensation, benefits
- Incorporates industry best practices and your company's unique requirements
- Generates both structured JSON and formatted text output

### 📋 Hiring Plan Creation
- Develops comprehensive hiring strategy aligned with your goals
- Multi-channel sourcing plan (referrals, direct sourcing, job boards, agencies)
- Detailed budget breakdown (recruiting costs, compensation, onboarding)
- Success metrics and KPIs for tracking hiring performance
- Risk analysis with mitigation strategies

### 📊 Interview Rubric Development
- Creates structured interview process with multiple stages
- Detailed rubrics for each interview type (product sense, execution, technical, leadership)
- Specific questions and evaluation criteria for each stage
- Scoring frameworks and decision-making guidelines
- Interviewer training materials and best practices

### 📅 Hiring Timeline Generation
- Week-by-week breakdown of hiring activities
- Key milestones and dependencies
- Resource allocation planning
- Risk timeline with buffers and contingencies
- Communication plan for candidates and stakeholders

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Hiring-Job-Description-Generator.git
cd Hiring-Job-Description-Generator

# No external dependencies required - uses Python standard library only!
# Requires Python 3.7+
```

## Quick Start

### Using Example Data

The easiest way to get started is to use the provided example files:

```bash
python -m src.main
```

This will use the sample job descriptions and company info from the `examples/` directory and generate a complete hiring system in the `output/` directory.

### Using Custom Data

1. **Prepare your input files:**

   - **Job Descriptions** (`job_descriptions.json`): A JSON array of job descriptions from other companies
   - **Company Info** (`company_info.json`): Your company's specific requirements and information

2. **Run the generator:**

```bash
python -m src.main path/to/job_descriptions.json path/to/company_info.json output_directory
```

## Input File Formats

### Job Descriptions File

A JSON array containing job descriptions from other companies:

```json
[
  {
    "title": "Senior Product Manager",
    "company": "TechCorp",
    "location": "San Francisco, CA",
    "salary_range": "$150,000 - $180,000",
    "description": "Full job description text including responsibilities, requirements, etc."
  },
  {
    "title": "Product Manager",
    "company": "StartupXYZ",
    "location": "Remote",
    "salary_range": "$130,000 - $160,000",
    "description": "Full job description text..."
  }
]
```

### Company Info File

A JSON object with your company's specific information:

```json
{
  "company_name": "Acme Technologies",
  "department": "Product",
  "experience_level": "Senior",
  "location": "San Francisco, CA / Remote",
  "employment_type": "Full-Time",
  "mission": "your company mission",
  "about": "Description of your company",
  "product_focus": "What products you're building",
  "salary_range": "$160,000 - $190,000",
  "equity": "0.15% - 0.25% stock options",
  "bonus": "Up to 20% annual performance bonus",
  "benefits": [
    "List of company benefits"
  ],
  "custom_responsibilities": [
    "Company-specific responsibilities"
  ],
  "required_qualifications": [
    "Must-have qualifications"
  ],
  "preferred_qualifications": [
    "Nice-to-have qualifications"
  ],
  "required_skills": [
    "Specific skills needed"
  ]
}
```

## Project Structure

```
Hiring-Job-Description-Generator/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Main orchestrator
│   ├── analyzer.py           # Job description analyzer
│   ├── job_description.py    # Job description generator
│   ├── hiring_plan.py        # Hiring plan generator
│   ├── interview_rubric.py   # Interview rubric generator
│   └── timeline.py           # Timeline generator
├── examples/
│   ├── sample_job_descriptions.json
│   └── sample_company_info.json
├── output/                   # Generated files go here
├── README.md
└── requirements.txt
```

## Output Files

The generator creates the following files in your output directory:

1. **Complete JSON** (`*_complete.json`) - All generated data in structured JSON format
2. **Job Description** (`*_job_description.txt`) - Formatted job description ready to post
3. **Hiring Plan** (`*_hiring_plan.txt`) - Complete hiring strategy and plan
4. **Interview Rubric** (`*_interview_rubric.txt`) - Detailed interview guides and rubrics
5. **Timeline** (`*_timeline.txt`) - Week-by-week hiring timeline

All files are timestamped for easy version tracking.

## Usage Examples

### Example 1: Generate for Senior PM Role

```python
from src.main import HiringSystemGenerator, load_json_file

# Load your data
job_descriptions = load_json_file('examples/sample_job_descriptions.json')
company_info = load_json_file('examples/sample_company_info.json')

# Create generator
generator = HiringSystemGenerator()

# Generate complete system
system = generator.generate_complete_system(
    external_job_descriptions=job_descriptions,
    company_info=company_info,
    hiring_goals={
        'target_headcount': 2,
        'urgency': 'high',
        'hiring_manager': 'VP of Product'
    }
)

# Save to files
files = generator.save_system(system, output_dir='output')
```

### Example 2: Customize Interview Process

```python
# Disable technical interview for non-technical PM role
system = generator.generate_complete_system(
    external_job_descriptions=job_descriptions,
    company_info=company_info,
    hiring_config={
        'include_technical': False
    }
)
```

### Example 3: Generate with Specific Start Date

```python
system = generator.generate_complete_system(
    external_job_descriptions=job_descriptions,
    company_info=company_info,
    start_date='2025-12-01'
)
```

## Customization

### Experience Levels

The system supports four experience levels, each with tailored content:

- **Entry-Level** (0-2 years): APM or junior PM roles
- **Mid-Level** (3-5 years): Standard PM roles
- **Senior** (6-9 years): Senior PM with leadership responsibilities
- **Lead/Principal** (10+ years): Lead PM with team management and strategic scope

### Interview Stages

Default interview process includes:

1. Recruiter Screening (30 min)
2. Product Sense & Strategy (60 min)
3. Execution & Analytics (60 min)
4. Technical Understanding (45-60 min)
5. Leadership & Influence (60 min, for Senior+ roles)
6. Behavioral & Cultural Fit (45 min)
7. Final Round with Executive (45-60 min)

### Hiring Timeline

Timeline duration varies by experience level:

- Entry-Level: 6 weeks
- Mid-Level: 8 weeks
- Senior: 10 weeks
- Lead/Principal: 12 weeks

## Best Practices

### For Best Results

1. **Provide 5-10 job descriptions** from similar companies for analysis
2. **Include diverse sources** (startups, big tech, competitors)
3. **Be specific in company info** - the more detail, the better the output
4. **Review and customize** the generated content to match your voice and culture
5. **Update regularly** as you learn from your hiring process

### Tips

- Use the generated job description as a starting point and refine based on your specific needs
- Share interview rubrics with your team before starting interviews
- Track your actual hiring metrics against the timeline to improve future processes
- Customize the evaluation criteria to match your company's values

## Architecture

The system uses a modular architecture:

1. **Analyzer** - Extracts insights from external job descriptions
2. **Generator Modules** - Each generator focuses on one aspect (JD, plan, rubric, timeline)
3. **Orchestrator** - Coordinates all generators and manages data flow
4. **Formatters** - Convert structured data to human-readable formats

All modules are loosely coupled and can be used independently if needed.

## Contributing

Contributions are welcome! Areas for improvement:

- Support for other roles beyond Product Manager
- Integration with ATS systems
- Machine learning for better pattern recognition
- Additional interview question banks
- Multi-language support

## License

MIT License - feel free to use and modify as needed.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the examples directory for reference
- Review the generated output format

## Changelog

### Version 1.0.0
- Initial release
- Support for Product Manager roles (Entry to Lead/Principal)
- Job description analyzer and generator
- Hiring plan generator
- Interview rubric generator
- Timeline generator
- Example files and documentation

---

Built with care to help you hire amazing Product Managers! 🚀
