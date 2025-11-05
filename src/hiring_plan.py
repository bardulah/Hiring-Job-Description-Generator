"""
Hiring Plan Generator
Creates comprehensive hiring plans with strategy and execution details.
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta


class HiringPlanGenerator:
    """Generates detailed hiring plans for Product Manager roles."""

    def __init__(self):
        self.default_timeline_weeks = {
            'Entry-Level': 6,
            'Mid-Level': 8,
            'Senior': 10,
            'Lead/Principal': 12
        }

    def generate(self, job_description: Dict[str, Any], hiring_goals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a comprehensive hiring plan.

        Args:
            job_description: The generated job description
            hiring_goals: Hiring goals and constraints

        Returns:
            Dict containing the complete hiring plan
        """
        experience_level = job_description['metadata']['experience_level']

        plan = {
            'metadata': {
                'generated_date': datetime.now().isoformat(),
                'role': job_description['header']['title'],
                'company': job_description['metadata']['company'],
                'target_headcount': hiring_goals.get('target_headcount', 1),
                'urgency': hiring_goals.get('urgency', 'medium')
            },
            'hiring_strategy': self._generate_strategy(experience_level, hiring_goals),
            'sourcing_plan': self._generate_sourcing_plan(experience_level, hiring_goals),
            'budget': self._generate_budget(job_description, hiring_goals),
            'team_structure': self._generate_team_structure(hiring_goals),
            'success_metrics': self._generate_success_metrics(hiring_goals),
            'risks_and_mitigations': self._generate_risks_and_mitigations(experience_level)
        }

        return plan

    def _generate_strategy(self, experience_level: str, hiring_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Generate hiring strategy."""
        target_headcount = hiring_goals.get('target_headcount', 1)
        urgency = hiring_goals.get('urgency', 'medium')

        strategy = {
            'overview': f"""
This hiring plan outlines the strategy for hiring {target_headcount} {experience_level} Product Manager(s).
The plan focuses on attracting top talent through a multi-channel sourcing approach, rigorous
evaluation process, and competitive compensation packages.
""".strip(),
            'key_priorities': [],
            'target_candidate_profile': self._generate_target_profile(experience_level),
            'competitive_positioning': self._generate_competitive_positioning(experience_level, hiring_goals),
            'diversity_and_inclusion': {
                'goals': [
                    'Build diverse interview panel representing different backgrounds',
                    'Source from diverse talent pools and communities',
                    'Remove bias from job descriptions and screening process',
                    'Track diversity metrics throughout hiring funnel',
                    'Partner with organizations supporting underrepresented groups in tech'
                ],
                'targets': 'Aim for 50% diverse candidate slate at each interview stage'
            }
        }

        # Set priorities based on urgency
        if urgency == 'high':
            strategy['key_priorities'] = [
                'Fast-track interview process (target: 3-4 weeks from application to offer)',
                'Leverage employee referrals and recruiter networks',
                'Consider contract-to-hire arrangements for speed',
                'Expedite decision-making with streamlined approval process'
            ]
        elif urgency == 'low':
            strategy['key_priorities'] = [
                'Build robust pipeline for future needs',
                'Focus on cultural fit and long-term potential',
                'Engage passive candidates through networking',
                'Invest in employer branding and content marketing'
            ]
        else:
            strategy['key_priorities'] = [
                'Balance speed with quality of hire',
                'Build diverse candidate pipeline',
                'Maintain positive candidate experience',
                'Leverage multiple sourcing channels'
            ]

        return strategy

    def _generate_target_profile(self, experience_level: str) -> Dict[str, List[str]]:
        """Generate ideal candidate profile."""
        profiles = {
            'Entry-Level': {
                'background': [
                    'Recent graduates with product management internships',
                    'Associate product managers looking to step up',
                    'Professionals from related fields (consulting, analytics, engineering) transitioning to PM',
                    'Candidates with strong analytical and communication skills'
                ],
                'experience': [
                    '0-2 years in product management or related role',
                    'Demonstrated passion for products and technology',
                    'Experience with data analysis and user research'
                ],
                'traits': [
                    'Quick learner with growth mindset',
                    'Strong problem-solving abilities',
                    'Excellent communication skills',
                    'User-centric thinking',
                    'Collaborative team player'
                ]
            },
            'Mid-Level': {
                'background': [
                    'Product managers with proven track record of successful launches',
                    'Candidates from similar industry or product domain',
                    'Experience with both B2B and/or B2C products',
                    'Strong technical understanding and ability to work with engineers'
                ],
                'experience': [
                    '3-5 years in product management',
                    'Led multiple product launches or major features',
                    'Experience with agile development processes',
                    'Data-driven decision making experience'
                ],
                'traits': [
                    'Strategic thinker with execution skills',
                    'Strong leadership abilities',
                    'Excellent stakeholder management',
                    'Customer-obsessed',
                    'Results-oriented'
                ]
            },
            'Senior': {
                'background': [
                    'Senior PMs from top tech companies or successful startups',
                    'Candidates with experience scaling products',
                    'Track record of driving significant business impact',
                    'Experience mentoring junior PMs'
                ],
                'experience': [
                    '6-9 years in product management',
                    'Led product strategy for major product lines',
                    'Experience with P&L ownership',
                    'Built and managed product teams'
                ],
                'traits': [
                    'Visionary leader',
                    'Exceptional strategic thinking',
                    'Strong executive communication',
                    'Proven people development skills',
                    'Bias for action'
                ]
            },
            'Lead/Principal': {
                'background': [
                    'Senior or Lead PMs from industry-leading companies',
                    'Founders or co-founders with product experience',
                    'Executives with deep product expertise',
                    'Recognized thought leaders in product management'
                ],
                'experience': [
                    '10+ years in product management',
                    'Led product organizations or major business units',
                    'Experience with company-wide strategic initiatives',
                    'Built and scaled product teams and processes'
                ],
                'traits': [
                    'Strategic visionary',
                    'Strong executive presence',
                    'Proven organizational leadership',
                    'Change agent and influencer',
                    'Industry expertise'
                ]
            }
        }

        return profiles.get(experience_level, profiles['Mid-Level'])

    def _generate_competitive_positioning(self, experience_level: str,
                                         hiring_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Generate competitive positioning strategy."""
        return {
            'value_proposition': [
                'Opportunity to make significant impact on product direction',
                'Work with cutting-edge technology and talented team',
                'Strong learning and growth opportunities',
                'Competitive compensation and equity package',
                'Flexible work environment and strong culture'
            ],
            'differentiators': hiring_goals.get('differentiators', [
                'Fast-growing company with strong market position',
                'Innovative product addressing real customer pain points',
                'Collaborative and inclusive culture',
                'Investment in employee development'
            ]),
            'competing_with': self._get_likely_competitors(experience_level)
        }

    def _get_likely_competitors(self, experience_level: str) -> List[str]:
        """Identify likely competing employers."""
        if experience_level in ['Senior', 'Lead/Principal']:
            return [
                'Large tech companies (FAANG)',
                'Well-funded startups in similar space',
                'Consulting firms',
                'Other fast-growing tech companies'
            ]
        else:
            return [
                'Tech companies of similar size',
                'Startups in similar stage',
                'Consulting and strategy firms',
                'Other product-focused companies'
            ]

    def _generate_sourcing_plan(self, experience_level: str, hiring_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Generate candidate sourcing plan."""
        return {
            'channels': [
                {
                    'name': 'Employee Referrals',
                    'priority': 'High',
                    'expected_percentage': '30%',
                    'activities': [
                        'Launch internal referral campaign with incentives',
                        'Brief team on ideal candidate profile',
                        'Provide easy referral submission process',
                        'Track and acknowledge all referrals within 48 hours'
                    ]
                },
                {
                    'name': 'Direct Sourcing/Outreach',
                    'priority': 'High',
                    'expected_percentage': '25%',
                    'activities': [
                        'LinkedIn Recruiter searches with targeted criteria',
                        'Engage passive candidates with personalized messages',
                        'Leverage GitHub, ProductHunt, and Medium for active PMs',
                        'Attend industry events and conferences'
                    ]
                },
                {
                    'name': 'Job Boards',
                    'priority': 'Medium',
                    'expected_percentage': '20%',
                    'activities': [
                        'Post on LinkedIn, Indeed, Glassdoor',
                        'Use specialized boards: AngelList, ProductHQ, MindTheProduct',
                        'Optimize job postings for SEO and discoverability',
                        'Monitor and respond to applications within 24 hours'
                    ]
                },
                {
                    'name': 'Recruiting Agencies',
                    'priority': 'Medium' if hiring_goals.get('urgency') == 'high' else 'Low',
                    'expected_percentage': '15%',
                    'activities': [
                        'Partner with 2-3 specialized PM recruiting firms',
                        'Provide detailed candidate profile and expectations',
                        'Set clear SLAs for candidate submission and feedback',
                        'Review agency performance monthly'
                    ]
                },
                {
                    'name': 'University Recruiting' if experience_level == 'Entry-Level' else 'PM Communities',
                    'priority': 'Medium',
                    'expected_percentage': '10%',
                    'activities': [
                        'Engage with PM Slack groups and forums',
                        'Sponsor/speak at PM meetups and events',
                        'Create valuable content to attract candidates',
                        'Build relationships with PM influencers'
                    ] if experience_level != 'Entry-Level' else [
                        'Target top MBA and CS programs',
                        'Attend career fairs and info sessions',
                        'Offer PM internship conversion opportunities',
                        'Build university brand presence'
                    ]
                }
            ],
            'pipeline_goals': self._generate_pipeline_goals(hiring_goals.get('target_headcount', 1)),
            'timeline': f"{self.default_timeline_weeks.get(experience_level, 8)} weeks"
        }

    def _generate_pipeline_goals(self, target_headcount: int) -> Dict[str, int]:
        """Generate candidate pipeline goals based on typical conversion rates."""
        return {
            'sourced_candidates': target_headcount * 100,
            'screening_calls': target_headcount * 40,
            'first_round_interviews': target_headcount * 20,
            'final_round_interviews': target_headcount * 8,
            'offers_extended': target_headcount * 2,
            'target_hires': target_headcount
        }

    def _generate_budget(self, job_description: Dict[str, Any], hiring_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Generate hiring budget."""
        target_headcount = hiring_goals.get('target_headcount', 1)

        return {
            'recruiting_costs': {
                'job_board_postings': f'${2000 * target_headcount:,}',
                'recruiting_agency_fees': f'${15000 * target_headcount:,} (if used, 20-25% of first year salary)',
                'employee_referral_bonuses': f'${2500 * target_headcount:,}',
                'recruiting_software': '$500/month',
                'events_and_networking': f'${1000 * target_headcount:,}',
                'total_recruiting': f'${(20000 * target_headcount + 500):,}'
            },
            'compensation_budget': {
                'annual_salary_range': job_description['compensation']['salary_range'],
                'equity_value': job_description['compensation']['equity'],
                'signing_bonus': 'Up to 15% of base salary',
                'relocation': 'Up to $10,000 if applicable'
            },
            'onboarding_costs': {
                'equipment_and_setup': f'${3000 * target_headcount:,}',
                'training_and_development': f'${2000 * target_headcount:,}',
                'total_onboarding': f'${5000 * target_headcount:,}'
            }
        }

    def _generate_team_structure(self, hiring_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Generate hiring team structure and responsibilities."""
        return {
            'hiring_manager': {
                'role': hiring_goals.get('hiring_manager', 'VP of Product / Head of Product'),
                'responsibilities': [
                    'Define role requirements and ideal candidate profile',
                    'Review all candidates before final rounds',
                    'Conduct final interviews',
                    'Make hiring decisions and extend offers',
                    'Participate in sourcing and outreach for senior roles'
                ]
            },
            'recruiter': {
                'role': 'Internal Recruiter or Agency Partner',
                'responsibilities': [
                    'Manage sourcing and candidate pipeline',
                    'Conduct initial screening calls',
                    'Coordinate interview scheduling',
                    'Communicate with candidates throughout process',
                    'Track metrics and provide weekly updates'
                ]
            },
            'interview_panel': {
                'composition': [
                    '1-2 Product Managers (peer level)',
                    '1-2 Engineering Leads/Managers',
                    '1 Designer or UX Lead',
                    '1 Cross-functional partner (Marketing, Sales, or Data)',
                    '1 Executive stakeholder'
                ],
                'responsibilities': [
                    'Conduct structured interviews using rubrics',
                    'Provide timely feedback within 24 hours',
                    'Participate in debrief sessions',
                    'Help with candidate engagement and selling'
                ]
            },
            'recruiting_coordinator': {
                'role': 'Recruiting Coordinator or Executive Assistant',
                'responsibilities': [
                    'Schedule all interviews',
                    'Send preparation materials to candidates',
                    'Coordinate logistics for on-site/virtual interviews',
                    'Collect interview feedback',
                    'Support offer process'
                ]
            }
        }

    def _generate_success_metrics(self, hiring_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Generate success metrics for hiring plan."""
        return {
            'efficiency_metrics': {
                'time_to_hire': 'Target: <60 days from job posting to offer acceptance',
                'time_to_fill': 'Target: <90 days from requisition approval to start date',
                'cost_per_hire': 'Target: <$20,000 per hire',
                'offer_acceptance_rate': 'Target: >80%'
            },
            'quality_metrics': {
                'quality_of_hire': 'Measured by 90-day performance review score (target: 4.0+/5.0)',
                'hiring_manager_satisfaction': 'Target: 4.5+/5.0 satisfaction score',
                'new_hire_retention': 'Target: >90% retention at 12 months',
                'cultural_fit': 'Measured in performance reviews and 360 feedback'
            },
            'pipeline_metrics': {
                'candidate_pipeline_health': 'Maintain 3:1 ratio of candidates to open roles',
                'source_effectiveness': 'Track conversion rate by source channel',
                'diversity_metrics': 'Track diversity at each stage of funnel',
                'candidate_experience': 'Target: 4.0+/5.0 candidate satisfaction score'
            },
            'reporting_cadence': {
                'weekly': 'Pipeline status, candidate flow, upcoming interviews',
                'bi_weekly': 'Detailed funnel metrics and source analysis',
                'monthly': 'Full metrics dashboard and strategy review'
            }
        }

    def _generate_risks_and_mitigations(self, experience_level: str) -> List[Dict[str, str]]:
        """Generate risk analysis and mitigation strategies."""
        common_risks = [
            {
                'risk': 'Competitive market for PM talent',
                'impact': 'High',
                'mitigation': 'Develop strong employer brand, competitive compensation, fast decision-making process, and compelling growth opportunities'
            },
            {
                'risk': 'Extended time to hire leads to losing candidates',
                'impact': 'High',
                'mitigation': 'Streamline interview process, set clear timelines, maintain regular candidate communication, expedite internal approvals'
            },
            {
                'risk': 'Insufficient candidate pipeline',
                'impact': 'High',
                'mitigation': 'Multi-channel sourcing approach, build talent community, start sourcing before opening is approved, leverage employee networks'
            },
            {
                'risk': 'Poor candidate experience damages employer brand',
                'impact': 'Medium',
                'mitigation': 'Timely communication, respectful interview process, gather and act on candidate feedback, personalized interactions'
            },
            {
                'risk': 'Interview panel availability constraints',
                'impact': 'Medium',
                'mitigation': 'Block recurring interview time slots, train backup interviewers, use asynchronous assessment tools where appropriate'
            },
            {
                'risk': 'Mis-hire due to rushed process',
                'impact': 'High',
                'mitigation': 'Maintain interview standards regardless of urgency, use structured interviews and rubrics, involve multiple interviewers'
            },
            {
                'risk': 'Offer rejections due to compensation',
                'impact': 'Medium',
                'mitigation': 'Research market rates, understand candidate expectations early, have flexibility in comp structure, highlight total comp package'
            }
        ]

        if experience_level in ['Senior', 'Lead/Principal']:
            common_risks.append({
                'risk': 'Limited pool of qualified senior candidates',
                'impact': 'High',
                'mitigation': 'Start outreach to passive candidates early, consider candidates from adjacent industries, build relationships over time'
            })

        return common_risks

    def format_as_text(self, hiring_plan: Dict[str, Any]) -> str:
        """Format hiring plan as readable text."""
        meta = hiring_plan['metadata']

        output = f"""
{'='*80}
HIRING PLAN: {meta['role']}
{meta['company']}
{'='*80}

Generated: {meta['generated_date']}
Target Headcount: {meta['target_headcount']}
Urgency: {meta['urgency'].upper()}

HIRING STRATEGY
{'='*80}
{hiring_plan['hiring_strategy']['overview']}

Key Priorities:
"""
        for priority in hiring_plan['hiring_strategy']['key_priorities']:
            output += f"• {priority}\n"

        output += "\nTarget Candidate Profile:\n"
        profile = hiring_plan['hiring_strategy']['target_candidate_profile']
        for category, items in profile.items():
            output += f"\n{category.title()}:\n"
            for item in items:
                output += f"  • {item}\n"

        output += "\nSOURCING PLAN\n"
        output += "="*80 + "\n"
        for channel in hiring_plan['sourcing_plan']['channels']:
            output += f"\n{channel['name']} (Priority: {channel['priority']})\n"
            output += f"Expected: {channel['expected_percentage']} of hires\n"
            for activity in channel['activities']:
                output += f"  • {activity}\n"

        output += f"\nPipeline Goals:\n"
        for stage, count in hiring_plan['sourcing_plan']['pipeline_goals'].items():
            output += f"  • {stage.replace('_', ' ').title()}: {count}\n"

        output += "\nBUDGET\n"
        output += "="*80 + "\n"
        for category, items in hiring_plan['budget'].items():
            output += f"\n{category.replace('_', ' ').title()}:\n"
            if isinstance(items, dict):
                for item, value in items.items():
                    output += f"  • {item.replace('_', ' ').title()}: {value}\n"

        output += "\nSUCCESS METRICS\n"
        output += "="*80 + "\n"
        for category, metrics in hiring_plan['success_metrics'].items():
            if category != 'reporting_cadence':
                output += f"\n{category.replace('_', ' ').title()}:\n"
                if isinstance(metrics, dict):
                    for metric, target in metrics.items():
                        output += f"  • {metric.replace('_', ' ').title()}: {target}\n"

        output += "\nRISKS AND MITIGATIONS\n"
        output += "="*80 + "\n"
        for risk_item in hiring_plan['risks_and_mitigations']:
            output += f"\nRisk: {risk_item['risk']}\n"
            output += f"Impact: {risk_item['impact']}\n"
            output += f"Mitigation: {risk_item['mitigation']}\n"

        return output
