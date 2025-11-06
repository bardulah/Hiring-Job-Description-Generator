"""
Analytics and usage tracking system.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from .models import UsageMetrics, FeedbackRecord
from .logging_config import get_logger
from .config import config

logger = get_logger(__name__)


class AnalyticsManager:
    """Manages analytics and usage tracking."""

    def __init__(self, storage_path: str = 'data/analytics'):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.enabled = config.get('analytics.enabled', True)

        if not self.enabled:
            logger.info("Analytics disabled")

    def track_usage(self, metrics: UsageMetrics):
        """Track usage metrics."""
        if not self.enabled:
            return

        try:
            # Append to daily log file
            date_str = datetime.now().strftime('%Y-%m-%d')
            log_file = self.storage_path / f'usage_{date_str}.jsonl'

            with open(log_file, 'a') as f:
                f.write(metrics.json() + '\n')

            logger.debug(f"Tracked usage: {metrics.request_id}")

        except Exception as e:
            logger.error(f"Failed to track usage: {e}")

    def record_feedback(self, feedback: FeedbackRecord):
        """Record hiring outcome feedback."""
        if not self.enabled:
            return

        try:
            feedback_file = self.storage_path / 'feedback.jsonl'

            with open(feedback_file, 'a') as f:
                f.write(feedback.json() + '\n')

            logger.info(f"Recorded feedback for candidate: {feedback.candidate_id}")

        except Exception as e:
            logger.error(f"Failed to record feedback: {e}")

    def get_usage_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get usage statistics for the past N days."""
        if not self.enabled:
            return {'enabled': False}

        try:
            all_metrics: List[UsageMetrics] = []

            # Read log files from past N days
            from datetime import timedelta
            start_date = datetime.now() - timedelta(days=days)

            for log_file in self.storage_path.glob('usage_*.jsonl'):
                try:
                    with open(log_file, 'r') as f:
                        for line in f:
                            try:
                                metric = UsageMetrics.parse_raw(line)
                                if metric.timestamp >= start_date:
                                    all_metrics.append(metric)
                            except:
                                continue
                except:
                    continue

            if not all_metrics:
                return {'total_requests': 0, 'period_days': days}

            # Calculate statistics
            total_requests = len(all_metrics)
            successful = sum(1 for m in all_metrics if m.success)
            failed = total_requests - successful

            # Group by experience level
            by_level = {}
            for metric in all_metrics:
                level = metric.experience_level
                if level not in by_level:
                    by_level[level] = 0
                by_level[level] += 1

            # Calculate average processing time
            processing_times = [m.processing_time for m in all_metrics if m.success]
            avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0

            return {
                'enabled': True,
                'period_days': days,
                'total_requests': total_requests,
                'successful': successful,
                'failed': failed,
                'success_rate': (successful / total_requests * 100) if total_requests > 0 else 0,
                'by_experience_level': by_level,
                'average_processing_time': round(avg_processing_time, 2),
                'requests_per_day': round(total_requests / days, 2)
            }

        except Exception as e:
            logger.error(f"Failed to get usage stats: {e}")
            return {'error': str(e)}

    def get_feedback_insights(self) -> Dict[str, Any]:
        """Get insights from hiring feedback."""
        if not self.enabled:
            return {'enabled': False}

        try:
            feedback_file = self.storage_path / 'feedback.jsonl'
            if not feedback_file.exists():
                return {'total_feedback': 0}

            all_feedback: List[FeedbackRecord] = []

            with open(feedback_file, 'r') as f:
                for line in f:
                    try:
                        feedback = FeedbackRecord.parse_raw(line)
                        all_feedback.append(feedback)
                    except:
                        continue

            if not all_feedback:
                return {'total_feedback': 0}

            # Calculate statistics
            total = len(all_feedback)
            hired = sum(1 for f in all_feedback if f.hired)
            hire_rate = (hired / total * 100) if total > 0 else 0

            # Average time to hire
            times = [f.time_to_hire for f in all_feedback if f.time_to_hire is not None and f.hired]
            avg_time_to_hire = sum(times) / len(times) if times else None

            # Average performance rating
            ratings = [f.performance_rating for f in all_feedback if f.performance_rating is not None and f.hired]
            avg_rating = sum(ratings) / len(ratings) if ratings else None

            # Average retention
            retention = [f.retention_months for f in all_feedback if f.retention_months is not None]
            avg_retention = sum(retention) / len(retention) if retention else None

            return {
                'enabled': True,
                'total_feedback': total,
                'hired_count': hired,
                'hire_rate': round(hire_rate, 2),
                'average_time_to_hire_days': round(avg_time_to_hire, 1) if avg_time_to_hire else None,
                'average_performance_rating': round(avg_rating, 2) if avg_rating else None,
                'average_retention_months': round(avg_retention, 1) if avg_retention else None
            }

        except Exception as e:
            logger.error(f"Failed to get feedback insights: {e}")
            return {'error': str(e)}

    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analytics."""
        recommendations = []

        try:
            stats = self.get_usage_stats(days=30)
            feedback = self.get_feedback_insights()

            # Check success rate
            if stats.get('success_rate', 100) < 90:
                recommendations.append("Success rate is below 90%. Review error logs to identify common issues.")

            # Check processing time
            if stats.get('average_processing_time', 0) > 60:
                recommendations.append("Average processing time exceeds 60 seconds. Consider optimizing analysis pipeline.")

            # Check time to hire
            if feedback.get('average_time_to_hire_days'):
                avg_time = feedback['average_time_to_hire_days']
                if avg_time > 60:
                    recommendations.append(f"Average time to hire is {avg_time:.0f} days. Consider streamlining interview process.")

            # Check performance ratings
            if feedback.get('average_performance_rating'):
                avg_rating = feedback['average_performance_rating']
                if avg_rating < 3.5:
                    recommendations.append(f"Average hire performance rating is {avg_rating:.1f}/5.0. Review interview criteria.")

        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")

        return recommendations if recommendations else ["No recommendations at this time. System performing well!"]


# Global analytics instance
analytics_manager = AnalyticsManager()
