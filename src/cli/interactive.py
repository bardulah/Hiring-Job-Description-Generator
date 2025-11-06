"""
Interactive CLI for the Hiring System Generator.
"""

import click
import json
from pathlib import Path
from datetime import datetime

from ..core.models import CompanyInfo, HiringGoals, ExperienceLevel
from ..core.logging_config import get_logger
from ..analyzers.nlp_analyzer import NLPAnalyzer

logger = get_logger(__name__)


@click.group()
def cli():
    """Hiring System Generator - Interactive CLI"""
    pass


@cli.command()
def interactive():
    """Start interactive wizard for generating hiring system."""
    click.secho("\n" + "="*80, fg="cyan")
    click.secho("  HIRING SYSTEM GENERATOR - Interactive Mode", fg="cyan", bold=True)
    click.secho("="*80 + "\n", fg="cyan")

    try:
        # Step 1: Company Information
        click.secho("Step 1: Company Information", fg="yellow", bold=True)
        click.echo("Let's start by gathering information about your company.\n")

        company_name = click.prompt("Company name", type=str)
        department = click.prompt("Department", default="Product", type=str)

        # Experience level
        click.echo("\nExperience levels:")
        levels = ["Entry-Level", "Mid-Level", "Senior", "Lead/Principal"]
        for i, level in enumerate(levels, 1):
            click.echo(f"  {i}. {level}")
        level_choice = click.prompt("Choose experience level", type=click.IntRange(1, 4), default=2)
        experience_level = levels[level_choice - 1]

        location = click.prompt("Location", default="Remote", type=str)
        salary_range = click.prompt("Salary range (e.g., $120k - $150k)", type=str)

        # Optional details
        if click.confirm("\nWould you like to add more details?", default=True):
            mission = click.prompt("Company mission", default="", type=str)
            product_focus = click.prompt("Product focus", default="", type=str)
        else:
            mission = ""
            product_focus = ""

        # Step 2: Hiring Goals
        click.echo("\n")
        click.secho("Step 2: Hiring Goals", fg="yellow", bold=True)

        target_headcount = click.prompt("How many people to hire?", type=int, default=1)

        click.echo("\nUrgency levels:")
        urgencies = ["low", "medium", "high"]
        for i, urg in enumerate(urgencies, 1):
            click.echo(f"  {i}. {urg}")
        urgency_choice = click.prompt("Choose urgency", type=click.IntRange(1, 3), default=2)
        urgency = urgencies[urgency_choice - 1]

        hiring_manager = click.prompt("Hiring manager title", default="VP of Product", type=str)

        # Step 3: Job Descriptions
        click.echo("\n")
        click.secho("Step 3: External Job Descriptions", fg="yellow", bold=True)
        click.echo("You need to provide at least 3 job descriptions for analysis.\n")

        # Check if they have a file
        has_file = click.confirm("Do you have a JSON file with job descriptions?", default=False)

        if has_file:
            jd_file = click.prompt("Path to job descriptions file", type=click.Path(exists=True))
            with open(jd_file, 'r') as f:
                job_descriptions = json.load(f)
        else:
            click.echo("\nPlease use the examples/sample_job_descriptions.json file")
            click.echo("or create your own following the format in the documentation.")
            if not click.confirm("Continue with example file?", default=True):
                click.echo("Exiting...")
                return
            jd_file = "examples/sample_job_descriptions.json"
            with open(jd_file, 'r') as f:
                job_descriptions = json.load(f)

        # Step 4: Output Preferences
        click.echo("\n")
        click.secho("Step 4: Output Preferences", fg="yellow", bold=True)

        click.echo("\nAvailable formats:")
        available_formats = ["json", "text", "markdown", "pdf"]
        selected_formats = []

        for fmt in available_formats:
            if click.confirm(f"  Generate {fmt.upper()}?", default=(fmt in ["json", "text"])):
                selected_formats.append(fmt)

        output_dir = click.prompt("\nOutput directory", default="output", type=str)

        # Confirmation
        click.echo("\n")
        click.secho("="*80, fg="cyan")
        click.secho("Configuration Summary", fg="cyan", bold=True)
        click.secho("="*80, fg="cyan")
        click.echo(f"\nCompany: {company_name}")
        click.echo(f"Role: {experience_level} Product Manager")
        click.echo(f"Location: {location}")
        click.echo(f"Salary Range: {salary_range}")
        click.echo(f"Target Headcount: {target_headcount}")
        click.echo(f"Urgency: {urgency}")
        click.echo(f"Output Formats: {', '.join(selected_formats)}")
        click.echo(f"Output Directory: {output_dir}\n")

        if not click.confirm("Generate hiring system with these settings?", default=True):
            click.echo("Cancelled.")
            return

        # Generate
        click.echo("\n")
        click.secho("Generating hiring system...", fg="green", bold=True)

        # Import here to avoid circular imports
        from ..main import HiringSystemGenerator, load_json_file

        generator = HiringSystemGenerator()

        # Prepare data
        from ..core.models import JobDescription

        jds = [JobDescription(**jd) for jd in job_descriptions]

        company_info_dict = {
            'company_name': company_name,
            'department': department,
            'experience_level': experience_level,
            'location': location,
            'salary_range': salary_range,
            'mission': mission or f"innovate in {product_focus}" if product_focus else "create great products",
            'product_focus': product_focus or "innovative solutions"
        }

        hiring_goals = {
            'target_headcount': target_headcount,
            'urgency': urgency,
            'hiring_manager': hiring_manager
        }

        # Generate with progress
        with click.progressbar(length=100, label='Generating') as bar:
            bar.update(10)

            # Analyze
            analyzer = NLPAnalyzer()
            analysis = analyzer.analyze_multiple_descriptions(jds)
            bar.update(30)

            # Generate all components
            system = generator.generate_complete_system(
                external_job_descriptions=jds,
                company_info=company_info_dict,
                hiring_goals=hiring_goals
            )
            bar.update(80)

            # Save
            files = generator.save_system(system, output_dir=output_dir)
            bar.update(100)

        # Success
        click.echo("\n")
        click.secho("✓ Success!", fg="green", bold=True)
        click.echo("\nGenerated files:")
        for file_type, path in files.items():
            click.echo(f"  • {file_type}: {path}")

        click.echo("\n")
        click.secho("Next steps:", fg="yellow")
        click.echo("1. Review the generated job description")
        click.echo("2. Share hiring plan with your recruiting team")
        click.echo("3. Train interviewers using the rubrics")
        click.echo("4. Track progress using the timeline\n")

    except Exception as e:
        logger.error(f"Interactive mode error: {e}", exc_info=True)
        click.secho(f"\n✗ Error: {e}", fg="red", bold=True)
        click.echo("Please check the logs for more details.\n")


@cli.command()
@click.argument('job_descriptions_file', type=click.Path(exists=True))
@click.argument('company_info_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='output', help='Output directory')
@click.option('--format', '-f', multiple=True, default=['json', 'text'], help='Output formats')
def generate(job_descriptions_file, company_info_file, output, format):
    """Generate hiring system from files."""
    click.secho("\nGenerating hiring system...", fg="green")

    try:
        from ..main import HiringSystemGenerator, load_json_file

        # Load data
        job_descriptions = load_json_file(job_descriptions_file)
        company_info = load_json_file(company_info_file)

        # Generate
        generator = HiringSystemGenerator()
        files = generator.generate_and_save(
            external_job_descriptions=job_descriptions,
            company_info=company_info,
            output_dir=output
        )

        click.secho("\n✓ Success!", fg="green", bold=True)
        click.echo("\nGenerated files:")
        for file_type, path in files.items():
            click.echo(f"  • {file_type}: {path}")
        click.echo()

    except Exception as e:
        click.secho(f"\n✗ Error: {e}", fg="red", bold=True)
        raise click.Abort()


@cli.command()
def stats():
    """Show usage statistics."""
    click.secho("\nUsage Statistics", fg="cyan", bold=True)
    click.secho("="*80, fg="cyan")

    try:
        from ..core.analytics import analytics_manager

        usage_stats = analytics_manager.get_usage_stats(days=30)
        feedback_insights = analytics_manager.get_feedback_insights()

        if not usage_stats.get('enabled', True):
            click.echo("\nAnalytics is disabled.")
            return

        # Usage stats
        click.echo(f"\nPast 30 days:")
        click.echo(f"  Total requests: {usage_stats.get('total_requests', 0)}")
        click.echo(f"  Success rate: {usage_stats.get('success_rate', 0):.1f}%")
        click.echo(f"  Avg processing time: {usage_stats.get('average_processing_time', 0):.2f}s")

        # Feedback insights
        if feedback_insights.get('total_feedback', 0) > 0:
            click.echo(f"\nHiring Outcomes:")
            click.echo(f"  Total feedback: {feedback_insights['total_feedback']}")
            click.echo(f"  Hire rate: {feedback_insights.get('hire_rate', 0):.1f}%")

            if feedback_insights.get('average_time_to_hire_days'):
                click.echo(f"  Avg time to hire: {feedback_insights['average_time_to_hire_days']:.0f} days")

            if feedback_insights.get('average_performance_rating'):
                click.echo(f"  Avg performance: {feedback_insights['average_performance_rating']:.1f}/5.0")

        # Recommendations
        recommendations = analytics_manager.generate_recommendations()
        click.echo("\nRecommendations:")
        for rec in recommendations:
            click.echo(f"  • {rec}")

        click.echo()

    except Exception as e:
        click.secho(f"\n✗ Error: {e}", fg="red")


if __name__ == '__main__':
    cli()
