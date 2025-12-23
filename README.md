# GraphQL-Argument-Inspector
A lightweight, dependency-free Python tool that discovers which GraphQL queries require arguments by automatically running a full introspection query against a target endpoint. This helps to identify which queries accept user-controlled input and are therefore better candidates to inspect for SQLi.

Run the tool by providing the target GraphQL endpoint URL as the sole argument:
python3 graphql_argument_inspector.py http(s)://target:port
