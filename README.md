# 🏢 Autonomous Enterprise IT Operations Center
**An Enterprise-Grade Multi-Agent Swarm powered by Agno v2.0+, Model Context Protocol (MCP), Agentic RAG, and Human-in-the-Loop (HITL) Governance.**

---

## 📖 Overview
In modern enterprise environments, IT support tickets rarely live in a single system. Diagnosing an issue requires checking corporate identity directories, reading local endpoint crash logs, searching runbooks, and sometimes sending official notifications.

This repository demonstrates a **Multi-Agent Supervisor Swarm**: five specialized AI agents that collaborate autonomously to investigate issues, gather verification data, and recommend or take actions (with optional human approval for sensitive steps).

---

## 🏛️ System Architecture & Workflow

```mermaid
graph TD
    User([👤 Employee / User]) -->|HTTP / WebSocket| OS[🖥️ AgentOS Runtime : Port 7777]
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
```

---

## 🤖 Agent Roster (high level)

| Agent Name | Primary Role | Underlying Technology | Data Source |
|---|---:|---|---|
| Supervisor Team | Orchestrates workflows, delegates tasks, synthesizes findings | Agno Team ReAct Engine | SQLite memory, runtime context |
| Identity Specialist | Query corporate identity, validate user contexts | MCP / SQL adapters | stage_data/active_directory.db |
| Device Diagnostics Specialist | Collect & parse endpoint logs, run diagnostics | MCP / filesystem adapters | stage_data/logs/ |
| Incident Historian | Find prior incidents and timelines | MCP / SQL adapters | stage_data/incident_history.db |
| Knowledge Specialist | Vector search over runbooks & KB | Agentic RAG, LanceDB | stage_data/lancedb_store |
| Communication Specialist | Draft and send notifications | SMTP bridge with HITL approval | SMTP (optional live dispatch) |

---

## Quickstart

1. Clone the repository

```bash
git clone https://github.com/lernwithshubham/agentic-it-center.git
cd agentic-it-center
```

2. Create a Python virtual environment and install dependencies

Option A (recommended, using uv):

```bash
uv venv
source .venv/bin/activate          # On Windows PowerShell: .venv\Scripts\activate
uv pip install -r requirements.txt
```

Option B (standard Python venv + pip):

```bash
python3 -m venv venv
source venv/bin/activate            # On Windows PowerShell: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables

Set your Google Gemini (or other model) API key:

macOS / Linux:

```bash
export GOOGLE_API_KEY="your_actual_gemini_api_key_here"
```

Windows (PowerShell):

```powershell
$env:GOOGLE_API_KEY = "your_actual_gemini_api_key_here"
```

(Optional) To enable live email dispatch in the Human-in-the-Loop demo, export SMTP credentials:

```bash
export SMTP_SENDER_EMAIL="your_email@gmail.com"
export SMTP_APP_PASSWORD="your_16_digit_app_password"
```

4. Bootstrap the enterprise environment (creates SQLite DBs, logs, and runbooks)

The repository does not include scripts/bootstrap_demo.py. Instead run the provided setup script:

```bash
python setup_env.py
```

This will generate:
- stage_data/active_directory.db
- stage_data/incident_history.db
- stage_data/logs/vpn_connection_error.log
- stage_data/runbooks/vpn_policy.md

5. Run the AgentOS server (local)

Start the production example runtime directly with:

```bash
python production_it_center.py
```

The script boots AgentOS and serves the IT Operations Center runtime on port 7777 (it prints a startup banner). Note: the example uses Agno's MCP stdio pipelines; the production script calls agent_os.serve(..., reload=False) which is required for those pipelines to remain stable.

---

## 🎮 Live Walkthrough & Testing

Once the server is running you can interact with the control plane UI or use provided code paths to exercise the multi-agent workflows. The HITL approval gate will intercept any actions that require explicit human confirmation (for example: sending a real SMTP email).

A few useful code references:
- setup_env.py — creates demo databases, logs, and markdown runbooks.
- production_it_center.py — defines agents, MCP connectors, the Team supervisor, and boots AgentOS.

---

## Contributing

Contributions are welcome. Please open issues or pull requests for bug fixes, improvements, or documentation updates.

---

## License

This project is provided under the MIT License. See the LICENSE file for details.
