import argparse
import asyncio
from introspect import audit_graphql_introspection
from field_auditor import generate_sensitive_query, audit_field_access
from formatter import print_graphql_report

def main():
    parser = argparse.ArgumentParser(description="Automated GraphQL Introspection & Authorization Auditor")
    parser.add_argument("--url", required=True, help="Target GraphQL endpoint URL")
    parser.add_argument("--token", default=None, help="Optional Authorization Bearer token")

    args = parser.parse_args()

    headers = {"Authorization": f"Bearer {args.token}"} if args.token else None

    print(f"[*] Step 1: Auditing Introspection status on {args.url}")
    schema = audit_graphql_introspection(args.url, headers)

    vulnerabilities = []
    if schema:
        print("[*] Step 2: Leveraging Antigravity to generate targeted sensitive queries...")
        summary_str = str(schema)[:1500]
        query = asyncio.run(generate_sensitive_query(summary_str))
        print(f"\n[+] Generated Query Payload:\n{query}\n")

        print("[*] Step 3: Probing sensitive field access...")
        status, resp_data = audit_field_access(args.url, query, headers)
        if status == 200:
            vulnerabilities.append(query)

    print_graphql_report(bool(schema), vulnerabilities)

if __name__ == "__main__":
    main()