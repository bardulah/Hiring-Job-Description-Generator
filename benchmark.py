"""
Benchmark v1.0 vs v2.0 analyzer performance.
"""

import time
import json
from src.analyzer import JobDescriptionAnalyzer as V1Analyzer
from src.analyzers.nlp_analyzer import NLPAnalyzer as V2Analyzer
from src.core.models import JobDescription

# Load sample data
with open('examples/sample_job_descriptions.json', 'r') as f:
    job_data = json.load(f)

# Convert to models for v2
job_descriptions_v2 = [JobDescription(**jd) for jd in job_data]

print("="*80)
print("BENCHMARK: v1.0 vs v2.0 Analyzer")
print("="*80)
print(f"\nAnalyzing {len(job_data)} job descriptions...\n")

# Benchmark v1.0
print("v1.0 Analyzer (Original)")
print("-" * 40)
v1_analyzer = V1Analyzer()

start = time.time()
v1_result = v1_analyzer.analyze_multiple_descriptions(job_data)
v1_time = time.time() - start

print(f"Time: {v1_time:.3f}s")
print(f"Skills found: {len(v1_result['common_skills'])}")
print(f"Top 5 skills: {list(v1_result['common_skills'].keys())[:5]}")
print()

# Benchmark v2.0
print("v2.0 Analyzer (NLP-Enhanced, without spaCy)")
print("-" * 40)
v2_analyzer = V2Analyzer()

start = time.time()
v2_result = v2_analyzer.analyze_multiple_descriptions(job_descriptions_v2)
v2_time = time.time() - start

print(f"Time: {v2_time:.3f}s")
print(f"Skills found: {len(v2_result.common_skills)}")
print(f"Top 5 skills: {list(v2_result.common_skills.keys())[:5]}")
print()

# Compare
print("="*80)
print("COMPARISON")
print("="*80)
print(f"Performance: v2.0 is {v1_time/v2_time:.2f}x {'faster' if v2_time < v1_time else 'slower'}")
print(f"Skill detection: v1={len(v1_result['common_skills'])}, v2={len(v2_result.common_skills)}")

# Quality comparison
v1_skills_set = set(v1_result['common_skills'].keys())
v2_skills_set = set(v2_result.common_skills.keys())

common = v1_skills_set & v2_skills_set
only_v1 = v1_skills_set - v2_skills_set
only_v2 = v2_skills_set - v1_skills_set

print(f"\nSkill Detection Quality:")
print(f"  Both found: {len(common)}")
print(f"  Only v1: {len(only_v1)}")
print(f"  Only v2: {len(only_v2)}")

if only_v2:
    print(f"\n  New skills found by v2: {list(only_v2)[:10]}")

# New features in v2
print(f"\nNew Features in v2.0:")
print(f"  ✓ Skill categorization: {list(v2_result.insights[0]['skills_by_category'].keys())}")
print(f"  ✓ Experience years extracted: {v2_result.insights[0].get('experience_years', 'N/A')}")
print(f"  ✓ Salary insights: {'Yes' if v2_result.salary_insights else 'No'}")
print(f"  ✓ Market comparison: {'Yes' if v2_result.market_comparison else 'No'}")

print("\n" + "="*80)
