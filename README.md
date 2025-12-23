# GraphQL-Argument-Inspector
A lightweight, dependency-free Python tool that discovers which GraphQL queries require arguments by automatically running a full introspection query against a target endpoint. This helps to identify which queries accept user-controlled input and are therefore better candidates to inspect for SQLi.

Limitations & Requirements
This tool relies on GraphQL introspection and will only function correctly under the following conditions:
GraphQL introspection is enabled on the target endpoint
The endpoint is reachable without authentication, or valid authentication headers are provided externally (e.g., via a proxy)
The schema follows standard GraphQL introspection behavior
If introspection is disabled, restricted, or filtered by authorisation logic, the tool will not be able to enumerate queries or determine which fields require arguments.

Run the tool by providing the target GraphQL endpoint URL as the sole argument:
python3 graphql_argument_inspector.py http(s)://target:port
