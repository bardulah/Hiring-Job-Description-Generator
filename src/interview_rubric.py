"""
Interview Rubric Generator
Creates structured interview rubrics for evaluating Product Manager candidates.
"""

from typing import Dict, List, Any
from datetime import datetime


class InterviewRubricGenerator:
    """Generates comprehensive interview rubrics for PM hiring."""

    def __init__(self):
        self.interview_stages = [
            'screening',
            'product_sense',
            'execution',
            'technical',
            'leadership',
            'behavioral',
            'final'
        ]

    def generate(self, job_description: Dict[str, Any], hiring_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates complete interview rubric package.

        Args:
            job_description: The generated job description
            hiring_config: Configuration for interview process

        Returns:
            Dict containing full interview rubric with all stages
        """
        experience_level = job_description['metadata']['experience_level']

        rubric = {
            'metadata': {
                'generated_date': datetime.now().isoformat(),
                'role': job_description['header']['title'],
                'company': job_description['metadata']['company'],
                'experience_level': experience_level,
                'total_interview_time': self._calculate_total_time(experience_level)
            },
            'interview_process_overview': self._generate_process_overview(experience_level),
            'interview_stages': self._generate_all_stages(experience_level, hiring_config),
            'evaluation_framework': self._generate_evaluation_framework(),
            'scoring_guide': self._generate_scoring_guide(),
            'interviewer_training': self._generate_interviewer_training(),
            'candidate_experience_guidelines': self._generate_candidate_experience_guidelines()
        }

        return rubric

    def _calculate_total_time(self, experience_level: str) -> str:
        """Calculate total interview time."""
        time_map = {
            'Entry-Level': '3-4 hours',
            'Mid-Level': '4-5 hours',
            'Senior': '5-6 hours',
            'Lead/Principal': '6-8 hours'
        }
        return time_map.get(experience_level, '4-5 hours')

    def _generate_process_overview(self, experience_level: str) -> Dict[str, Any]:
        """Generate overview of interview process."""
        stages_count = {
            'Entry-Level': '4-5 stages',
            'Mid-Level': '5-6 stages',
            'Senior': '6-7 stages',
            'Lead/Principal': '7-8 stages'
        }

        return {
            'total_stages': stages_count.get(experience_level, '5-6 stages'),
            'typical_duration': '3-4 weeks from first contact to offer',
            'decision_criteria': 'Must receive strong "hire" recommendation from majority of interviewers, with no strong "no hire" signals',
            'process_principles': [
                'Structured and consistent evaluation across all candidates',
                'Multiple perspectives from cross-functional team members',
                'Balance of different competency areas',
                'Focus on predictive indicators of success',
                'Fair and unbiased assessment',
                'Positive candidate experience throughout'
            ]
        }

    def _generate_all_stages(self, experience_level: str, hiring_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate all interview stages."""
        stages = []

        # Stage 1: Recruiter Screening
        stages.append(self._generate_screening_stage())

        # Stage 2: Product Sense
        stages.append(self._generate_product_sense_stage(experience_level))

        # Stage 3: Execution & Analytics
        stages.append(self._generate_execution_stage(experience_level))

        # Stage 4: Technical Understanding
        if hiring_config.get('include_technical', True):
            stages.append(self._generate_technical_stage(experience_level))

        # Stage 5: Leadership & Collaboration
        if experience_level in ['Senior', 'Lead/Principal']:
            stages.append(self._generate_leadership_stage(experience_level))

        # Stage 6: Behavioral/Cultural Fit
        stages.append(self._generate_behavioral_stage())

        # Stage 7: Final Round with Leadership
        stages.append(self._generate_final_stage(experience_level))

        return stages

    def _generate_screening_stage(self) -> Dict[str, Any]:
        """Generate recruiter screening stage."""
        return {
            'stage_name': 'Recruiter Screening',
            'stage_number': 1,
            'duration': '30 minutes',
            'interviewer': 'Recruiter',
            'format': 'Phone or Video Call',
            'objectives': [
                'Assess basic qualifications and experience',
                'Evaluate communication skills',
                'Gauge interest and motivation',
                'Provide role and company overview',
                'Discuss compensation expectations'
            ],
            'key_questions': [
                'Walk me through your PM experience and key accomplishments',
                'What interests you about this role and our company?',
                'Describe your experience with product roadmap development',
                'Tell me about your experience working with engineering teams',
                'What are your salary expectations?',
                'What is your timeline and are you interviewing elsewhere?'
            ],
            'evaluation_criteria': [
                {
                    'criterion': 'Relevant Experience',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Has required years of PM experience',
                        'Experience aligns with role requirements',
                        'Relevant product or industry background',
                        'Clear career progression'
                    ]
                },
                {
                    'criterion': 'Communication',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Articulates thoughts clearly and concisely',
                        'Answers questions directly',
                        'Professional and engaging manner',
                        'Good listening skills'
                    ]
                },
                {
                    'criterion': 'Motivation',
                    'weight': 'Medium',
                    'signals_to_look_for': [
                        'Genuine interest in role and company',
                        'Has done research on the company',
                        'Career goals align with opportunity',
                        'Enthusiastic and positive attitude'
                    ]
                }
            ],
            'red_flags': [
                'Cannot articulate clear PM experience',
                'Poor communication or unprepared',
                'Compensation expectations significantly misaligned',
                'Negative comments about previous employers',
                'Lacks basic knowledge about the company'
            ],
            'next_steps': 'If positive, advance to product sense interview'
        }

    def _generate_product_sense_stage(self, experience_level: str) -> Dict[str, Any]:
        """Generate product sense interview stage."""
        questions_by_level = {
            'Entry-Level': [
                'Tell me about a product you love. What makes it great?',
                'How would you improve [popular consumer app]?',
                'Design a product for [specific user need]',
                'Walk me through how you would gather user feedback for a new feature',
                'How do you prioritize features when you have limited resources?'
            ],
            'Mid-Level': [
                'Tell me about a product you shipped. How did you decide what to build?',
                'Design a [product type] for [target user]. Walk me through your thinking.',
                'How would you improve our product? (after showing our product)',
                'Estimate the market size for [product category]',
                'How would you determine if a new feature is successful?'
            ],
            'Senior': [
                'Describe your product vision for [our product category]. How would you differentiate from competitors?',
                'Walk me through how you would build a product strategy for entering [new market]',
                'Tell me about a time you had to pivot product direction. How did you decide?',
                'How do you balance short-term wins with long-term product vision?',
                'Design the next generation of [product category]. What would you build and why?'
            ],
            'Lead/Principal': [
                'What is your philosophy on product strategy? How do you develop multi-year product vision?',
                'How would you think about our product portfolio strategy?',
                'Describe a time you had to make a major product bet. How did you decide and what was the outcome?',
                'How do you identify and evaluate new market opportunities?',
                'Walk me through how you would lead a major platform or architecture decision'
            ]
        }

        return {
            'stage_name': 'Product Sense & Strategy',
            'stage_number': 2,
            'duration': '60 minutes',
            'interviewer': 'Senior PM or Product Leader',
            'format': 'Video Call or In-Person',
            'objectives': [
                'Assess product thinking and intuition',
                'Evaluate strategic thinking ability',
                'Test user empathy and customer focus',
                'Assess creativity and problem-solving',
                'Evaluate product taste and judgment'
            ],
            'key_questions': questions_by_level.get(experience_level, questions_by_level['Mid-Level']),
            'evaluation_criteria': [
                {
                    'criterion': 'Product Intuition',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Demonstrates strong understanding of user needs',
                        'Asks clarifying questions about users and context',
                        'Considers multiple perspectives (user, business, technical)',
                        'Shows creativity in solution generation',
                        'Articulates clear product vision'
                    ]
                },
                {
                    'criterion': 'Strategic Thinking',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Thinks about market positioning and competition',
                        'Considers business model and monetization',
                        'Connects product decisions to business outcomes',
                        'Shows ability to prioritize ruthlessly',
                        'Demonstrates long-term thinking'
                    ]
                },
                {
                    'criterion': 'Structured Problem Solving',
                    'weight': 'Medium',
                    'signals_to_look_for': [
                        'Uses frameworks to organize thinking',
                        'Breaks down complex problems systematically',
                        'Makes reasonable assumptions',
                        'Identifies trade-offs clearly',
                        'Reaches conclusions logically'
                    ]
                }
            ],
            'scoring_dimensions': {
                'User Understanding': 'How well does candidate understand user needs and pain points?',
                'Product Vision': 'Can they articulate a compelling product direction?',
                'Strategic Thinking': 'Do they connect product decisions to business strategy?',
                'Creativity': 'Do they generate novel and valuable ideas?',
                'Trade-off Analysis': 'Can they evaluate options and make decisions?'
            },
            'what_great_looks_like': [
                'Asks insightful questions to understand context',
                'Demonstrates deep empathy for users',
                'Proposes creative yet practical solutions',
                'Considers multiple dimensions (user, business, technical)',
                'Articulates clear reasoning for decisions',
                'Shows passion for products and problem-solving'
            ],
            'red_flags': [
                'Jumps to solutions without understanding problem',
                'Focuses only on features without considering outcomes',
                'Cannot explain reasoning behind decisions',
                'Lacks creativity or only proposes obvious ideas',
                'Does not consider business viability'
            ]
        }

    def _generate_execution_stage(self, experience_level: str) -> Dict[str, Any]:
        """Generate execution & analytics interview stage."""
        questions_by_level = {
            'Entry-Level': [
                'Walk me through how you would launch a new feature from kickoff to release',
                'How do you write user stories? Show me an example.',
                'Tell me about a time you had to work with an engineering team on a tight deadline',
                'What metrics would you track for [specific feature]?',
                'How would you handle a situation where engineering says something will take twice as long as you expected?'
            ],
            'Mid-Level': [
                'Tell me about a complex product launch you led. What was your approach?',
                'How do you prioritize items on your product roadmap?',
                'Walk me through your process for defining and tracking success metrics',
                'Describe a time when you had to make trade-offs between speed and quality',
                'How do you work with engineering to estimate and plan sprints?'
            ],
            'Senior': [
                'Describe your approach to building and managing a product roadmap',
                'Tell me about a time you had to coordinate a complex, cross-functional initiative',
                'How do you balance multiple competing priorities from different stakeholders?',
                'Walk me through how you use data to make product decisions',
                'Describe your experience with A/B testing and experimentation'
            ],
            'Lead/Principal': [
                'How do you think about building and scaling product processes?',
                'Describe your approach to portfolio management across multiple products',
                'How do you build a culture of data-driven decision making?',
                'Tell me about a time you had to drive alignment across executive leadership',
                'How do you balance innovation with operational excellence?'
            ]
        }

        return {
            'stage_name': 'Execution & Analytics',
            'stage_number': 3,
            'duration': '60 minutes',
            'interviewer': 'PM or Engineering Manager',
            'format': 'Video Call or In-Person',
            'objectives': [
                'Assess ability to ship products on time',
                'Evaluate data-driven decision making',
                'Test project management and organizational skills',
                'Assess stakeholder management abilities',
                'Evaluate metrics and analytics knowledge'
            ],
            'key_questions': questions_by_level.get(experience_level, questions_by_level['Mid-Level']),
            'evaluation_criteria': [
                {
                    'criterion': 'Execution Excellence',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Track record of shipping products on time',
                        'Strong project management skills',
                        'Ability to break down complex projects',
                        'Experience with agile/scrum methodologies',
                        'Handles ambiguity well'
                    ]
                },
                {
                    'criterion': 'Data & Analytics',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Defines clear success metrics',
                        'Uses data to inform decisions',
                        'Understands basic statistics and A/B testing',
                        'Can interpret data and draw insights',
                        'Balances quantitative and qualitative data'
                    ]
                },
                {
                    'criterion': 'Stakeholder Management',
                    'weight': 'Medium',
                    'signals_to_look_for': [
                        'Communicates effectively with different audiences',
                        'Manages expectations well',
                        'Builds consensus across teams',
                        'Handles disagreements constructively',
                        'Keeps stakeholders informed'
                    ]
                }
            ],
            'scoring_dimensions': {
                'Shipping Track Record': 'Do they have a history of delivering results?',
                'Analytical Thinking': 'Can they define and use metrics effectively?',
                'Process & Organization': 'Are they structured and organized in their approach?',
                'Cross-functional Collaboration': 'Can they work effectively with different teams?',
                'Bias for Action': 'Do they move quickly and decisively?'
            },
            'red_flags': [
                'Cannot provide examples of shipped products',
                'Vague or no understanding of metrics',
                'Poor project management skills',
                'Blames others for failures',
                'Lacks attention to detail'
            ]
        }

    def _generate_technical_stage(self, experience_level: str) -> Dict[str, Any]:
        """Generate technical interview stage."""
        return {
            'stage_name': 'Technical Understanding',
            'stage_number': 4,
            'duration': '45-60 minutes',
            'interviewer': 'Engineering Lead or Technical PM',
            'format': 'Video Call or In-Person',
            'objectives': [
                'Assess technical depth and credibility',
                'Evaluate ability to work with engineers',
                'Test understanding of system design concepts',
                'Assess API and data model understanding',
                'Evaluate technical decision-making'
            ],
            'key_questions': [
                'Explain the technical architecture of a product you\'ve worked on',
                'How do you make technical trade-off decisions?',
                'Design the technical architecture for [product/feature]',
                'How would you explain [technical concept] to a non-technical stakeholder?',
                'Tell me about a time you had a technical disagreement with engineering. How did you handle it?',
                'What questions do you ask engineers when scoping a new feature?',
                'How do you evaluate technical debt vs. new features?'
            ],
            'evaluation_criteria': [
                {
                    'criterion': 'Technical Depth',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Understands technical concepts relevant to role',
                        'Can discuss system architecture intelligently',
                        'Knows enough to make informed decisions',
                        'Asks good technical questions',
                        'Credible with engineering teams'
                    ]
                },
                {
                    'criterion': 'Engineering Collaboration',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Speaks engineers\' language',
                        'Respects technical constraints',
                        'Balances ideal vs. practical solutions',
                        'Builds trust with technical teams',
                        'Values engineering input'
                    ]
                },
                {
                    'criterion': 'Technical Decision Making',
                    'weight': 'Medium',
                    'signals_to_look_for': [
                        'Makes informed technical trade-offs',
                        'Considers scalability and maintainability',
                        'Understands technical debt',
                        'Can evaluate build vs. buy decisions',
                        'Balances speed with quality'
                    ]
                }
            ],
            'note': 'Technical bar should be appropriate for experience level - not expecting engineers, but need to be credible technical partner',
            'red_flags': [
                'No understanding of basic technical concepts',
                'Cannot explain technical aspects of previous work',
                'Dismissive of technical constraints',
                'Poor relationship with engineering teams',
                'Makes unrealistic technical assumptions'
            ]
        }

    def _generate_leadership_stage(self, experience_level: str) -> Dict[str, Any]:
        """Generate leadership interview stage."""
        return {
            'stage_name': 'Leadership & Influence',
            'stage_number': 5,
            'duration': '60 minutes',
            'interviewer': 'Product Leader or Cross-functional Executive',
            'format': 'Video Call or In-Person',
            'objectives': [
                'Assess leadership style and effectiveness',
                'Evaluate ability to influence without authority',
                'Test mentorship and people development skills',
                'Assess strategic influence at senior levels',
                'Evaluate change management abilities'
            ],
            'key_questions': [
                'Tell me about your leadership philosophy',
                'Describe a time you had to influence a decision without having authority',
                'How do you develop and mentor other PMs?',
                'Tell me about a time you led a major organizational change',
                'How do you build alignment across senior leadership?',
                'Describe a situation where you had to make an unpopular decision',
                'How do you create a culture of excellence in product management?',
                'Tell me about a time you had to course-correct a team or project'
            ],
            'evaluation_criteria': [
                {
                    'criterion': 'Leadership Impact',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Clear leadership philosophy and examples',
                        'Drives results through others',
                        'Inspires and motivates teams',
                        'Takes ownership and accountability',
                        'Leads through ambiguity'
                    ]
                },
                {
                    'criterion': 'Influence & Communication',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Influences across all levels',
                        'Builds coalition and consensus',
                        'Excellent executive communication',
                        'Handles conflict constructively',
                        'Persuasive and compelling'
                    ]
                },
                {
                    'criterion': 'People Development',
                    'weight': 'Medium' if experience_level == 'Senior' else 'High',
                    'signals_to_look_for': [
                        'Invests in developing others',
                        'Provides effective feedback',
                        'Creates growth opportunities',
                        'Builds high-performing teams',
                        'Attracts and retains talent'
                    ]
                }
            ],
            'scoring_dimensions': {
                'Leadership Style': 'Do they demonstrate effective leadership?',
                'Influence': 'Can they drive decisions across the organization?',
                'Strategic Impact': 'Do they operate at the right level of strategy?',
                'People Development': 'Do they grow and develop others?',
                'Change Leadership': 'Can they lead through transformation?'
            },
            'red_flags': [
                'No examples of leadership or influence',
                'Weak executive presence',
                'Cannot articulate leadership philosophy',
                'Does not invest in people development',
                'Avoids conflict or difficult conversations'
            ]
        }

    def _generate_behavioral_stage(self) -> Dict[str, Any]:
        """Generate behavioral/culture fit interview stage."""
        return {
            'stage_name': 'Behavioral & Cultural Fit',
            'stage_number': 6,
            'duration': '45 minutes',
            'interviewer': 'Cross-functional Partner (Design, Marketing, Sales, Data)',
            'format': 'Video Call or In-Person',
            'objectives': [
                'Assess alignment with company values',
                'Evaluate collaboration style',
                'Test self-awareness and growth mindset',
                'Assess resilience and adaptability',
                'Evaluate culture add (not just fit)'
            ],
            'key_questions': [
                'Tell me about a time you failed. What did you learn?',
                'Describe a situation where you had conflict with a colleague. How did you resolve it?',
                'Tell me about a time you had to adapt to significant change',
                'Describe your ideal work environment and team culture',
                'What are you passionate about outside of work?',
                'Tell me about a time you gave difficult feedback to someone',
                'Describe a situation where you had to work with someone very different from you',
                'What does diversity and inclusion mean to you in practice?',
                'Tell me about a time you went above and beyond',
                'What are you looking for in your next role and why?'
            ],
            'evaluation_criteria': [
                {
                    'criterion': 'Values Alignment',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Demonstrates company values in examples',
                        'Genuine alignment with mission',
                        'Will thrive in company culture',
                        'Adds to culture positively',
                        'Shares team working style'
                    ]
                },
                {
                    'criterion': 'Growth Mindset',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Learns from failures and mistakes',
                        'Seeks feedback actively',
                        'Self-aware about strengths and weaknesses',
                        'Continuously improving',
                        'Embraces challenges'
                    ]
                },
                {
                    'criterion': 'Collaboration',
                    'weight': 'Medium',
                    'signals_to_look_for': [
                        'Works well with different personalities',
                        'Values diverse perspectives',
                        'Resolves conflicts constructively',
                        'Builds strong relationships',
                        'Team player mentality'
                    ]
                }
            ],
            'scoring_dimensions': {
                'Cultural Alignment': 'Will they thrive in our culture?',
                'Values Match': 'Do they demonstrate our core values?',
                'Growth Mindset': 'Do they learn and adapt?',
                'Collaboration Style': 'Will they work well with the team?',
                'Motivation': 'Are they motivated by the right things?'
            },
            'red_flags': [
                'Blames others consistently',
                'Not self-aware',
                'Poor attitude or negative energy',
                'Misalignment with core values',
                'Red flags in reference checks'
            ]
        }

    def _generate_final_stage(self, experience_level: str) -> Dict[str, Any]:
        """Generate final interview stage."""
        interviewer = 'VP of Product or CTO' if experience_level in ['Entry-Level', 'Mid-Level'] else 'CEO or CPO'

        return {
            'stage_name': 'Final Round - Executive Interview',
            'stage_number': 7,
            'duration': '45-60 minutes',
            'interviewer': interviewer,
            'format': 'Video Call or In-Person',
            'objectives': [
                'Final assessment of candidate fit',
                'Evaluate strategic thinking at highest level',
                'Executive-level sell of role and company',
                'Address any remaining concerns',
                'Assess culture and values match'
            ],
            'key_questions': [
                'Why are you interested in this role and our company?',
                'Where do you see yourself in 3-5 years?',
                'What do you think our biggest product challenges are?',
                'How would you approach your first 90 days?',
                'What questions do you have for me?',
                'What would make you excited to join our company?',
                'Tell me about the most impactful thing you\'ve done in your career',
                'What\'s your take on [industry trend or company strategic direction]?'
            ],
            'evaluation_criteria': [
                {
                    'criterion': 'Strategic Caliber',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Thinks at appropriate strategic level',
                        'Understands market and industry dynamics',
                        'Asks insightful questions',
                        'Demonstrates business acumen',
                        'Has informed perspective on company direction'
                    ]
                },
                {
                    'criterion': 'Motivation & Fit',
                    'weight': 'High',
                    'signals_to_look_for': [
                        'Genuinely excited about company and role',
                        'Clear alignment with mission and values',
                        'Will stay and grow with company',
                        'Positive energy and culture add',
                        'Mutual excitement'
                    ]
                }
            ],
            'interviewer_focus': [
                'Make final hire/no-hire decision',
                'Sell candidate on opportunity and vision',
                'Address any concerns or questions',
                'Assess executive presence and communication',
                'Evaluate long-term potential'
            ],
            'red_flags': [
                'Not well prepared or knowledgeable about company',
                'Lack of strategic thinking',
                'Poor executive communication',
                'Not genuinely interested',
                'Misalignment on vision or values'
            ]
        }

    def _generate_evaluation_framework(self) -> Dict[str, Any]:
        """Generate overall evaluation framework."""
        return {
            'rating_scale': {
                'Strong Hire': 'Exceptional candidate. Top 5% of candidates. Multiple areas of excellence. No significant weaknesses.',
                'Hire': 'Strong candidate. Meets all requirements with some areas of strength. Minor weaknesses that are not deal-breakers.',
                'Maybe': 'Borderline candidate. Mixed signals. Has strengths but also concerns. Needs discussion.',
                'No Hire': 'Does not meet bar. Significant gaps or concerns. Would not be successful in role.'
            },
            'decision_making': {
                'hiring_decision': 'Must have majority "Hire" or "Strong Hire" ratings across all interviewers',
                'veto_power': 'Any "Strong No Hire" from an interviewer triggers team discussion',
                'debrief_process': 'Hold structured debrief with all interviewers before making decision',
                'timeline': 'Make decision within 48 hours of final interview'
            },
            'key_competencies': [
                {
                    'competency': 'Product Sense',
                    'weight': 'Critical',
                    'evaluated_in': 'Product Sense interview'
                },
                {
                    'competency': 'Execution',
                    'weight': 'Critical',
                    'evaluated_in': 'Execution & Analytics interview'
                },
                {
                    'competency': 'Technical Acumen',
                    'weight': 'Important',
                    'evaluated_in': 'Technical Understanding interview'
                },
                {
                    'competency': 'Leadership & Influence',
                    'weight': 'Important (Critical for Senior+)',
                    'evaluated_in': 'Leadership interview'
                },
                {
                    'competency': 'Communication',
                    'weight': 'Important',
                    'evaluated_in': 'All interviews'
                },
                {
                    'competency': 'Cultural Fit',
                    'weight': 'Important',
                    'evaluated_in': 'Behavioral interview'
                },
                {
                    'competency': 'Strategic Thinking',
                    'weight': 'Critical for Senior+',
                    'evaluated_in': 'Product Sense and Final interviews'
                }
            ]
        }

    def _generate_scoring_guide(self) -> Dict[str, Any]:
        """Generate detailed scoring guide."""
        return {
            'how_to_score': [
                'Evaluate each criterion independently',
                'Use specific examples and evidence',
                'Compare to bar for the role level',
                'Consider both what they did and how they did it',
                'Be calibrated with other interviewers'
            ],
            'writing_feedback': [
                'Provide specific examples to support rating',
                'Include both strengths and areas of concern',
                'Note any red flags or exceptional signals',
                'Be objective and professional',
                'Submit feedback within 24 hours'
            ],
            'avoiding_bias': [
                'Use structured questions and rubric',
                'Focus on job-relevant criteria only',
                'Be aware of affinity bias',
                'Don\'t compare to yourself',
                'Evaluate candidate against role requirements, not other candidates'
            ],
            'calibration': [
                'Attend interviewer training and calibration sessions',
                'Review examples of strong vs. weak answers',
                'Discuss borderline cases with team',
                'Maintain consistency across candidates'
            ]
        }

    def _generate_interviewer_training(self) -> Dict[str, Any]:
        """Generate interviewer training guidelines."""
        return {
            'before_interview': [
                'Review candidate resume and application',
                'Read feedback from previous interview rounds',
                'Prepare your questions using the rubric',
                'Set up quiet, professional environment',
                'Allocate full time without interruptions'
            ],
            'during_interview': [
                'Start with warm welcome and role overview',
                'Follow structured question guide',
                'Take detailed notes on responses',
                'Probe for specific examples using STAR method',
                'Leave time for candidate questions (10-15 minutes)',
                'Close by explaining next steps'
            ],
            'after_interview': [
                'Write detailed feedback within 24 hours',
                'Include specific examples for your rating',
                'Submit feedback before seeing others\' input',
                'Be available for debrief discussion',
                'Provide timely response to recruiting team'
            ],
            'star_method': {
                'description': 'Framework for evaluating behavioral responses',
                'situation': 'What was the context?',
                'task': 'What needed to be done?',
                'action': 'What did the candidate specifically do?',
                'result': 'What was the outcome? What was learned?'
            },
            'interview_best_practices': [
                'Be on time and prepared',
                'Create welcoming environment',
                'Listen more than you talk (80/20 rule)',
                'Don\'t lead the witness - ask open-ended questions',
                'Follow up with probing questions',
                'Take detailed notes',
                'Be aware of your biases',
                'Provide positive candidate experience regardless of outcome'
            ]
        }

    def _generate_candidate_experience_guidelines(self) -> Dict[str, Any]:
        """Generate guidelines for positive candidate experience."""
        return {
            'principles': [
                'Treat every candidate with respect and professionalism',
                'Communicate clearly and timely at every stage',
                'Make the process efficient and organized',
                'Provide transparency about process and timeline',
                'Give candidate opportunity to put their best foot forward',
                'Provide closure and feedback when appropriate'
            ],
            'communication_timeline': {
                'application_received': 'Acknowledge within 48 hours',
                'after_screening': 'Decision within 2-3 business days',
                'between_interviews': 'Update within 3 business days',
                'after_final_interview': 'Decision within 48 hours',
                'offer_extended': 'Follow up daily until decision'
            },
            'candidate_preparation': {
                'before_each_interview': [
                    'Send calendar invite with video link or location',
                    'Provide interviewer name, title, and LinkedIn',
                    'Share what to expect in the interview',
                    'Send any prep materials or case studies in advance',
                    'Provide contact for questions'
                ],
                'materials_to_share': [
                    'Overview of interview process and timeline',
                    'Information about the team and role',
                    'Company values and culture deck',
                    'Recent news or blog posts about company'
                ]
            },
            'making_it_positive': [
                'Be warm and welcoming',
                'Show genuine interest in candidate',
                'Sell the role and company',
                'Answer questions thoroughly',
                'Be respectful of their time',
                'Provide clear next steps',
                'Send thank you note after interview'
            ]
        }

    def format_as_text(self, rubric: Dict[str, Any]) -> str:
        """Format interview rubric as readable text."""
        meta = rubric['metadata']

        output = f"""
{'='*80}
INTERVIEW RUBRIC: {meta['role']}
{meta['company']}
{'='*80}

Generated: {meta['generated_date']}
Experience Level: {meta['experience_level']}
Total Interview Time: {meta['total_interview_time']}

PROCESS OVERVIEW
{'='*80}
Total Stages: {rubric['interview_process_overview']['total_stages']}
Duration: {rubric['interview_process_overview']['typical_duration']}

Decision Criteria: {rubric['interview_process_overview']['decision_criteria']}

Process Principles:
"""
        for principle in rubric['interview_process_overview']['process_principles']:
            output += f"• {principle}\n"

        output += "\n" + "="*80 + "\n"
        output += "INTERVIEW STAGES\n"
        output += "="*80 + "\n"

        for stage in rubric['interview_stages']:
            output += f"\n{'='*80}\n"
            output += f"STAGE {stage['stage_number']}: {stage['stage_name'].upper()}\n"
            output += f"{'='*80}\n"
            output += f"Duration: {stage['duration']}\n"
            output += f"Interviewer: {stage['interviewer']}\n"
            output += f"Format: {stage['format']}\n"

            output += "\nObjectives:\n"
            for obj in stage['objectives']:
                output += f"• {obj}\n"

            output += "\nKey Questions:\n"
            for i, question in enumerate(stage['key_questions'], 1):
                output += f"{i}. {question}\n"

            output += "\nEvaluation Criteria:\n"
            for criterion in stage['evaluation_criteria']:
                output += f"\n{criterion['criterion']} (Weight: {criterion['weight']})\n"
                output += "Signals to look for:\n"
                for signal in criterion['signals_to_look_for']:
                    output += f"  • {signal}\n"

            if 'scoring_dimensions' in stage:
                output += "\nScoring Dimensions:\n"
                for dimension, description in stage['scoring_dimensions'].items():
                    output += f"• {dimension}: {description}\n"

            if 'red_flags' in stage:
                output += "\nRed Flags:\n"
                for flag in stage['red_flags']:
                    output += f"• {flag}\n"

        output += "\n" + "="*80 + "\n"
        output += "EVALUATION FRAMEWORK\n"
        output += "="*80 + "\n\n"

        output += "Rating Scale:\n"
        for rating, description in rubric['evaluation_framework']['rating_scale'].items():
            output += f"\n{rating}:\n{description}\n"

        output += "\nKey Competencies:\n"
        for comp in rubric['evaluation_framework']['key_competencies']:
            output += f"• {comp['competency']} ({comp['weight']}) - evaluated in {comp['evaluated_in']}\n"

        return output
