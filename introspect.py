import requests
import json

INTROSPECTION_QUERY = """
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    types {
      name
      kind
      fields {
        name
        args {
          name
          type { name kind }
        }
      }
    }
  }
}
"""

def audit_graphql_introspection(target_url, headers=None):
    """Sends a standard introspection query to determine if GraphQL schema is exposed."""
    hdrs = {"Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)

    payload = {"query": INTROSPECTION_QUERY}

    try:
        print(f"[*] Sending introspection query to: {target_url}")
        response = requests.post(target_url, json=payload, headers=hdrs, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if "data" in data and data["data"].get("__schema"):
                print("[!] VULNERABLE: GraphQL Introspection is enabled publicly!")
                return data["data"]["__schema"]
            else:
                print("[-] Secure: Introspection returned errors or restricted schema.")
        else:
            print(f"[-] HTTP Error {response.status_code}: Endpoint rejected request.")

    except requests.RequestException as e:
        print(f"[-] Connection failed: {e}")
    return None

if __name__ == "__main__":
    print("[+] GraphQL Introspection module loaded.")