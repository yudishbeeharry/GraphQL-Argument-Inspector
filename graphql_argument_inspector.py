import json
import sys
import urllib.request
import urllib.error

INTROSPECTION_QUERY = json.dumps({
    "query": """
    query IntrospectionQuery {
      __schema {
        queryType { name kind }
        mutationType { name kind }
        subscriptionType { name kind }
        types {
          ...FullType
        }
        directives {
          name
          description
          locations
          args {
            ...InputValue
          }
        }
      }
    }

    fragment FullType on __Type {
      kind
      name
      description
      fields(includeDeprecated: true) {
        name
        description
        args {
          ...InputValue
        }
        type {
          ...TypeRef
        }
        isDeprecated
        deprecationReason
      }
      inputFields {
        ...InputValue
      }
      interfaces {
        ...TypeRef
      }
      enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
      }
      possibleTypes {
        ...TypeRef
      }
    }

    fragment InputValue on __InputValue {
      name
      description
      type { ...TypeRef }
      defaultValue
    }

    fragment TypeRef on __Type {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
    """
}).encode("utf-8")


def fetch_schema(base_url):
    graphql_url = base_url.rstrip("/") + "/graphql"

    req = urllib.request.Request(
        graphql_url,
        data=INTROSPECTION_QUERY,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"[!] HTTP error {e.code} at {graphql_url}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[!] Connection error: {e.reason}")
        sys.exit(1)


def find_query_type(schema):
    for t in schema["data"]["__schema"]["types"]:
        if t.get("name") == "Query" and t.get("kind") == "OBJECT":
            return t
    print("[!] Query type not found")
    sys.exit(1)


def analyze_queries(query_type):
    requires_args = {}
    no_args = []

    for field in query_type.get("fields", []):
        name = field["name"]
        args = field.get("args", [])

        if not args:
            no_args.append(name)
            continue

        arg_details = []
        for arg in args:
            arg_name = arg["name"]
            arg_type = arg["type"]
            required = arg_type["kind"] == "NON_NULL"
            arg_details.append((arg_name, required))

        requires_args[name] = arg_details

    return requires_args, no_args


def main(base_url):
    schema = fetch_schema(base_url)
    query_type = find_query_type(schema)
    requires_args, no_args = analyze_queries(query_type)

    print("\n=== Queries that REQUIRE arguments ===")
    for query, args in requires_args.items():
        formatted = ", ".join(
            f"{name}{' (required)' if req else ''}"
            for name, req in args
        )
        print(f"- {query}: {formatted}")

    print("\n=== Queries that DO NOT require arguments ===")
    for query in no_args:
        print(f"- {query}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <base_url>")
        print("Example: python graphql_args_full_introspection.py http://94.237.63.174:35005")
        sys.exit(1)

    main(sys.argv[1])
