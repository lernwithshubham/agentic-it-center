# 🏢 Autonomous Enterprise IT Operations Center
**An Enterprise-Grade Multi-Agent Swarm powered by Agno v2.0+, Model Context Protocol (MCP), Agentic RAG, and Human-in-the-Loop (HITL) Governance.**

---

## 📖 Overview
In modern enterprise environments, IT support tickets rarely live in a single system. Diagnosing an issue requires checking corporate identity directories, reading local endpoint crash logs, searching policy runbooks, and cross-referencing historical outages.

Instead of a standard single-prompt chatbot, this repository demonstrates a **Multi-Agent Supervisor Swarm**. Five specialized AI agents collaborate autonomously to investigate issues, gather verified evidence using open industry standards (**Model Context Protocol**), and propose structured Root Cause Analyses (RCA) before executing human-approved remediation actions.

---

## 🏛️ System Architecture & Workflow

```mermaid
graph TD
    User([👤 Employee / User]) -->|HTTP / Web Socket| OS[🖥️ AgentOS Runtime : Port 7777]
    OS -->|Control Plane UI| UI[🌐 os.agno.com Dashboard]
    UI -->|Prompt| SUP[🧠 Supervisor Team : IT Operations Center]

    subgraph Specialists [Specialized Worker Swarm]
        SUP -->|Delegate| ID[🔐 Identity Specialist]
        SUP -->|Delegate| DEV[💻 Device Diagnostics Specialist]
        SUP -->|Delegate| HIST[📜 Incident Historian]
        SUP -->|Delegate| KNOW[📚 Knowledge Specialist]
        SUP -->|Delegate| COMM[📧 Communication Specialist]
    end

    subgraph DataLayer [Physical Stage Data Layer]
        ID <-->|MCP Stdio : SQL| AD_DB[(active_directory.db)]
        DEV <-->|MCP Stdio : Filesystem| LOGS[/stage_data/logs/]
        HIST <-->|MCP Stdio : SQL| INC_DB[(incident_history.db)]
        KNOW <-->|Agentic RAG : Vector Search| VEC[(LanceDB Vector Store)]
    end

    COMM -->|Intercept Execution| HITL{⚖️ Human-in-the-Loop Approval Gate}
    HITL -->|Approve| SMTP[🚀 Live SMTP Email Dispatch]


====

🤖 The Agent RosterAgent NamePrimary RoleUnderlying TechnologyData SourceSupervisor TeamOrchestrates workflows, delegates tasks, and synthesizes findings.Agno Team ReAct EngineSQLite Memory (operations_center_state.db)Identity SpecialistVerifies Active Directory health, MFA status, and account lockouts.Official Python MCP Server (mcp-server-sqlite)stage_data/active_directory.dbDevice DiagnosticsReads raw endpoint logs, crash dumps, and local configs.Node/NPM MCP Server (@modelcontextprotocol/server-filesystem)stage_data/logs/Incident HistorianQueries historical outage databases to find verified past fixes.Official Python MCP Server (mcp-server-sqlite)stage_data/incident_history.dbKnowledge SpecialistRetrieves official IT Standard Operating Procedures (SOPs).Agentic RAG (Knowledge + LanceDb)stage_data/lancedb_store/Communication SpecialistDrafts and dispatches final resolution emails to employees.Native Tool Calling + @tool(requires_confirmation=True)Live SMTP Network Relay🛠️ PrerequisitesBefore starting, ensure your local development machine has the following installed:Python 3.10+Node.js & NPM (npx -v must return a valid version to run filesystem MCP servers).Google Gemini API Key (Get one free from Google AI Studio).(Optional) uv Package Manager for lightning-fast environment setup.🚀 Step-by-Step Setup GuideStep 1: Clone the RepositoryBashgit clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME
Step 2: Create Virtual Environment & Install DependenciesYou can use either modern uv or standard pip:Option A: Using uv (Recommended - Ultra Fast)Bash# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows PowerShell: .venv\Scripts\activate

# Install dependencies directly from requirements.txt
uv pip install -r requirements.txt
Option B: Using Standard Python pipBashpython3 -m venv venv
source venv/bin/activate   # On Windows PowerShell: venv\Scripts\activate

pip install -r requirements.txt
Step 3: Configure Environment VariablesSet your Google Gemini API key in your terminal session:macOS / Linux:Bashexport GOOGLE_API_KEY="your_actual_gemini_api_key_here"
Windows (PowerShell):PowerShell$env:GOOGLE_API_KEY="your_actual_gemini_api_key_here"
(Optional) If you want the swarm to send real live emails to your inbox during the Human-in-the-Loop demo, export your SMTP credentials:Bashexport SMTP_SENDER_EMAIL="your_email@gmail.com"
export SMTP_APP_PASSWORD="your_16_digit_app_password"
Step 4: Bootstrap the Enterprise EnvironmentRun the automated setup script. This dynamically builds physical SQLite databases, generates endpoint logs, writes markdown runbooks, and initializes folder structures inside a local stage_data/ directory:Bashpython setup_env.py
(Verify: You should see a success message indicating all databases and runbooks were created cleanly).Step 5: Boot the AgentOS ServerLaunch the master Agno runtime on local port 7777:Bashpython production_it_center.py
(Verify: Your terminal will display the ASCII AgentOS banner and state that Uvicorn is running on http://localhost:7777).🎮 Live Walkthrough & TestingOnce your server is running in the terminal, connect your dashboard to observe the agents in action:Open your web browser and navigate to the official Control Plane UI: https://os.agno.com.Click Connect OS (or Add OS) $\rightarrow$ select the Local tab.Enter http://localhost:7777 and click Connect.Select IT Support Operations Center from the sidebar menu.Scenario 1: Multi-Agent Root Cause Analysis (RCA)Copy and paste the following prompt into the chat console:"Since yesterday I can't connect to VPN. My email is shubham@enterprise.com. Please investigate the root cause and email me the instructions."What to observe in the UI:Open the Traces tab on the right sidebar. Watch the live execution graph as the Supervisor delegates sub-tasks concurrently.SQL Execution via MCP: Observe the Identity Specialist executing real SQL against active_directory.db to verify account status.Filesystem Execution via MCP: Observe the Device Diagnostics Specialist reading vpn_connection_error.log directly off your disk.Vector Retrieval: Observe the Knowledge Specialist semantic-searching LanceDB for Runbook ERR-809-CERT-EXPIRED.Scenario 2: Human-in-the-Loop (HITL) Governance GateWhen the swarm finishes its investigation, the Communication Specialist will attempt to dispatch an official resolution email.Execution Halts: Notice that the chat console pauses execution. An interactive confirmation box appears displaying the recipient, subject line, and draft email body.Review & Approve: Select Approve (or Yes) inside the confirmation box.Submit: Click the SUBMIT button.Dispatch: The runtime resumes execution, opens the SMTP tunnel, delivers the email, and logs the final state to disk.🛑 Troubleshooting Common Issuesnpm error 404 / E404 during startup: Ensure you installed mcp-server-sqlite via pip/uv. The application uses the official Python MCP server for SQLite to avoid Node C++ compilation bottlenecks.Submit button is disabled / grayed out: Ensure you explicitly selected an option (Approve or Reject) inside the tool confirmation box before clicking Submit.Run Error: requirements parameter must be provided: Do not refresh the browser mid-execution while a HITL confirmation card is pending. If disconnected, click + NEW SESSION and re-run the prompt.