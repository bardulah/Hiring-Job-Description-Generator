"""
Main Hiring System Generator
Orchestrates the complete hiring system generation process.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

from .analyzer import JobDescriptionAnalyzer
from .job_description import JobDescriptionGenerator
from .hiring_plan import HiringPlanGenerator
from .interview_rubric import InterviewRubricGenerator
from .timeline import HiringTimelineGenerator


class HiringSystemGenerator:
    """
    Main class that orchestrates the generation of comprehensive hiring materials.
    """

    def __init__(self):
        self.analyzer = JobDescriptionAnalyzer()
        self.jd_generator = JobDescriptionGenerator()
        self.plan_generator = HiringPlanGenerator()
        self.rubric_generator = InterviewRubricGenerator()
        self.timeline_generator = HiringTimelineGenerator()

    def generate_complete_system(self,
                                 external_job_descriptions: List[Dict[str, Any]],
                                 company_info: Dict[str, Any],
                                 hiring_goals: Optional[Dict[str, Any]] = None,
                                 hiring_config: Optional[Dict[str, Any]] = None,
                                 start_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate complete hiring system including job description, hiring plan,
        interview rubrics, and timeline.

        Args:
            external_job_descriptions: List of job descriptions from other companies
            company_info: Company-specific information and requirements
            hiring_goals: Hiring goals and constraints (optional)
            hiring_config: Configuration for interview process (optional)
            start_date: Start date for timeline in YYYY-MM-DD format (optional)

        Returns:
            Dict containing all generated hiring materials
        """
        print("🚀 Starting Hiring System Generation...\n")

        # Set defaults
        if hiring_goals is None:
            hiring_goals = {
                'target_headcount': 1,
                'urgency': 'medium',
                'hiring_manager': 'VP of Product'
            }

        if hiring_config is None:
            hiring_config = {
                'include_technical': True
            }

        # Step 1: Analyze external job descriptions
        print("📊 Step 1: Analyzing external job descriptions...")
        analysis = self.analyzer.analyze_multiple_descriptions(external_job_descriptions)
        print(f"   ✓ Analyzed {analysis['total_analyzed']} job descriptions")
        print(f"   ✓ Identified {len(analysis['common_skills'])} common skills")
        print()

        # Step 2: Generate job description
        print("📝 Step 2: Generating job description...")
        job_description = self.jd_generator.generate(analysis, company_info)
        print(f"   ✓ Generated job description for {job_description['header']['title']}")
        print(f"   ✓ Experience level: {job_description['metadata']['experience_level']}")
        print()

        # Step 3: Generate hiring plan
        print("📋 Step 3: Creating hiring plan...")
        hiring_plan = self.plan_generator.generate(job_description, hiring_goals)
        print(f"   ✓ Created hiring strategy and sourcing plan")
        print(f"   ✓ Target headcount: {hiring_plan['metadata']['target_headcount']}")
        print()

        # Step 4: Generate interview rubrics
        print("📊 Step 4: Building interview rubrics...")
        interview_rubric = self.rubric_generator.generate(job_description, hiring_config)
        print(f"   ✓ Created {len(interview_rubric['interview_stages'])} interview stages")
        print(f"   ✓ Total interview time: {interview_rubric['metadata']['total_interview_time']}")
        print()

        # Step 5: Generate timeline
        print("📅 Step 5: Generating hiring timeline...")
        timeline = self.timeline_generator.generate(job_description, hiring_plan, start_date)
        print(f"   ✓ Created {timeline['metadata']['estimated_duration_weeks']}-week timeline")
        print(f"   ✓ Target hire date: {timeline['metadata']['target_hire_date']}")
        print()

        # Compile complete system
        complete_system = {
            'metadata': {
                'generated_date': datetime.now().isoformat(),
                'system_version': '1.0.0',
                'company': company_info.get('company_name', 'Your Company'),
                'role': job_description['header']['title']
            },
            'analysis': analysis,
            'job_description': job_description,
            'hiring_plan': hiring_plan,
            'interview_rubric': interview_rubric,
            'timeline': timeline
        }

        print("✅ Hiring System Generation Complete!\n")
        return complete_system

    def save_system(self, system: Dict[str, Any], output_dir: str = 'output') -> Dict[str, str]:
        """
        Save generated system to files.

        Args:
            system: Complete generated system
            output_dir: Directory to save files

        Returns:
            Dict with paths to saved files
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Generate timestamp for filenames
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        role_slug = system['metadata']['role'].lower().replace(' ', '_')

        files = {}

        # Save complete system as JSON
        json_path = os.path.join(output_dir, f'{role_slug}_{timestamp}_complete.json')
        with open(json_path, 'w') as f:
            json.dump(system, f, indent=2)
        files['complete_json'] = json_path

        # Save job description as text
        jd_path = os.path.join(output_dir, f'{role_slug}_{timestamp}_job_description.txt')
        with open(jd_path, 'w') as f:
            f.write(self.jd_generator.format_as_text(system['job_description']))
        files['job_description'] = jd_path

        # Save hiring plan as text
        plan_path = os.path.join(output_dir, f'{role_slug}_{timestamp}_hiring_plan.txt')
        with open(plan_path, 'w') as f:
            f.write(self.plan_generator.format_as_text(system['hiring_plan']))
        files['hiring_plan'] = plan_path

        # Save interview rubric as text
        rubric_path = os.path.join(output_dir, f'{role_slug}_{timestamp}_interview_rubric.txt')
        with open(rubric_path, 'w') as f:
            f.write(self.rubric_generator.format_as_text(system['interview_rubric']))
        files['interview_rubric'] = rubric_path

        # Save timeline as text
        timeline_path = os.path.join(output_dir, f'{role_slug}_{timestamp}_timeline.txt')
        with open(timeline_path, 'w') as f:
            f.write(self.timeline_generator.format_as_text(system['timeline']))
        files['timeline'] = timeline_path

        print("💾 Saved files:")
        for file_type, path in files.items():
            print(f"   • {file_type}: {path}")
        print()

        return files

    def generate_and_save(self,
                         external_job_descriptions: List[Dict[str, Any]],
                         company_info: Dict[str, Any],
                         hiring_goals: Optional[Dict[str, Any]] = None,
                         hiring_config: Optional[Dict[str, Any]] = None,
                         start_date: Optional[str] = None,
                         output_dir: str = 'output') -> Dict[str, str]:
        """
        Generate complete system and save to files.

        Args:
            external_job_descriptions: List of job descriptions from other companies
            company_info: Company-specific information
            hiring_goals: Hiring goals and constraints (optional)
            hiring_config: Configuration for interview process (optional)
            start_date: Start date for timeline (optional)
            output_dir: Directory to save files

        Returns:
            Dict with paths to saved files
        """
        system = self.generate_complete_system(
            external_job_descriptions,
            company_info,
            hiring_goals,
            hiring_config,
            start_date
        )

        return self.save_system(system, output_dir)


def load_json_file(file_path: str) -> Any:
    """Load JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def main():
    """
    Main entry point for the hiring system generator.
    """
    import sys

    print("="*80)
    print("HIRING SYSTEM GENERATOR")
    print("="*80)
    print()

    # Check if example files are being used
    if len(sys.argv) > 1:
        # Custom files provided
        if len(sys.argv) < 3:
            print("Usage: python -m src.main <job_descriptions.json> <company_info.json> [output_dir]")
            sys.exit(1)

        jd_file = sys.argv[1]
        company_file = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else 'output'
    else:
        # Use example files
        print("📁 Using example files from examples/ directory\n")
        jd_file = 'examples/sample_job_descriptions.json'
        company_file = 'examples/sample_company_info.json'
        output_dir = 'output'

    # Load input files
    try:
        external_jds = load_json_file(jd_file)
        company_info = load_json_file(company_file)
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find file {e.filename}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in file - {e}")
        sys.exit(1)

    # Generate system
    generator = HiringSystemGenerator()

    # Optional: customize hiring goals
    hiring_goals = {
        'target_headcount': 1,
        'urgency': 'medium',
        'hiring_manager': 'VP of Product',
        'differentiators': company_info.get('differentiators', [])
    }

    # Generate and save
    files = generator.generate_and_save(
        external_job_descriptions=external_jds,
        company_info=company_info,
        hiring_goals=hiring_goals,
        output_dir=output_dir
    )

    print("="*80)
    print("🎉 SUCCESS! Your complete hiring system has been generated.")
    print("="*80)
    print()
    print("Next steps:")
    print("1. Review the generated job description and customize as needed")
    print("2. Share the hiring plan with your recruiting team")
    print("3. Train interviewers using the interview rubrics")
    print("4. Use the timeline to plan and track your hiring process")
    print()


if __name__ == '__main__':
    main()
