# Instructions for Hiring System Generator

This guide provides instructions on how to use the Hiring System Generator tool.

## What It Does

This is a powerful command-line tool that automates the creation of a complete hiring package for a new role at your company. It saves you time and helps standardize your hiring process.

By analyzing your company's needs and examples of similar job descriptions, it generates:
*   A professional **Job Description** tailored to the role.
*   A strategic **Hiring Plan** with sourcing strategies and budgets.
*   A detailed **Interview Rubric** with specific questions and evaluation criteria.
*   A week-by-week **Hiring Timeline**.

## How to Use It

This is a Command-Line Interface (CLI) tool, which means you run it from your terminal.

### Prerequisites

*   You must be logged into the server where the tool is located.
*   Navigate to the project directory: `cd /opt/deployment/repos/Hiring-Job-Description-Generator`

### Basic Usage

The easiest way to see the tool in action is to run it with the provided example files.

```bash
# Run the generator with example data
python -m src.main
```

This command will:
1.  Use the sample data located in the `examples/` directory.
2.  Generate a complete set of hiring documents.
3.  Save the output files to the `output/` directory.

### Using Your Own Data

To generate a real hiring plan, you need to provide two input files:

1.  **`job_descriptions.json`**: A JSON file containing an array of 5-10 job descriptions for similar roles from other companies. This helps the tool understand the market.
2.  **`company_info.json`**: A JSON file containing specific details about the role at your company (e.g., title, salary, responsibilities, benefits).

You can use `examples/sample_job_descriptions.json` and `examples/sample_company_info.json` as templates for creating your own input files.

Once your files are ready, run the following command, replacing the file paths with your own:

```bash
python -m src.main path/to/your_job_descriptions.json path/to/your_company_info.json path/to/your_output_directory
```

### Output Files

The tool will generate a set of `.txt` and `.json` files in your specified output directory, including:
*   `*_job_description.txt`
*   `*_hiring_plan.txt`
*   `*_interview_rubric.txt`
*   `*_timeline.txt`

These documents provide a comprehensive and structured foundation for your entire hiring process.
