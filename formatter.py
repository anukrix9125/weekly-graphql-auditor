def print_graphql_report(schema_exposed, vuln_fields):
    print("\n" + "="*50)
    print("       GRAPHQL SECURITY AUDIT SUMMARY       ")
    print("="*50)
    print(f"[*] Introspection Enabled: {'[YES - VULNERABLE]' if schema_exposed else '[NO - SECURE]'}")
    print(f"[*] Sensitive Field Access Probed: {len(vuln_fields)} query vector(s) executed.")
    print("="*50 + "\n")