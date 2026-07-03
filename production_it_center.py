import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from agno.agent import Agent
from agno.approval import approval
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.os import AgentOS
from agno.team import Team
from agno.tools import tool
from agno.tools.mcp import MCPTools
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.google import GeminiEmbedder

# =====================================================================
# 1. REAL VECTOR KNOWLEDGE BASE (Agentic RAG via LanceDB)
# =====================================================================

knowledge_base = Knowledge(
    name="Enterprise IT Runbooks",
    vector_db=LanceDb(
        table_name="it_runbooks",
        uri="stage_data/lancedb_store",
        embedder=GeminiEmbedder(id="gemini-embedding-001")
    ),
)
# Load real markdown files from disk into vector store
knowledge_base.insert(path="stage_data/runbooks/vpn_policy.md")

# =====================================================================
# 2. REAL HUMAN-IN-THE-LOOP SMTP TOOL
# =====================================================================

#@approval
@tool(requires_confirmation=True)
def send_real_resolution_email(recipient: str, subject: str, body: str) -> str:
    """Send an official IT resolution email to an employee over live SMTP.
    Requires human confirmation before executing.
    
    Args:
        recipient (str): Employee email address.
        subject (str): Email subject line.
        body (str): Detailed resolution instructions.
    """
    # Replace with real credentials or a test Gmail/App Password
    SMTP_SERVER = "smtp.gmail.com" 
    SMTP_PORT = 587
    SENDER_EMAIL = os.getenv("SMTP_SENDER_EMAIL", "test_ops@enterprise.com")
    SENDER_PASSWORD = os.getenv("SMTP_APP_PASSWORD", "mock_password_if_unset")
    
    try:
        if SENDER_PASSWORD == "mock_password_if_unset":
            print(f"\n[SMTP SIMULATION] Real email payload ready for {recipient}. Set SMTP_APP_PASSWORD env var to dispatch over wire.")
            return f"Resolution email prepared and approved for {recipient} regarding '{subject}'."

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient
        msg["Subject"] = f"[IT Operations] {subject}"
        msg.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            
        return f"Real SMTP email delivered successfully to {recipient}."
    except Exception as e:
        return f"SMTP Dispatch failed: {str(e)}"

# =====================================================================
# 3. OFFICIAL MCP CONNECTORS TO REAL DATABASES & FILES
# =====================================================================

# Official Python SQLite MCP Server connected to physical Active Directory SQL db
mcp_ad_server = MCPTools(
    command="mcp-server-sqlite --db-path stage_data/active_directory.db"
)

# Official Python SQLite MCP Server connected to historical incidents SQL db
mcp_incidents_server = MCPTools(
    command="mcp-server-sqlite --db-path stage_data/incident_history.db"
)

# Real Filesystem MCP Server connected to physical endpoint logs
mcp_filesystem_server = MCPTools(
    command="npx -y @modelcontextprotocol/server-filesystem stage_data/logs"
)

# =====================================================================
# 4. SPECIALIZED AGENT ROSTER
# =====================================================================

identity_agent = Agent(
    name="Identity Specialist",
    role="Query corporate Active Directory SQL records via MCP.",
    model=Gemini(id="gemini-2.5-flash"),
    tools=[mcp_ad_server],
    instructions="Use SQLite MCP tools (like query or list_tables) to inspect the 'employees' table. Execute SQL queries to check lockout status and MFA health.",
)

device_agent = Agent(
    name="Device Diagnostics Specialist",
    role="Read endpoint crash dumps and connection logs from the filesystem via MCP.",
    model=Gemini(id="gemini-2.5-flash"),
    tools=[mcp_filesystem_server],
    instructions="Use filesystem MCP tools to list directory contents and read files in stage_data/logs to extract specific error codes.",
)

knowledge_agent = Agent(
    name="Knowledge Specialist",
    role="Retrieve IT runbook documentation from local vector database.",
    model=Gemini(id="gemini-2.5-flash"),
    knowledge=knowledge_base,
    search_knowledge=True, # Enables Agentic RAG
    instructions="Search the vector knowledge base for exact error codes or technical symptoms reported by other agents.",
)

incident_agent = Agent(
    name="Incident Historian",
    role="Query historical SQL databases via MCP to find past resolutions.",
    model=Gemini(id="gemini-2.5-flash"),
    tools=[mcp_incidents_server],
    instructions="Use SQLite MCP tools to execute SQL queries on the 'past_incidents' table to match current error codes against historical root causes.",
)

communication_agent = Agent(
    name="Communication Specialist",
    role="Dispatch final resolution emails via SMTP.",
    model=Gemini(id="gemini-2.5-flash"),
    tools=[send_real_resolution_email],
    instructions="Format a professional, step-by-step resolution email and invoke the email tool.",
)

# =====================================================================
# 5. TEAM SUPERVISOR & RUNTIME
# =====================================================================

shared_db = SqliteDb(db_file="stage_data/operations_center_state.db")

it_operations_center = Team(
    name="IT Support Operations Center",
    model=Gemini(id="gemini-2.5-flash"),
    members=[identity_agent, device_agent, knowledge_agent, incident_agent, communication_agent],
    db=shared_db,
    add_history_to_context=True,
    instructions=[
        "You are the Lead Supervisor coordinating real system diagnostics.",
        "When an issue is reported:",
        "1. Ask Identity Specialist to query SQL records for the user's email.",
        "2. Ask Device Diagnostics Specialist to read filesystem logs.",
        "3. Ask Incident Historian to query historical SQL incident records.",
        "4. Ask Knowledge Specialist to search the vector runbook store.",
        "5. Direct the Communication Specialist to email the resolution.",
    ],
    show_members_responses=True,
    markdown=True,
)

agent_os = AgentOS(
    id="it-support-os",
    teams=[it_operations_center],
    tracing=True
)

app = agent_os.get_app()

if __name__ == "__main__":
    print("🚀 Booting Real Enterprise IT Operations Center Runtime on port 7777...")
    # NOTE: reload=False is strictly required by Agno when running persistent stdio MCP pipelines inside AgentOS
    agent_os.serve(app="production_it_center:app", host="localhost", port=7777, reload=False)