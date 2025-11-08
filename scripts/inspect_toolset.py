import inspect
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

print("--- Inspecting McpToolset ---")
print("\nMethods:")
for name, func in inspect.getmembers(McpToolset, inspect.isfunction):
    print(f"- {name}{inspect.signature(func)}")

print("\nAttributes:")
for name, var in inspect.getmembers(McpToolset, lambda a: not(inspect.isroutine(a))):
    if not name.startswith('_'):
        print(f"- {name}")

print("\n--- dir(McpToolset) ---")
print(dir(McpToolset))
