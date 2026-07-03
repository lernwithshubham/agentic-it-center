import sqlite3
import os

def bootstrap_environment():
    os.makedirs("stage_data/logs", exist_ok=True)
    os.makedirs("stage_data/runbooks", exist_ok=True)

    # 1. Real Active Directory SQLite Database
    conn_ad = sqlite3.connect("stage_data/active_directory.db")
    cursor_ad = conn_ad.cursor()
    cursor_ad.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL,
            lockout_count INTEGER DEFAULT 0,
            mfa_status TEXT NOT NULL,
            pwd_expiration_days INTEGER NOT NULL
        )
    """)
    employees = [
        ("shubham@enterprise.com", "ACTIVE", 0, "ENABLED_FUNCTIONING", 45),
        ("ravi@enterprise.com", "LOCKED", 5, "FAILED_TOO_MANY_ATTEMPTS", -1),
        ("sarah@enterprise.com", "ACTIVE", 0, "ENABLED_FUNCTIONING", 12)
    ]
    cursor_ad.executemany("INSERT OR REPLACE INTO employees (email, status, lockout_count, mfa_status, pwd_expiration_days) VALUES (?, ?, ?, ?, ?)", employees)
    conn_ad.commit()
    conn_ad.close()

    # 2. Real Historical Incident SQLite Database
    conn_inc = sqlite3.connect("stage_data/incident_history.db")
    cursor_inc = conn_inc.cursor()
    cursor_inc.execute("""
        CREATE TABLE IF NOT EXISTS past_incidents (
            incident_id TEXT PRIMARY KEY,
            error_code TEXT NOT NULL,
            symptom_summary TEXT NOT NULL,
            root_cause TEXT NOT NULL,
            resolution_step TEXT NOT NULL
        )
    """)
    incidents = [
        ("INC-89921", "ERR-809-CERT-EXPIRED", "Multiple users unable to connect to IKEv2 VPN tunnel after July 1st.", "Local client hardware certificates expired.", "Instructed users to renew certificates via https://portal.enterprise.internal/certs."),
        ("INC-44102", "AUTH-LOCKOUT-MFA", "Outlook continually asking for passwords and rejecting logins.", "Account locked due to brute-force or multiple failed MFA prompt pushes.", "Unlock AD account and reset MFA registration seed.")
    ]
    cursor_inc.executemany("INSERT OR REPLACE INTO past_incidents VALUES (?, ?, ?, ?, ?)", incidents)
    conn_inc.commit()
    conn_inc.close()

    # 3. Real Endpoint Log File on Hard Drive
    log_content = """[2026-07-04 08:14:22] [ENDPOINT_MONITOR] [ERROR] Tunnel establishment aborted for shubham@enterprise.com
[2026-07-04 08:14:22] [IKEv2_PROTOCOL] Error Code: ERR-809-CERT-EXPIRED
[2026-07-04 08:14:22] [CRYPTO_SUBSYSTEM] Machine Hardware Certificate expired on 2026-07-03. Handshake rejected."""
    with open("stage_data/logs/vpn_connection_error.log", "w") as f:
        f.write(log_content)

    # 4. Real Knowledge Base Runbook Doc
    runbook_content = """# Standard Operating Procedure: VPN Error ERR-809-CERT-EXPIRED

## Background
Error ERR-809 indicates that the employee's local machine certificate has expired. Active Directory credentials and passwords are NOT affected by this issue.

## Protocol
1. Do NOT reset Active Directory passwords.
2. Instruct the user to open `https://portal.enterprise.internal/certs`.
3. Click **"Renew Hardware Certificate"** and restart their endpoint."""
    with open("stage_data/runbooks/vpn_policy.md", "w") as f:
        f.write(runbook_content)

    print("✅ Real SQL databases, logs, and markdown runbooks successfully generated in ./stage_data/")

if __name__ == "__main__":
    bootstrap_environment()