"""
Job Description Generator
Creates comprehensive job descriptions based on analyzed data.
"""

from typing import Dict, List, Any
from datetime import datetime


class JobDescriptionGenerator:
    """Generates detailed job descriptions for Product Manager roles."""

    def __init__(self):
        self.templates = {
            'Senior': self._get_senior_template(),
            'Mid-Level': self._get_mid_level_template(),
            'Entry-Level': self._get_entry_level_template(),
            'Lead/Principal': self._get_lead_template()
        }

    def generate(self, analysis: Dict[str, Any], company_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a comprehensive job description.

        Args:
            analysis: Analyzed data from multiple job descriptions
            company_info: Company-specific information

        Returns:
            Dict containing the complete job description
        """
        experience_level = company_info.get('experience_level', 'Mid-Level')
        template = self.templates.get(experience_level, self._get_mid_level_template())

        job_description = {
            'metadata': {
                'generated_date': datetime.now().isoformat(),
                'version': '1.0',
                'company': company_info.get('company_name', 'Your Company'),
                'department': company_info.get('department', 'Product'),
                'experience_level': experience_level
            },
            'header': self._generate_header(company_info, experience_level),
            'overview': self._generate_overview(company_info, analysis),
            'responsibilities': self._generate_responsibilities(analysis, template, company_info),
            'qualifications': self._generate_qualifications(analysis, template, company_info),
            'skills': self._generate_skills(analysis, company_info),
            'compensation': self._generate_compensation(company_info),
            'benefits': self._generate_benefits(company_info),
            'application_process': self._generate_application_process(company_info)
        }

        return job_description

    def _generate_header(self, company_info: Dict[str, Any], experience_level: str) -> Dict[str, str]:
        """Generate job header information."""
        return {
            'title': f"{experience_level} Product Manager",
            'company': company_info.get('company_name', 'Your Company'),
            'location': company_info.get('location', 'Remote'),
            'type': company_info.get('employment_type', 'Full-Time'),
            'department': company_info.get('department', 'Product')
        }

    def _generate_overview(self, company_info: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Generate company and role overview."""
        company_name = company_info.get('company_name', 'Your Company')
        company_mission = company_info.get('mission', 'create innovative solutions')
        product_focus = company_info.get('product_focus', 'cutting-edge products')

        overview = f"""
About {company_name}:
{company_info.get('about', f'{company_name} is a leading company focused on {company_mission}.')}

Role Overview:
We are seeking a talented Product Manager to join our dynamic team. In this role, you will be responsible for driving product strategy, working with cross-functional teams, and delivering exceptional products that delight our customers. You will own the product roadmap and work closely with engineering, design, marketing, and sales to bring innovative solutions to market.

This role is perfect for someone who is passionate about {product_focus} and wants to make a significant impact on our product direction and company growth.
"""
        return overview.strip()

    def _generate_responsibilities(self, analysis: Dict[str, Any], template: List[str],
                                   company_info: Dict[str, Any]) -> List[str]:
        """Generate list of responsibilities."""
        responsibilities = template.copy()

        # Add company-specific responsibilities
        if 'custom_responsibilities' in company_info:
            responsibilities.extend(company_info['custom_responsibilities'])

        # Customize based on analysis
        common_responsibilities = analysis.get('common_responsibilities', {})
        if common_responsibilities:
            top_responsibilities = list(common_responsibilities.keys())[:3]
            for resp in top_responsibilities:
                if resp not in ' '.join(responsibilities):
                    responsibilities.append(resp)

        return responsibilities

    def _generate_qualifications(self, analysis: Dict[str, Any], template: List[str],
                                company_info: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate required and preferred qualifications."""
        qualifications = {
            'required': template.copy(),
            'preferred': []
        }

        # Add company-specific qualifications
        if 'required_qualifications' in company_info:
            qualifications['required'].extend(company_info['required_qualifications'])

        if 'preferred_qualifications' in company_info:
            qualifications['preferred'].extend(company_info['preferred_qualifications'])

        # Add common qualifications from analysis
        common_quals = analysis.get('common_qualifications', {})
        if common_quals:
            top_quals = list(common_quals.keys())[:5]
            qualifications['preferred'].extend(top_quals)

        return qualifications

    def _generate_skills(self, analysis: Dict[str, Any], company_info: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate required and nice-to-have skills."""
        common_skills = analysis.get('common_skills', {})
        top_skills = list(common_skills.keys())[:15] if common_skills else []

        skills = {
            'technical': [
                'Data analysis and metrics-driven decision making',
                'Product roadmap development',
                'Agile/Scrum methodologies',
                'SQL or similar data query languages',
                'A/B testing and experimentation',
                'Analytics tools (e.g., Google Analytics, Mixpanel, Amplitude)'
            ],
            'business': [
                'Strategic thinking and product vision',
                'Market and competitive analysis',
                'Go-to-market strategy',
                'Business case development',
                'Pricing and monetization',
                'Financial modeling and P&L management'
            ],
            'soft_skills': [
                'Excellent communication and presentation skills',
                'Strong stakeholder management',
                'Leadership and influence without authority',
                'Problem-solving and critical thinking',
                'User empathy and customer focus',
                'Cross-functional collaboration'
            ]
        }

        # Add company-specific skills
        if 'required_skills' in company_info:
            skills['technical'].extend(company_info['required_skills'])

        # Add skills from analysis
        for skill in top_skills:
            added = False
            for category in skills.values():
                if skill in ' '.join(category).lower():
                    added = True
                    break
            if not added:
                skills['technical'].append(skill.title())

        return skills

    def _generate_compensation(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate compensation information."""
        return {
            'salary_range': company_info.get('salary_range', 'Competitive, based on experience'),
            'equity': company_info.get('equity', 'Stock options available'),
            'bonus': company_info.get('bonus', 'Performance-based bonus eligible')
        }

    def _generate_benefits(self, company_info: Dict[str, Any]) -> List[str]:
        """Generate benefits list."""
        default_benefits = [
            'Comprehensive health, dental, and vision insurance',
            'Flexible PTO and paid holidays',
            '401(k) with company match',
            'Professional development budget',
            'Remote work flexibility',
            'Home office stipend',
            'Parental leave',
            'Mental health and wellness programs',
            'Team events and company offsites'
        ]

        custom_benefits = company_info.get('benefits', [])
        return custom_benefits if custom_benefits else default_benefits

    def _generate_application_process(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate application process information."""
        return {
            'how_to_apply': company_info.get('application_instructions',
                'Please submit your resume and a cover letter explaining why you\'re interested in this role.'),
            'equal_opportunity': 'We are an equal opportunity employer and value diversity at our company. We do not discriminate on the basis of race, religion, color, national origin, gender, sexual orientation, age, marital status, veteran status, or disability status.',
            'accommodations': 'If you need accommodations during the application process, please let us know.'
        }

    def _get_senior_template(self) -> List[str]:
        """Template for Senior PM roles."""
        return [
            'Lead product strategy and vision for key product areas',
            'Own and manage product roadmap, prioritizing features based on business impact',
            'Conduct user research and market analysis to identify opportunities',
            'Work closely with engineering teams to define technical requirements and specifications',
            'Drive go-to-market strategy in collaboration with marketing and sales teams',
            'Define and track key product metrics and success criteria',
            'Present product updates and strategic recommendations to executive leadership',
            'Mentor junior product managers and contribute to PM practice development',
            'Lead cross-functional initiatives and drive alignment across teams'
        ]

    def _get_mid_level_template(self) -> List[str]:
        """Template for Mid-Level PM roles."""
        return [
            'Manage product roadmap and feature prioritization for your product area',
            'Gather and analyze user feedback to inform product decisions',
            'Write detailed product requirements and user stories',
            'Collaborate with design and engineering to deliver high-quality products',
            'Conduct competitive analysis and market research',
            'Define success metrics and analyze product performance data',
            'Support go-to-market activities and product launches',
            'Communicate product updates to stakeholders',
            'Contribute to product strategy discussions'
        ]

    def _get_entry_level_template(self) -> List[str]:
        """Template for Entry-Level PM roles."""
        return [
            'Assist in product roadmap planning and feature prioritization',
            'Conduct user research and gather customer feedback',
            'Write user stories and maintain product backlog',
            'Collaborate with engineering and design teams on feature development',
            'Track and report on product metrics and KPIs',
            'Support product launches and go-to-market activities',
            'Participate in user testing and feedback sessions',
            'Contribute to product documentation and specifications',
            'Learn and apply product management best practices'
        ]

    def _get_lead_template(self) -> List[str]:
        """Template for Lead/Principal PM roles."""
        return [
            'Define and drive overall product vision and strategy across multiple product lines',
            'Lead and mentor a team of product managers',
            'Partner with executive leadership on long-term product planning',
            'Drive major cross-functional initiatives and organizational change',
            'Establish product management processes and best practices',
            'Own P&L responsibility and business outcomes for product portfolio',
            'Represent product organization in company-wide strategic discussions',
            'Build relationships with key customers and partners',
            'Evangelize product vision internally and externally',
            'Make data-driven decisions on major product investments and trade-offs'
        ]

    def format_as_text(self, job_description: Dict[str, Any]) -> str:
        """Format job description as readable text."""
        header = job_description['header']
        text_output = f"""
{'='*80}
{header['title'].upper()}
{header['company']}
{'='*80}

Location: {header['location']}
Type: {header['type']}
Department: {header['department']}

{job_description['overview']}

RESPONSIBILITIES:
"""
        for i, resp in enumerate(job_description['responsibilities'], 1):
            text_output += f"{i}. {resp}\n"

        text_output += "\nREQUIRED QUALIFICATIONS:\n"
        for i, qual in enumerate(job_description['qualifications']['required'], 1):
            text_output += f"{i}. {qual}\n"

        if job_description['qualifications']['preferred']:
            text_output += "\nPREFERRED QUALIFICATIONS:\n"
            for i, qual in enumerate(job_description['qualifications']['preferred'], 1):
                text_output += f"{i}. {qual}\n"

        text_output += "\nSKILLS:\n"
        for category, skills in job_description['skills'].items():
            text_output += f"\n{category.replace('_', ' ').title()}:\n"
            for skill in skills:
                text_output += f"• {skill}\n"

        text_output += f"\nCOMPENSATION:\n"
        comp = job_description['compensation']
        text_output += f"• Salary: {comp['salary_range']}\n"
        text_output += f"• Equity: {comp['equity']}\n"
        text_output += f"• Bonus: {comp['bonus']}\n"

        text_output += "\nBENEFITS:\n"
        for benefit in job_description['benefits']:
            text_output += f"• {benefit}\n"

        text_output += f"\nHOW TO APPLY:\n{job_description['application_process']['how_to_apply']}\n"
        text_output += f"\n{job_description['application_process']['equal_opportunity']}\n"

        return text_output
