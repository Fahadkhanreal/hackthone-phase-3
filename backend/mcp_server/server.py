# This file is a placeholder for the MCP server.
# The actual tools are directly imported from mcp_tools directory.
# This maintains the architecture while avoiding import errors during server startup.
pass
from mcp_tools.add_task import add_task_tool
from mcp_tools.list_tasks import list_tasks_tool
from mcp_tools.complete_task import complete_task_tool
from mcp_tools.delete_task import delete_task_tool
from mcp_tools.update_task import update_task_tool
from sqlmodel.ext.asyncio.session import AsyncSession


# Create the FastMCP server instance
mcp_server = FastMCP(
    name="Todo AI Chatbot MCP Server",
    description="MCP server for managing tasks through natural language AI chatbot"
)


@mcp_server.tool(
    name="add_task",
    description="Add a new task for the user. Requires user_id, title, and optional description.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ID of the user creating the task"},
            "title": {"type": "string", "description": "Title of the task"},
            "description": {"type": "string", "description": "Optional description of the task"}
        },
        "required": ["user_id", "title"]
    }
)
async def add_task_handler(session: AsyncSession, user_id: str, title: str, description: str = None):
    """Handler for the add_task tool."""
    return await add_task_tool(session, user_id, title, description)


@mcp_server.tool(
    name="list_tasks",
    description="List tasks for the user based on status. Requires user_id and optional status filter (all, pending, completed).",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ID of the user whose tasks to list"},
            "status": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all", "description": "Filter by status"}
        },
        "required": ["user_id"]
    }
)
async def list_tasks_handler(session: AsyncSession, user_id: str, status: str = "all"):
    """Handler for the list_tasks tool."""
    return await list_tasks_tool(session, user_id, status)


@mcp_server.tool(
    name="complete_task",
    description="Mark a task as completed. Requires user_id and task_id.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ID of the user who owns the task"},
            "task_id": {"type": "string", "description": "ID of the task to complete"}
        },
        "required": ["user_id", "task_id"]
    }
)
async def complete_task_handler(session: AsyncSession, user_id: str, task_id: str):
    """Handler for the complete_task tool."""
    return await complete_task_tool(session, user_id, task_id)


@mcp_server.tool(
    name="delete_task",
    description="Delete a task. Requires user_id and task_id.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ID of the user who owns the task"},
            "task_id": {"type": "string", "description": "ID of the task to delete"}
        },
        "required": ["user_id", "task_id"]
    }
)
async def delete_task_handler(session: AsyncSession, user_id: str, task_id: str):
    """Handler for the delete_task tool."""
    return await delete_task_tool(session, user_id, task_id)


@mcp_server.tool(
    name="update_task",
    description="Update a task. Requires user_id and task_id, with optional title and description.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ID of the user who owns the task"},
            "task_id": {"type": "string", "description": "ID of the task to update"},
            "title": {"type": "string", "description": "New title for the task (optional)"},
            "description": {"type": "string", "description": "New description for the task (optional)"}
        },
        "required": ["user_id", "task_id"]
    }
)
async def update_task_handler(session: AsyncSession, user_id: str, task_id: str, title: str = None, description: str = None):
    """Handler for the update_task tool."""
    return await update_task_tool(session, user_id, task_id, title, description)


# Run the server if this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp_server.app, host="0.0.0.0", port=3000)