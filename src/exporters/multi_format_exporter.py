"""
Multi-format exporter for hiring system outputs.
"""

import os
import json
import asyncio
import aiofiles
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime

from ..core.logging_config import get_logger
from ..core.exceptions import ExportError
from ..core.config import config

logger = get_logger(__name__)


class MultiFormatExporter:
    """Exports hiring system outputs in multiple formats."""

    def __init__(self, output_dir: str = 'output'):
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    async def export_all_async(
        self,
        data: Dict[str, Any],
        formats: List[str],
        request_id: str
    ) -> Dict[str, str]:
        """
        Export all data in specified formats asynchronously.

        Args:
            data: Complete hiring system data
            formats: List of formats ('json', 'text', 'markdown', 'pdf')
            request_id: Unique request ID for file naming

        Returns:
            Dict mapping format to file path
        """
        logger.info(f"Exporting to formats: {formats}")

        tasks = []
        for fmt in formats:
            if fmt == 'json':
                tasks.append(self._export_json_async(data, request_id))
            elif fmt == 'text':
                tasks.append(self._export_text_async(data, request_id))
            elif fmt == 'markdown':
                tasks.append(self._export_markdown_async(data, request_id))
            elif fmt == 'pdf':
                tasks.append(self._export_pdf_async(data, request_id))
            else:
                logger.warning(f"Unknown format: {fmt}")

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect successful exports
        output_files = {}
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Export failed for format {formats[i]}: {result}")
            else:
                fmt, path = result
                output_files[fmt] = path

        logger.info(f"Exported {len(output_files)} files successfully")
        return output_files

    async def _export_json_async(self, data: Dict[str, Any], request_id: str) -> tuple:
        """Export as JSON."""
        try:
            filename = f"{request_id}_complete.json"
            filepath = os.path.join(self.output_dir, filename)

            async with aiofiles.open(filepath, 'w') as f:
                await f.write(json.dumps(data, indent=2, default=str))

            logger.info(f"Exported JSON: {filepath}")
            return ('json', filepath)

        except Exception as e:
            logger.error(f"JSON export failed: {e}")
            raise ExportError(f"Failed to export JSON: {e}")

    async def _export_text_async(self, data: Dict[str, Any], request_id: str) -> tuple:
        """Export as formatted text."""
        try:
            # Import formatters
            from ..job_description import JobDescriptionGenerator
            from ..hiring_plan import HiringPlanGenerator
            from ..interview_rubric import InterviewRubricGenerator
            from ..timeline import HiringTimelineGenerator

            jd_gen = JobDescriptionGenerator()
            plan_gen = HiringPlanGenerator()
            rubric_gen = InterviewRubricGenerator()
            timeline_gen = HiringTimelineGenerator()

            # Export each component
            files = {}

            # Job Description
            if 'job_description' in data:
                jd_file = f"{request_id}_job_description.txt"
                jd_path = os.path.join(self.output_dir, jd_file)
                async with aiofiles.open(jd_path, 'w') as f:
                    await f.write(jd_gen.format_as_text(data['job_description']))
                files['job_description'] = jd_path

            # Hiring Plan
            if 'hiring_plan' in data:
                plan_file = f"{request_id}_hiring_plan.txt"
                plan_path = os.path.join(self.output_dir, plan_file)
                async with aiofiles.open(plan_path, 'w') as f:
                    await f.write(plan_gen.format_as_text(data['hiring_plan']))
                files['hiring_plan'] = plan_path

            # Interview Rubric
            if 'interview_rubric' in data:
                rubric_file = f"{request_id}_interview_rubric.txt"
                rubric_path = os.path.join(self.output_dir, rubric_file)
                async with aiofiles.open(rubric_path, 'w') as f:
                    await f.write(rubric_gen.format_as_text(data['interview_rubric']))
                files['interview_rubric'] = rubric_path

            # Timeline
            if 'timeline' in data:
                timeline_file = f"{request_id}_timeline.txt"
                timeline_path = os.path.join(self.output_dir, timeline_file)
                async with aiofiles.open(timeline_path, 'w') as f:
                    await f.write(timeline_gen.format_as_text(data['timeline']))
                files['timeline'] = timeline_path

            logger.info(f"Exported {len(files)} text files")
            return ('text', json.dumps(files))

        except Exception as e:
            logger.error(f"Text export failed: {e}")
            raise ExportError(f"Failed to export text: {e}")

    async def _export_markdown_async(self, data: Dict[str, Any], request_id: str) -> tuple:
        """Export as Markdown."""
        try:
            filename = f"{request_id}_complete.md"
            filepath = os.path.join(self.output_dir, filename)

            markdown_content = self._generate_markdown(data)

            async with aiofiles.open(filepath, 'w') as f:
                await f.write(markdown_content)

            logger.info(f"Exported Markdown: {filepath}")
            return ('markdown', filepath)

        except Exception as e:
            logger.error(f"Markdown export failed: {e}")
            raise ExportError(f"Failed to export markdown: {e}")

    async def _export_pdf_async(self, data: Dict[str, Any], request_id: str) -> tuple:
        """Export as PDF."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch

            filename = f"{request_id}_complete.pdf"
            filepath = os.path.join(self.output_dir, filename)

            # Create PDF
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()

            # Add title
            story.append(Paragraph("Hiring System Package", styles['Title']))
            story.append(Spacer(1, 0.2*inch))

            # Add metadata
            if 'job_description' in data and 'metadata' in data['job_description']:
                meta = data['job_description']['metadata']
                story.append(Paragraph(f"Role: {meta.get('role', 'N/A')}", styles['Normal']))
                story.append(Paragraph(f"Company: {meta.get('company', 'N/A')}", styles['Normal']))
                story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
                story.append(Spacer(1, 0.3*inch))

            # Add sections
            sections = [
                ('Job Description', data.get('job_description')),
                ('Hiring Plan', data.get('hiring_plan')),
                ('Interview Rubric', data.get('interview_rubric')),
                ('Timeline', data.get('timeline'))
            ]

            for section_name, section_data in sections:
                if section_data:
                    story.append(Paragraph(section_name, styles['Heading1']))
                    story.append(Spacer(1, 0.1*inch))
                    # Add simplified content
                    story.append(Paragraph(f"{section_name} details included in JSON export", styles['Normal']))
                    story.append(PageBreak())

            # Build PDF asynchronously
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, doc.build, story)

            logger.info(f"Exported PDF: {filepath}")
            return ('pdf', filepath)

        except ImportError:
            logger.warning("reportlab not installed, skipping PDF export")
            raise ExportError("PDF export requires reportlab package")
        except Exception as e:
            logger.error(f"PDF export failed: {e}")
            raise ExportError(f"Failed to export PDF: {e}")

    def _generate_markdown(self, data: Dict[str, Any]) -> str:
        """Generate markdown content from data."""
        md = "# Hiring System Package\n\n"

        # Add metadata
        if 'job_description' in data and 'metadata' in data['job_description']:
            meta = data['job_description']['metadata']
            md += f"**Role:** {meta.get('role', 'N/A')}  \n"
            md += f"**Company:** {meta.get('company', 'N/A')}  \n"
            md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n\n"

        md += "---\n\n"

        # Job Description
        if 'job_description' in data:
            md += "## Job Description\n\n"
            jd = data['job_description']
            if 'header' in jd:
                md += f"### {jd['header'].get('title', 'N/A')}\n\n"
            if 'overview' in jd:
                md += f"{jd['overview']}\n\n"
            if 'responsibilities' in jd:
                md += "### Responsibilities\n\n"
                for i, resp in enumerate(jd['responsibilities'], 1):
                    md += f"{i}. {resp}\n"
                md += "\n"

        # Hiring Plan
        if 'hiring_plan' in data:
            md += "## Hiring Plan\n\n"
            plan = data['hiring_plan']
            if 'hiring_strategy' in plan and 'overview' in plan['hiring_strategy']:
                md += f"{plan['hiring_strategy']['overview']}\n\n"

        # Interview Rubric
        if 'interview_rubric' in data:
            md += "## Interview Process\n\n"
            rubric = data['interview_rubric']
            if 'interview_stages' in rubric:
                for stage in rubric['interview_stages']:
                    md += f"### {stage.get('stage_name', 'Stage')}\n"
                    md += f"**Duration:** {stage.get('duration', 'N/A')}  \n"
                    md += f"**Interviewer:** {stage.get('interviewer', 'N/A')}  \n\n"

        # Timeline
        if 'timeline' in data:
            md += "## Timeline\n\n"
            timeline = data['timeline']
            if 'milestones' in timeline:
                for milestone in timeline['milestones']:
                    md += f"- **{milestone.get('target_date')}**: {milestone.get('milestone')}\n"

        return md
