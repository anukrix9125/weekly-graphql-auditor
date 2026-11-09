import asyncio
import requests
from google.antigravity import Agent, LocalAgentConfig

async def generate_sensitive_query(schema_types_summary: str):
    """Uses Google Antigravity Agent to generate targeted GraphQL queries for sensitive fields."""
    config = LocalAgentConfig(
        system_instructions="You are an expert GraphQL security auditor. Given a summary of schema types, generate a valid GraphQL query string targeting sensitive fields like user data, emails, roles, or private tokens. Output ONLY the raw GraphQL query string inside standard code formatting or plain text."
    )
    async with Agent(config) as agent:
        response = await agent.chat(f"Create a targeted GraphQL query to extract user records and private fields based on this schema: {schema_types_summary}")
        return await response.text()

def audit_field_access(target_url, query_payload, headers=None):
    """Dispatches the targeted query to check if sensitive fields are accessible without auth."""
    hdrs = {"Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)

    try:
        print(f"[*] Dispatching targeted field audit query to: {target_url}")
        response = requests.post(target_url, json={"query": query_payload}, headers=hdrs, timeout=10)

        print(f"[+] Response Status: {response.status_code}")
        print(f"[+] Response Body: {response.text[:300]}...")
        return response.status_code, response.json() if response.headers.get("content-type", "").startswith("application/json") else None
    except Exception as e:
        print(f"[-] Field audit execution failed: {e}")
        return None, None

if __name__ == "__main__":
    print("[+] Field Auditor module loaded.")