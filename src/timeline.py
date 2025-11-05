"""
Hiring Timeline Generator
Creates detailed, week-by-week hiring timelines with milestones and dependencies.
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
import json


class HiringTimelineGenerator:
    """Generates detailed hiring timelines with milestones and activities."""

    def __init__(self):
        self.timeline_duration_weeks = {
            'Entry-Level': 6,
            'Mid-Level': 8,
            'Senior': 10,
            'Lead/Principal': 12
        }

    def generate(self, job_description: Dict[str, Any],
                 hiring_plan: Dict[str, Any],
                 start_date: str = None) -> Dict[str, Any]:
        """
        Generates comprehensive hiring timeline.

        Args:
            job_description: The generated job description
            hiring_plan: The generated hiring plan
            start_date: Start date in YYYY-MM-DD format (defaults to today)

        Returns:
            Dict containing detailed timeline with milestones
        """
        experience_level = job_description['metadata']['experience_level']
        duration_weeks = self.timeline_duration_weeks.get(experience_level, 8)

        if start_date:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start_dt = datetime.now()

        timeline = {
            'metadata': {
                'generated_date': datetime.now().isoformat(),
                'role': job_description['header']['title'],
                'company': job_description['metadata']['company'],
                'start_date': start_dt.strftime('%Y-%m-%d'),
                'estimated_duration_weeks': duration_weeks,
                'target_hire_date': (start_dt + timedelta(weeks=duration_weeks)).strftime('%Y-%m-%d')
            },
            'phases': self._generate_phases(start_dt, duration_weeks, experience_level, hiring_plan),
            'milestones': self._generate_milestones(start_dt, duration_weeks),
            'weekly_breakdown': self._generate_weekly_breakdown(start_dt, duration_weeks, experience_level),
            'dependencies': self._generate_dependencies(),
            'resource_allocation': self._generate_resource_allocation(),
            'risk_timeline': self._generate_risk_timeline(),
            'communication_plan': self._generate_communication_plan()
        }

        return timeline

    def _generate_phases(self, start_date: datetime, duration_weeks: int,
                         experience_level: str, hiring_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate hiring process phases."""
        phases = []

        # Phase 1: Preparation
        prep_start = start_date
        prep_end = start_date + timedelta(weeks=1)
        phases.append({
            'phase_number': 1,
            'phase_name': 'Preparation & Setup',
            'start_date': prep_start.strftime('%Y-%m-%d'),
            'end_date': prep_end.strftime('%Y-%m-%d'),
            'duration': '1 week',
            'objectives': [
                'Finalize job description and requirements',
                'Set up interview process and rubrics',
                'Brief hiring team and interviewers',
                'Set up job postings and sourcing channels',
                'Prepare recruiting materials'
            ],
            'deliverables': [
                'Approved job description',
                'Interview rubrics and questions',
                'Trained interview panel',
                'Active job postings',
                'Sourcing campaign launched'
            ],
            'success_criteria': 'Ready to begin active sourcing and screening'
        })

        # Phase 2: Sourcing & Screening
        sourcing_start = prep_end
        sourcing_duration = 2 if experience_level in ['Entry-Level', 'Mid-Level'] else 3
        sourcing_end = sourcing_start + timedelta(weeks=sourcing_duration)
        phases.append({
            'phase_number': 2,
            'phase_name': 'Sourcing & Initial Screening',
            'start_date': sourcing_start.strftime('%Y-%m-%d'),
            'end_date': sourcing_end.strftime('%Y-%m-%d'),
            'duration': f'{sourcing_duration} weeks',
            'objectives': [
                'Build strong candidate pipeline',
                'Conduct recruiter screening calls',
                'Identify top candidates for interviews',
                'Engage passive candidates',
                'Maintain candidate pipeline'
            ],
            'deliverables': [
                f'Sourced {hiring_plan["sourcing_plan"]["pipeline_goals"]["sourced_candidates"]} candidates',
                f'Completed {hiring_plan["sourcing_plan"]["pipeline_goals"]["screening_calls"]} screening calls',
                f'Advanced {hiring_plan["sourcing_plan"]["pipeline_goals"]["first_round_interviews"]} candidates to first round',
                'Pipeline dashboard updated weekly'
            ],
            'success_criteria': 'Strong pipeline of qualified candidates ready for interviews'
        })

        # Phase 3: First Round Interviews
        first_round_start = sourcing_start + timedelta(weeks=1)  # Overlap with sourcing
        first_round_duration = 3 if experience_level in ['Entry-Level', 'Mid-Level'] else 4
        first_round_end = first_round_start + timedelta(weeks=first_round_duration)
        phases.append({
            'phase_number': 3,
            'phase_name': 'First Round Interviews',
            'start_date': first_round_start.strftime('%Y-%m-%d'),
            'end_date': first_round_end.strftime('%Y-%m-%d'),
            'duration': f'{first_round_duration} weeks',
            'objectives': [
                'Conduct product sense interviews',
                'Conduct execution interviews',
                'Assess technical understanding',
                'Evaluate culture fit',
                'Identify finalists'
            ],
            'deliverables': [
                'All first round interviews completed',
                'Interview feedback submitted',
                f'{hiring_plan["sourcing_plan"]["pipeline_goals"]["final_round_interviews"]} finalists identified',
                'Debrief sessions held'
            ],
            'success_criteria': 'Strong finalist slate advanced to final rounds'
        })

        # Phase 4: Final Round Interviews
        final_round_start = first_round_end
        final_round_duration = 2
        final_round_end = final_round_start + timedelta(weeks=final_round_duration)
        phases.append({
            'phase_number': 4,
            'phase_name': 'Final Round Interviews',
            'start_date': final_round_start.strftime('%Y-%m-%d'),
            'end_date': final_round_end.strftime('%Y-%m-%d'),
            'duration': f'{final_round_duration} weeks',
            'objectives': [
                'Conduct leadership/senior stakeholder interviews',
                'Complete reference checks',
                'Hold team debrief and make decisions',
                'Prepare offer packages',
                'Address any remaining questions'
            ],
            'deliverables': [
                'All final interviews completed',
                'Reference checks completed',
                'Hiring decisions made',
                'Offer packages prepared',
                'Offer approval obtained'
            ],
            'success_criteria': 'Ready to extend offers to top candidate(s)'
        })

        # Phase 5: Offer & Close
        offer_start = final_round_end
        offer_duration = 2
        offer_end = offer_start + timedelta(weeks=offer_duration)
        phases.append({
            'phase_number': 5,
            'phase_name': 'Offer & Close',
            'start_date': offer_start.strftime('%Y-%m-%d'),
            'end_date': offer_end.strftime('%Y-%m-%d'),
            'duration': f'{offer_duration} weeks',
            'objectives': [
                'Extend offers to top candidates',
                'Negotiate and finalize offer terms',
                'Obtain offer acceptance',
                'Begin onboarding preparation',
                'Close out search'
            ],
            'deliverables': [
                'Offers extended',
                'Offer accepted',
                'Background check completed',
                'Start date confirmed',
                'Onboarding plan ready'
            ],
            'success_criteria': 'Offer accepted and candidate ready to start'
        })

        return phases

    def _generate_milestones(self, start_date: datetime, duration_weeks: int) -> List[Dict[str, Any]]:
        """Generate key milestones."""
        milestones = [
            {
                'milestone': 'Job Posting Live',
                'target_date': (start_date + timedelta(days=3)).strftime('%Y-%m-%d'),
                'description': 'Job description finalized and posted on all channels',
                'critical': True
            },
            {
                'milestone': 'First Candidates Screened',
                'target_date': (start_date + timedelta(weeks=1)).strftime('%Y-%m-%d'),
                'description': 'Initial batch of recruiter screens completed',
                'critical': False
            },
            {
                'milestone': 'First Round Interviews Begin',
                'target_date': (start_date + timedelta(weeks=2)).strftime('%Y-%m-%d'),
                'description': 'First candidates move to interview stage',
                'critical': True
            },
            {
                'milestone': 'Finalist Slate Identified',
                'target_date': (start_date + timedelta(weeks=int(duration_weeks * 0.6))).strftime('%Y-%m-%d'),
                'description': 'Strong finalists identified for final rounds',
                'critical': True
            },
            {
                'milestone': 'Final Interviews Complete',
                'target_date': (start_date + timedelta(weeks=int(duration_weeks * 0.75))).strftime('%Y-%m-%d'),
                'description': 'All final interviews and reference checks done',
                'critical': True
            },
            {
                'milestone': 'Offer Extended',
                'target_date': (start_date + timedelta(weeks=int(duration_weeks * 0.85))).strftime('%Y-%m-%d'),
                'description': 'Offer extended to top candidate',
                'critical': True
            },
            {
                'milestone': 'Offer Accepted',
                'target_date': (start_date + timedelta(weeks=duration_weeks)).strftime('%Y-%m-%d'),
                'description': 'Candidate accepts offer and signs paperwork',
                'critical': True
            }
        ]

        return milestones

    def _generate_weekly_breakdown(self, start_date: datetime, duration_weeks: int,
                                   experience_level: str) -> List[Dict[str, Any]]:
        """Generate week-by-week activity breakdown."""
        weeks = []

        for week_num in range(1, duration_weeks + 1):
            week_start = start_date + timedelta(weeks=week_num - 1)
            week_end = week_start + timedelta(days=6)

            week_data = {
                'week_number': week_num,
                'start_date': week_start.strftime('%Y-%m-%d'),
                'end_date': week_end.strftime('%Y-%m-%d'),
                'phase': self._get_phase_for_week(week_num, duration_weeks),
                'key_activities': self._get_activities_for_week(week_num, duration_weeks, experience_level),
                'metrics_to_track': self._get_metrics_for_week(week_num, duration_weeks),
                'who_involved': self._get_team_for_week(week_num, duration_weeks)
            }

            weeks.append(week_data)

        return weeks

    def _get_phase_for_week(self, week_num: int, duration_weeks: int) -> str:
        """Determine phase for given week."""
        if week_num == 1:
            return 'Preparation & Setup'
        elif week_num <= 3:
            return 'Sourcing & Initial Screening'
        elif week_num <= int(duration_weeks * 0.7):
            return 'First Round Interviews'
        elif week_num <= int(duration_weeks * 0.9):
            return 'Final Round Interviews'
        else:
            return 'Offer & Close'

    def _get_activities_for_week(self, week_num: int, duration_weeks: int, experience_level: str) -> List[str]:
        """Get activities for specific week."""
        phase = self._get_phase_for_week(week_num, duration_weeks)

        activities_by_phase = {
            'Preparation & Setup': [
                'Finalize and approve job description',
                'Create and distribute interview rubrics',
                'Brief hiring team and train interviewers',
                'Post job on LinkedIn, company site, and job boards',
                'Launch referral campaign internally',
                'Begin direct sourcing and outreach',
                'Set up applicant tracking workflow'
            ],
            'Sourcing & Initial Screening': [
                'Continue sourcing candidates via multiple channels',
                'Review incoming applications daily',
                'Conduct 8-12 recruiter screening calls',
                'Update candidate pipeline dashboard',
                'Engage with employee referrals',
                'Post in PM communities and networks',
                'Identify candidates for first round interviews'
            ],
            'First Round Interviews': [
                'Schedule and conduct product sense interviews',
                'Schedule and conduct execution interviews',
                'Schedule and conduct technical interviews',
                'Collect and review interview feedback',
                'Hold debrief sessions for each candidate',
                'Continue sourcing to maintain pipeline',
                'Identify finalists for final rounds'
            ],
            'Final Round Interviews': [
                'Schedule final round with leadership',
                'Conduct behavioral and culture fit interviews',
                'Complete reference checks',
                'Hold final debrief and make decisions',
                'Prepare offer packages and get approvals',
                'Begin back-channel references if appropriate',
                'Keep candidates engaged and informed'
            ],
            'Offer & Close': [
                'Extend offers to selected candidate(s)',
                'Schedule offer call with hiring manager',
                'Negotiate terms if needed',
                'Answer candidate questions and concerns',
                'Obtain signed offer letter',
                'Initiate background check',
                'Begin onboarding preparation',
                'Communicate with other candidates'
            ]
        }

        return activities_by_phase.get(phase, [])

    def _get_metrics_for_week(self, week_num: int, duration_weeks: int) -> List[str]:
        """Get metrics to track for specific week."""
        phase = self._get_phase_for_week(week_num, duration_weeks)

        metrics_by_phase = {
            'Preparation & Setup': [
                'Job postings live (target: all channels)',
                'Hiring team trained (target: 100%)',
                'Sourcing channels activated'
            ],
            'Sourcing & Initial Screening': [
                'Applications received (target: 20+ per week)',
                'Screening calls completed (target: 8-12 per week)',
                'Screen-to-interview conversion rate (target: 50%)',
                'Pipeline health: ratio of candidates to roles'
            ],
            'First Round Interviews': [
                'Interviews conducted (target: 5-8 per week)',
                'Interview-to-finalist conversion (target: 40%)',
                'Time to feedback (target: <24 hours)',
                'Candidate satisfaction scores'
            ],
            'Final Round Interviews': [
                'Final interviews completed',
                'Reference checks completed',
                'Offer approval status',
                'Days to decision'
            ],
            'Offer & Close': [
                'Offers extended',
                'Offer acceptance rate (target: 80%+)',
                'Days from offer to acceptance',
                'Onboarding readiness'
            ]
        }

        return metrics_by_phase.get(phase, [])

    def _get_team_for_week(self, week_num: int, duration_weeks: int) -> List[str]:
        """Get team members involved in specific week."""
        phase = self._get_phase_for_week(week_num, duration_weeks)

        team_by_phase = {
            'Preparation & Setup': [
                'Hiring Manager',
                'Recruiter',
                'HR/People Ops',
                'Interview Panel'
            ],
            'Sourcing & Initial Screening': [
                'Recruiter (primary)',
                'Hiring Manager',
                'Recruiting Coordinator'
            ],
            'First Round Interviews': [
                'Product Managers',
                'Engineering Managers',
                'Design Leads',
                'Recruiter',
                'Recruiting Coordinator'
            ],
            'Final Round Interviews': [
                'Hiring Manager',
                'VP Product/CTO',
                'Cross-functional Leaders',
                'CEO (for senior roles)',
                'Recruiter'
            ],
            'Offer & Close': [
                'Hiring Manager',
                'Recruiter',
                'HR/People Ops',
                'Finance (for approvals)',
                'IT (for onboarding)'
            ]
        }

        return team_by_phase.get(phase, [])

    def _generate_dependencies(self) -> List[Dict[str, str]]:
        """Generate task dependencies."""
        return [
            {
                'task': 'First Round Interviews',
                'depends_on': 'Recruiter Screening Complete',
                'impact': 'Cannot start interviews without screened candidates'
            },
            {
                'task': 'Final Round Interviews',
                'depends_on': 'First Round Debrief Complete',
                'impact': 'Need to identify finalists before final rounds'
            },
            {
                'task': 'Offer Extension',
                'depends_on': 'Reference Checks Complete',
                'impact': 'Must complete due diligence before offer'
            },
            {
                'task': 'Interview Scheduling',
                'depends_on': 'Panel Availability',
                'impact': 'Limited interview slots can slow process'
            },
            {
                'task': 'Offer Approval',
                'depends_on': 'Budget Approval & Comp Review',
                'impact': 'Cannot extend offer without approval'
            },
            {
                'task': 'Start Date',
                'depends_on': 'Background Check Complete',
                'impact': 'Cannot onboard until background cleared'
            }
        ]

    def _generate_resource_allocation(self) -> Dict[str, Any]:
        """Generate resource allocation plan."""
        return {
            'recruiter_time': {
                'phase_1': '20 hours - setup and preparation',
                'phase_2': '30-40 hours - sourcing and screening',
                'phase_3': '20 hours - interview coordination',
                'phase_4': '15 hours - final round coordination',
                'phase_5': '10 hours - offer and close',
                'total': '95-105 hours'
            },
            'hiring_manager_time': {
                'phase_1': '10 hours - planning and setup',
                'phase_2': '5 hours - pipeline review',
                'phase_3': '20-25 hours - first round interviews',
                'phase_4': '15-20 hours - final interviews and decisions',
                'phase_5': '10 hours - offer and onboarding prep',
                'total': '60-70 hours'
            },
            'interview_panel_time': {
                'per_interviewer': '10-15 hours (including prep and feedback)',
                'total_panel': '50-75 hours (5 interviewers)',
                'note': 'Stagger to avoid overwhelming individual interviewers'
            },
            'recruiting_coordinator_time': {
                'total': '30-40 hours',
                'activities': 'Scheduling, logistics, candidate communication'
            }
        }

    def _generate_risk_timeline(self) -> List[Dict[str, Any]]:
        """Generate timeline risks and mitigation."""
        return [
            {
                'risk': 'Delayed Start',
                'timing': 'Week 1',
                'impact': 'Pushes entire timeline',
                'mitigation': 'Complete all prep work before official start date',
                'buffer': 'Build in 1 week buffer'
            },
            {
                'risk': 'Slow Pipeline Build',
                'timing': 'Weeks 2-3',
                'impact': 'Insufficient candidates for interviews',
                'mitigation': 'Multi-channel sourcing, start early, leverage referrals',
                'buffer': 'Target 3x pipeline coverage'
            },
            {
                'risk': 'Interview Scheduling Delays',
                'timing': 'Weeks 4-7',
                'impact': 'Extended time-to-hire, candidate drop-off',
                'mitigation': 'Block recurring interview slots, train backup interviewers',
                'buffer': 'Schedule 1-2 weeks out'
            },
            {
                'risk': 'Candidate Drops Out',
                'timing': 'Any time',
                'impact': 'Need to restart with new candidates',
                'mitigation': 'Maintain warm pipeline, move quickly, stay engaged',
                'buffer': 'Keep multiple candidates moving through process'
            },
            {
                'risk': 'Offer Negotiation Extends',
                'timing': 'Weeks 9-10',
                'impact': 'Delayed start date',
                'mitigation': 'Discuss comp early, understand expectations, have flexibility',
                'buffer': 'Build 1 week into offer phase'
            },
            {
                'risk': 'Background Check Delays',
                'timing': 'Week 10+',
                'impact': 'Cannot confirm start date',
                'mitigation': 'Use reputable background check vendor, initiate immediately',
                'buffer': 'Allow 1-2 weeks for background check'
            }
        ]

    def _generate_communication_plan(self) -> Dict[str, Any]:
        """Generate communication plan."""
        return {
            'internal_communication': {
                'daily': [
                    'Recruiter checks pipeline and responds to applications',
                    'Hiring manager reviews new candidates'
                ],
                'weekly': [
                    'Pipeline review meeting (recruiter + hiring manager)',
                    'Interview debriefs for each candidate',
                    'Status update to broader team'
                ],
                'bi_weekly': [
                    'Metrics review and strategy adjustment',
                    'Leadership update on progress'
                ]
            },
            'candidate_communication': {
                'application_received': 'Auto-acknowledgment within 24 hours',
                'after_screening': 'Decision within 2-3 business days',
                'between_interviews': 'Update within 3 business days',
                'after_final_interview': 'Decision within 48 hours',
                'offer_extended': 'Daily follow-up until decision',
                'rejection': 'Personalized note with feedback where appropriate'
            },
            'stakeholder_updates': {
                'weekly': 'Pipeline status to hiring team',
                'milestone_based': 'Updates at each major milestone',
                'monthly': 'Full metrics and strategy review with leadership',
                'issues': 'Immediate escalation of any blockers or risks'
            },
            'tools': [
                'ATS for tracking candidates',
                'Shared calendar for interviews',
                'Slack/Email for daily updates',
                'Dashboard for metrics',
                'Regular meetings for alignment'
            ]
        }

    def format_as_text(self, timeline: Dict[str, Any]) -> str:
        """Format timeline as readable text."""
        meta = timeline['metadata']

        output = f"""
{'='*80}
HIRING TIMELINE: {meta['role']}
{meta['company']}
{'='*80}

Generated: {meta['generated_date']}
Start Date: {meta['start_date']}
Estimated Duration: {meta['estimated_duration_weeks']} weeks
Target Hire Date: {meta['target_hire_date']}

PHASES
{'='*80}
"""
        for phase in timeline['phases']:
            output += f"\nPhase {phase['phase_number']}: {phase['phase_name']}\n"
            output += f"Duration: {phase['duration']} ({phase['start_date']} to {phase['end_date']})\n"
            output += f"Success Criteria: {phase['success_criteria']}\n"

            output += "\nObjectives:\n"
            for obj in phase['objectives']:
                output += f"  • {obj}\n"

            output += "\nDeliverables:\n"
            for deliv in phase['deliverables']:
                output += f"  • {deliv}\n"
            output += "\n"

        output += "\nKEY MILESTONES\n"
        output += "="*80 + "\n"
        for milestone in timeline['milestones']:
            critical = " [CRITICAL]" if milestone['critical'] else ""
            output += f"\n{milestone['target_date']}: {milestone['milestone']}{critical}\n"
            output += f"  {milestone['description']}\n"

        output += "\n\nWEEKLY BREAKDOWN\n"
        output += "="*80 + "\n"
        for week in timeline['weekly_breakdown']:
            output += f"\nWEEK {week['week_number']} ({week['start_date']} to {week['end_date']})\n"
            output += f"Phase: {week['phase']}\n"

            output += "Key Activities:\n"
            for activity in week['key_activities']:
                output += f"  • {activity}\n"

            output += "Metrics to Track:\n"
            for metric in week['metrics_to_track']:
                output += f"  • {metric}\n"

            output += f"Team Involved: {', '.join(week['who_involved'])}\n"

        output += "\n\nDEPENDENCIES & RISKS\n"
        output += "="*80 + "\n"
        for dep in timeline['dependencies']:
            output += f"\n{dep['task']} depends on {dep['depends_on']}\n"
            output += f"  Impact: {dep['impact']}\n"

        output += "\n\nTIMELINE RISKS\n"
        output += "="*80 + "\n"
        for risk in timeline['risk_timeline']:
            output += f"\n{risk['risk']} ({risk['timing']})\n"
            output += f"  Impact: {risk['impact']}\n"
            output += f"  Mitigation: {risk['mitigation']}\n"
            output += f"  Buffer: {risk['buffer']}\n"

        return output
