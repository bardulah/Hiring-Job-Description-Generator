# Agent Handoff Document: Hiring-Job-Description-Generator

**Last Updated**: 2025-11-10
**Current Agent**: Gemini

---

## 🎯 1. Current Status

### Project Overview
This is a sophisticated command-line (CLI) tool designed to automate the creation of hiring materials. It analyzes a company's specific needs and job descriptions from other companies to generate job descriptions, hiring plans, interview questions, and timelines.

### Deployment Status
*   **Status**: ✅ **Ready for CLI Use**
*   **Platform**: VPS (Not deployed as a service)
*   **Note**: This application is a **CLI tool**, not a web service. It was previously configured to run under PM2, which was incorrect. It has since been removed from PM2 and is intended to be run on-demand from the command line.

### Technology Stack
*   **Language**: Python
*   **Key Libraries**: FastAPI, Spacy, NLTK (Note: While FastAPI is a dependency, it is not currently used to serve a web application).

### Key Files
*   `INSTRUCTIONS.md`: User-facing guide on how to use the CLI tool.
*   `src/main.py`: The main entry point for the command-line application.
*   `requirements.txt`: The list of Python dependencies.

---

## 🚀 2. Recommended Improvements

This section outlines potential future enhancements for the project.

1.  **Web Interface**: The most valuable improvement would be to build a web-based front-end for this tool. Users could fill out forms with their company info, upload competitor job descriptions, and download the generated documents. The existing FastAPI dependency provides a perfect foundation for building this API.
2.  **ATS Integration**: Integrate with popular Applicant Tracking Systems (ATS) like Greenhouse or Lever to directly import the generated job descriptions and hiring plans.
3.  **Template Library**: Build a library of pre-made templates for various common roles (e.g., "Software Engineer," "Marketing Manager") that users can start from instead of providing all the input data from scratch.
4.  **AI Model Integration**: Integrate a large language model (like the Anthropic API key available in `secrets.env`) to significantly improve the quality, creativity, and nuance of the generated text for job descriptions and interview questions.
5.  **Feedback Loop**: Add a feature where users can rate the quality of the generated content, providing a feedback loop to fine-tune the generation algorithms over time.

---

## 🤝 3. Agent Handoff Notes

### How to Work on This Project

*   **Running the Tool**: This is a CLI tool. To run it, navigate to the project directory (`/opt/deployment/repos/Hiring-Job-Description-Generator`) and execute it with Python. Example: `python -m src.main`.
*   **Dependencies**: Python dependencies are managed in `requirements.txt`. If you add a new dependency, you will need to install it on the server using `pip install --break-system-packages <package-name>`.
*   **No Live Service**: Remember that this tool does **not** run as a persistent service. There is no `pm2` process for it, and it does not listen on a port.
*   **Potential for a Web App**: If the user decides to implement the "Web Interface" improvement, the `src/api/server.py` file contains a basic FastAPI application that can be used as a starting point. To run it, you would use a command like `uvicorn src.api.server:app --host 0.0.0.0 --port 8003`.
*   **Updating Documentation**: If you make any user-facing changes to the CLI commands, update the `INSTRUCTIONS.md` file. If you make architectural changes (like adding a web interface), update this `AGENTS.md` file.

### What to Watch Out For

*   **CLI, Not a Web App**: The most important thing to remember is the distinction between this tool and the other deployed services. Do not try to manage it with `pm2` or access it via a URL unless the web interface improvement is implemented.
*   **Python Environment**: The Python dependencies were installed globally on the server. Be mindful of potential conflicts if you add new libraries.
