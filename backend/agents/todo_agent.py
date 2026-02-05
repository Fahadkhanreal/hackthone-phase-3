import os
from typing import Dict, Any, List
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.conversation_helpers import create_conversation, get_conversation_by_id, get_messages_for_conversation, save_user_message, save_assistant_message
from uuid import UUID
import cohere
from auth.jwt_utils import extract_email_from_payload
from mcp_tools.add_task import add_task_tool
from mcp_tools.list_tasks import list_tasks_tool
from mcp_tools.complete_task import complete_task_tool
from mcp_tools.delete_task import delete_task_tool
from mcp_tools.update_task import update_task_tool


class TodoAgent:
    def __init__(self):
        # Initialize Cohere client
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")
        self.co = cohere.AsyncClient(api_key=api_key)

        # Store the tools that will be available to the agent in Cohere function format
        self.tools = [
            {
                "name": "add_task",
                "description": "Add a new task for the user. Use this when someone wants to add a task. Requires user_id and title, with optional description.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user creating the task"},
                        "title": {"type": "string", "description": "Title of the task to add"},
                        "description": {"type": "string", "description": "Optional description of the task to add"}
                    },
                    "required": ["user_id", "title"]
                }
            },
            {
                "name": "list_tasks",
                "description": "List tasks for the user based on status. Use this when someone wants to see their tasks. Requires user_id and optional status filter (all, pending, completed).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user whose tasks to list"},
                        "status": {"type": "string", "description": "Filter by status (all, pending, completed). Default is 'all'"}
                    },
                    "required": ["user_id"]
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a task as completed. Use this when someone wants to mark a task as done. Requires user_id and task_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user who owns the task"},
                        "task_id": {"type": "string", "description": "ID of the task to complete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task. Use this when someone wants to remove a task. Requires user_id and task_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user who owns the task"},
                        "task_id": {"type": "string", "description": "ID of the task to delete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            {
                "name": "update_task",
                "description": "Update a task. Use this when someone wants to change a task's title or description. Requires user_id and task_id, with optional title and description.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user who owns the task"},
                        "task_id": {"type": "string", "description": "ID of the task to update"},
                        "title": {"type": "string", "description": "New title for the task"},
                        "description": {"type": "string", "description": "New description for the task"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        ]

    async def process_message(self, session: AsyncSession, user_id: str, user_email: str, message: str, conversation_id: str = None):
        """
        Process a user message and return a response with potential tool calls

        Args:
            session: Async database session
            user_id: ID of the user making the request
            user_email: Email of the user making the request
            message: The user's message
            conversation_id: Optional conversation ID to continue an existing conversation

        Returns:
            Dictionary with conversation_id, response, and tool_calls
        """
        # Get or create conversation
        if conversation_id:
            conv = await get_conversation_by_id(session, UUID(conversation_id), UUID(user_id))
            if not conv:
                # If conversation not found or doesn't belong to user, create new one
                conv = await create_conversation(session, UUID(user_id))
                conversation_id = str(conv.id)
        else:
            conv = await create_conversation(session, UUID(user_id))
            conversation_id = str(conv.id)

        # Save the user's message
        await save_user_message(session, UUID(conversation_id), UUID(user_id), message)

        # Get conversation history
        messages = await get_messages_for_conversation(session, UUID(conversation_id), UUID(user_id))

        # Prepare chat history for Cohere
        chat_history = []
        for msg in messages:
            role = "USER" if msg.role == "user" else "CHATBOT"
            chat_history.append({
                "role": role,
                "message": msg.content
            })

        # Check if the user is asking for their identity
        if self._is_identity_query(message):
            response_text = f"Your email is {user_email}"

            # Save the assistant's response
            await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

            return {
                "conversation_id": conversation_id,
                "response": response_text,
                "tool_calls": []
            }

        # First, let's try to do basic command parsing before calling Cohere
        # This will handle simple cases where Cohere doesn't pick up on the tools
        lower_message = message.lower().strip()

        # Check for general conversation that should not trigger tools
        general_conversation_keywords = [
            "how are you", "how do you do", "what's up", "hello", "hi", "hey",
            "how is it going", "how are things", "what are you up to", "good morning",
            "good afternoon", "good evening", "how have you been", "what's new",
            # Roman Urdu variations
            "kya haal hai", "kya haal hy", "kya kar rahe ho", "kya kr rhe ho",
            "tum koun ho", "tum kon ho", "kya time ho raha hai", "kya time horha hai",
            "kya haal chal hai", "kya haal chal hy", "kese ho", "kaise ho",
            "allah hafiz", "khuda hafiz", "ramazan mubarak", "eid mubarak",
            "kya hal hai", "kya haal hay", "kya kar rahay ho", "kya kr rhay ho",
            "aap kaise hain", "aap kesay hain", "aap kaisy hain", "kya haaal hai"
        ]

        # Check if any general conversation keyword is in the message
        is_general_conversation = False
        matched_keyword = None
        for keyword in general_conversation_keywords:
            if keyword in lower_message:
                is_general_conversation = True
                matched_keyword = keyword
                break

        # Additional check for common Urdu/Hindi words that might appear in Romanized form
        common_urdu_hindi_words = [
            "kya", "hai", "hy", "ho", "koun", "kon", "kr", "rah", "rahe", "rahay",
            "time", "hora", "horha", "hal", "chal", "aap", "hain", "kaise", "kesay", "kaisy"
        ]

        # Count how many common Urdu/Hindi words are in the message
        urdu_word_count = sum(1 for word in common_urdu_hindi_words if word in lower_message)

        # Check if this is likely a general conversation
        is_simple_conversation = urdu_word_count >= 2 and len(lower_message.split()) <= 6

        # Check if the message is likely a simple greeting (not a task command)
        task_related_indicators = ["add", "list", "delete", "update", "complete", "task", "do ", "buy", "buy ", "make", "create"]
        is_task_related = any(indicator in lower_message for indicator in task_related_indicators)

        if is_general_conversation or (is_simple_conversation and not is_task_related):
            # For general conversation, provide a more varied response
            import random
            general_responses = [
                "Hi there! I'm your AI task assistant. You can ask me to add, list, complete, update, or delete tasks. How can I help you today?",
                "Hello! I'm here to help you manage your tasks. You can say things like 'Add a task: Buy groceries' or 'List my tasks'. What would you like to do?",
                "Hey! I'm your AI task assistant. I can help you organize your day by managing your tasks. Try saying 'Add task: Wash clothes' or similar!",
                "Greetings! I'm designed to help with your task management. You can ask me to add, list, complete, update, or delete tasks. How can I assist you?"
            ]

            response_text = random.choice(general_responses)

            # Save the assistant's response
            await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

            return {
                "conversation_id": conversation_id,
                "response": response_text,
                "tool_calls": []
            }

        # Simple command detection for common patterns
        if "add" in lower_message and ("task" in lower_message or "do" in lower_message or "buy" in lower_message):
            # Extract task title from message (simple extraction)
            import re
            # Look for patterns like "add task: title" or "add task title"
            add_match = re.search(r'(?:add\s+task(?:\s+to)?[:\s]*)?(.+?)(?:\.|$)', message, re.IGNORECASE)
            if not add_match:
                add_match = re.search(r'(?:add|create)\s+(?:a\s+)?(.+?)(?:\s+task)?(?:\.|$)', message, re.IGNORECASE)

            if add_match:
                task_title = add_match.group(1).strip().rstrip('.').strip()
                if task_title and len(task_title) > 0:
                    # Execute add_task tool directly
                    try:
                        result = await add_task_tool(session, user_id, task_title)
                        response_text = f"Task added: {task_title} ✅"

                        # Save the assistant's response
                        await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

                        return {
                            "conversation_id": conversation_id,
                            "response": response_text,
                            "tool_calls": [{"name": "add_task", "arguments": {"user_id": user_id, "title": task_title}}]
                        }
                    except Exception as e:
                        print(f"Error in direct add_task: {str(e)}")

        elif "delete" in lower_message and "task" in lower_message:
            # Extract task ID or title from message
            import re
            # Look for patterns like "delete task 1" or "delete task title"
            delete_match = re.search(r'delete\s+task\s+(.+?)(?:\.|$)', message, re.IGNORECASE)
            if delete_match:
                task_identifier = delete_match.group(1).strip()

                # Try to find the specific task to delete
                # First, list all tasks to see if the identifier matches
                try:
                    all_tasks = await list_tasks_tool(session, user_id, "all")

                    # Sort tasks by creation date to ensure consistent numbering
                    sorted_tasks = sorted(all_tasks, key=lambda x: x.get('created_at', ''))

                    # Check if the identifier is a sequential number (1, 2, 3...) or a specific task ID or part of a title
                    task_to_delete = None

                    # First check if it's a number (sequential task number)
                    if task_identifier.isdigit():
                        task_index = int(task_identifier) - 1  # Convert to 0-based index
                        if 0 <= task_index < len(sorted_tasks):
                            task_to_delete = sorted_tasks[task_index]
                    else:
                        # Check if it's a specific task ID or part of a title
                        for task in sorted_tasks:
                            if task_identifier == task['id'] or task_identifier.lower() in task['title'].lower():
                                task_to_delete = task
                                break

                    if task_to_delete:
                        # Execute the delete task tool
                        result = await delete_task_tool(session, user_id, task_to_delete['id'])
                        response_text = f"Task deleted: {task_to_delete['title']} ❌"

                        # Save the assistant's response
                        await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

                        return {
                            "conversation_id": conversation_id,
                            "response": response_text,
                            "tool_calls": [{"name": "delete_task", "arguments": {"user_id": user_id, "task_id": task_to_delete['id']}}]
                        }
                    else:
                        # If we can't find the specific task, ask user to list tasks first
                        response_text = f"I couldn't find a task matching '{task_identifier}'. Could you list your tasks first so I can identify the correct one to delete?"

                        # Save the assistant's response
                        await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

                        return {
                            "conversation_id": conversation_id,
                            "response": response_text,
                            "tool_calls": []
                        }
                except Exception as e:
                    print(f"Error in direct delete_task: {str(e)}")

            # If we can't extract or find the task, provide helpful response
            response_text = "To delete a task, please specify which task. You can say 'delete task 1' if you know the task number, or first ask me to 'list tasks' so I can help you identify the correct one."

            # Save the assistant's response
            await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

            return {
                "conversation_id": conversation_id,
                "response": response_text,
                "tool_calls": []
            }

        elif "delete" in lower_message and "task" in lower_message:
            # Extract task ID or title from message
            import re
            # Look for patterns like "delete task 1" or "delete task title"
            delete_match = re.search(r'delete\s+task\s+(.+?)(?:\.|$)', message, re.IGNORECASE)
            if delete_match:
                task_identifier = delete_match.group(1).strip()

                # Try to find the specific task to delete
                # First, list all tasks to see if the identifier matches
                try:
                    all_tasks = await list_tasks_tool(session, user_id, "all")

                    # Sort tasks by creation date to ensure consistent numbering
                    sorted_tasks = sorted(all_tasks, key=lambda x: x.get('created_at', ''))

                    # Check if the identifier is a sequential number (1, 2, 3...) or a specific task ID or part of a title
                    task_to_delete = None

                    # First check if it's a number (sequential task number)
                    if task_identifier.isdigit():
                        task_index = int(task_identifier) - 1  # Convert to 0-based index
                        if 0 <= task_index < len(sorted_tasks):
                            task_to_delete = sorted_tasks[task_index]
                    else:
                        # Check if it's a specific task ID or part of a title
                        for task in sorted_tasks:
                            if task_identifier == task['id'] or task_identifier.lower() in task['title'].lower():
                                task_to_delete = task
                                break

                    if task_to_delete:
                        # Execute the delete task tool
                        result = await delete_task_tool(session, user_id, task_to_delete['id'])
                        response_text = f"Task deleted: {task_to_delete['title']} ❌"

                        # Save the assistant's response
                        await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

                        return {
                            "conversation_id": conversation_id,
                            "response": response_text,
                            "tool_calls": [{"name": "delete_task", "arguments": {"user_id": user_id, "task_id": task_to_delete['id']}}]
                        }
                    else:
                        # If we can't find the specific task, ask user to list tasks first
                        response_text = f"I couldn't find a task matching '{task_identifier}'. Could you list your tasks first so I can identify the correct one to delete?"

                        # Save the assistant's response
                        await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

                        return {
                            "conversation_id": conversation_id,
                            "response": response_text,
                            "tool_calls": []
                        }
                except Exception as e:
                    print(f"Error in direct delete_task: {str(e)}")

            # If we can't extract or find the task, provide helpful response
            response_text = "To delete a task, please specify which task. You can say 'delete task 1' if you know the task number, or first ask me to 'list tasks' so I can help you identify the correct one."

            # Save the assistant's response
            await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

            return {
                "conversation_id": conversation_id,
                "response": response_text,
                "tool_calls": []
            }

        elif "update" in lower_message and "task" in lower_message:
            # Extract task ID and new content from message
            import re
            # Look for patterns like "update task 1 to new title" or "update task 1 new title"
            update_match = re.search(r'update\s+task\s+(\w+)\s+(?:to\s+)?(.+?)(?:\.|$)', message, re.IGNORECASE)
            if update_match:
                task_identifier = update_match.group(1).strip()
                new_content = update_match.group(2).strip()

                # Try to find the specific task to update
                try:
                    all_tasks = await list_tasks_tool(session, user_id, "all")

                    # Sort tasks by creation date to ensure consistent numbering
                    sorted_tasks = sorted(all_tasks, key=lambda x: x.get('created_at', ''))

                    # Check if the identifier is a sequential number (1, 2, 3...) or a specific task ID or part of a title
                    task_to_update = None

                    # First check if it's a number (sequential task number)
                    if task_identifier.isdigit():
                        task_index = int(task_identifier) - 1  # Convert to 0-based index
                        if 0 <= task_index < len(sorted_tasks):
                            task_to_update = sorted_tasks[task_index]
                    else:
                        # Check if it's a specific task ID or part of a title
                        for task in sorted_tasks:
                            if task_identifier == task['id'] or task_identifier.lower() in task['title'].lower():
                                task_to_update = task
                                break

                    if task_to_update:
                        # Execute the update task tool - try to determine if new_content is a title or description
                        # For simplicity, we'll treat it as a new title for now
                        result = await update_task_tool(session, user_id, task_to_update['id'], title=new_content)
                        response_text = f"Task updated: {result['title']} ✏️"

                        # Save the assistant's response
                        await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

                        return {
                            "conversation_id": conversation_id,
                            "response": response_text,
                            "tool_calls": [{"name": "update_task", "arguments": {"user_id": user_id, "task_id": task_to_update['id'], "title": new_content}}]
                        }
                    else:
                        # If we can't find the specific task, ask user to list tasks first
                        response_text = f"I couldn't find a task matching '{task_identifier}'. Could you list your tasks first so I can identify the correct one to update?"

                        # Save the assistant's response
                        await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

                        return {
                            "conversation_id": conversation_id,
                            "response": response_text,
                            "tool_calls": []
                        }
                except Exception as e:
                    print(f"Error in direct update_task: {str(e)}")

            # If we can't extract or find the task, provide helpful response
            response_text = "To update a task, please specify which task and what to change it to. For example: 'Update task 1 to New Title' or 'Update task 1 to New Title and Description'. You can also ask me to 'list tasks' first to see your current tasks."

            # Save the assistant's response
            await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

            return {
                "conversation_id": conversation_id,
                "response": response_text,
                "tool_calls": []
            }

        elif "list" in lower_message and ("task" in lower_message or "my" in lower_message):
            # Execute list_tasks tool directly
            try:
                result = await list_tasks_tool(session, user_id, "all")

                if result:
                    # Remove duplicates by task ID to prevent display issues
                    seen_ids = set()
                    unique_tasks = []
                    for task in result:
                        if task['id'] not in seen_ids:
                            unique_tasks.append(task)
                            seen_ids.add(task['id'])

                    # Sort tasks by creation date to ensure consistent numbering
                    sorted_tasks = sorted(unique_tasks, key=lambda x: x.get('created_at', ''))
                    task_list_str = "\n".join([f"- {idx + 1}: {task['title']} ({'completed' if task['completed'] else 'pending'})" for idx, task in enumerate(sorted_tasks)])
                    response_text = f"Here are your tasks:\n{task_list_str}"
                else:
                    response_text = "You don't have any tasks yet."

                # Save the assistant's response
                await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

                return {
                    "conversation_id": conversation_id,
                    "response": response_text,
                    "tool_calls": [{"name": "list_tasks", "arguments": {"user_id": user_id, "status": "all"}}]
                }
            except Exception as e:
                print(f"Error in direct list_tasks: {str(e)}")

        elif "complete" in lower_message and "task" in lower_message:
            # Extract task ID from message
            import re
            # Look for patterns like "complete task 1" or "mark task 1 complete"
            complete_match = re.search(r'(?:complete|mark|finish)\s+task\s+(\w+)', message, re.IGNORECASE)
            if complete_match:
                task_identifier = complete_match.group(1).strip()

                # Try to find the specific task to complete
                try:
                    all_tasks = await list_tasks_tool(session, user_id, "all")

                    # Sort tasks by creation date to ensure consistent numbering
                    sorted_tasks = sorted(all_tasks, key=lambda x: x.get('created_at', ''))

                    # Check if the identifier is a sequential number (1, 2, 3...) or a specific task ID or part of a title
                    task_to_complete = None

                    # First check if it's a number (sequential task number)
                    if task_identifier.isdigit():
                        task_index = int(task_identifier) - 1  # Convert to 0-based index
                        if 0 <= task_index < len(sorted_tasks):
                            task_to_complete = sorted_tasks[task_index]
                    else:
                        # Check if it's a specific task ID or part of a title
                        for task in sorted_tasks:
                            if task_identifier == task['id'] or task_identifier.lower() in task['title'].lower():
                                task_to_complete = task
                                break

                    if task_to_complete:
                        # Execute the complete task tool
                        result = await complete_task_tool(session, user_id, task_to_complete['id'])
                        response_text = f"Task completed: {task_to_complete['title']} ✅"

                        # Save the assistant's response
                        await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

                        return {
                            "conversation_id": conversation_id,
                            "response": response_text,
                            "tool_calls": [{"name": "complete_task", "arguments": {"user_id": user_id, "task_id": task_to_complete['id']}}]
                        }
                    else:
                        # If we can't find the specific task, ask user to list tasks first
                        response_text = f"I couldn't find a task matching '{task_identifier}'. Could you list your tasks first so I can identify the correct one to complete?"

                        # Save the assistant's response
                        await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

                        return {
                            "conversation_id": conversation_id,
                            "response": response_text,
                            "tool_calls": []
                        }
                except Exception as e:
                    print(f"Error in direct complete_task: {str(e)}")

            # If we can't extract or find the task, provide helpful response
            response_text = "To complete a task, please specify which task. You can say 'Complete task 1' if you know the task number, or first ask me to 'list tasks' so I can help you identify the correct one."

            # Save the assistant's response
            await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

            return {
                "conversation_id": conversation_id,
                "response": response_text,
                "tool_calls": []
            }

        # If simple command parsing didn't work, fall back to Cohere
        try:
            # Call Cohere to generate response with potential tool calls
            response = await self.co.chat(
                model="command-r-plus",
                message=message,
                chat_history=chat_history,
                tools=self.tools,
                force_single_step=True,
                # Add more specific parameters to encourage tool use
                preamble="You are an AI assistant that helps users manage their tasks. Always use the provided tools when users ask to add, list, complete, delete, or update tasks. Be direct and helpful. For general conversation that doesn't involve tasks, respond appropriately."
            )

            # Process tool calls if any
            tool_calls = []
            tool_results = []

            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tool_call in response.tool_calls:
                    tool_calls.append({
                        "name": tool_call.name,
                        "arguments": tool_call.parameters
                    })

                    # Execute the tool call
                    result = await self._execute_tool_call(
                        session,
                        tool_call.name,
                        tool_call.parameters,
                        user_id
                    )

                    tool_results.append({
                        "call_id": tool_call.id,
                        "outputs": [result]
                    })

            # Generate final response based on tool results
            if tool_results:
                final_response = await self.co.chat(
                    model="command-r-plus",
                    message=message,
                    chat_history=chat_history + [{"role": "USER", "message": message}],
                    tools=self.tools,
                    tool_results=tool_results
                )
                response_text = final_response.text
            else:
                # Check if response has a text attribute, otherwise use a default
                if hasattr(response, 'text'):
                    response_text = response.text
                    # If the response doesn't seem to have used tools when it should have,
                    # and it's a simple greeting, provide a helpful response
                    lower_response = response_text.lower()
                    if ("hello" in lower_response or "hi " in lower_response or
                        "hey" in lower_response or "can help" in lower_response):
                        response_text = "Hello! I'm your AI task assistant. You can ask me to add, list, complete, update, or delete tasks. For example: 'Add a task: Buy groceries' or 'List my tasks'."
                else:
                    response_text = "Hello! I'm your AI task assistant. You can ask me to add, list, complete, update, or delete tasks."
        except Exception as e:
            # If Cohere call fails, return a friendly default response
            import traceback
            print(f"Cohere API error: {str(e)}")
            print(traceback.format_exc())

            response_text = "Hello! I'm your AI task assistant. You can ask me to add, list, complete, update, or delete tasks."
            tool_calls = []

        # Save the assistant's response
        await save_assistant_message(session, UUID(conversation_id), UUID(user_id), response_text)

        return {
            "conversation_id": conversation_id,
            "response": response_text,
            "tool_calls": tool_calls
        }

    def _is_identity_query(self, message: str) -> bool:
        """
        Check if the user is asking for their identity
        """
        lower_msg = message.lower()
        identity_keywords = ["who am i", "what is my email", "my email", "email address", "identity", "user info"]

        for keyword in identity_keywords:
            if keyword in lower_msg:
                return True
        return False

    async def _execute_tool_call(self, session: AsyncSession, tool_name: str, parameters: Dict[str, Any], user_id: str):
        """
        Execute a specific tool call
        """
        # Add user_id to parameters if not already present
        params = parameters.copy()
        if "user_id" not in params:
            params["user_id"] = user_id

        # Map tool names to actual functions
        tool_functions = {
            "add_task": add_task_tool,
            "list_tasks": list_tasks_tool,
            "complete_task": complete_task_tool,
            "delete_task": delete_task_tool,
            "update_task": update_task_tool
        }

        # Execute the appropriate tool
        if tool_name in tool_functions:
            func = tool_functions[tool_name]

            # Call the function with the appropriate parameters
            if tool_name == "list_tasks":
                # For list_tasks, status is optional
                status = params.get("status", "all")
                result = await func(session, user_id, status)
            elif tool_name == "add_task":
                # For add_task, description is optional
                title = params["title"]
                description = params.get("description")
                result = await func(session, user_id, title, description)
            elif tool_name in ["complete_task", "delete_task"]:
                # For these, only user_id and task_id are needed
                task_id = params["task_id"]
                result = await func(session, user_id, task_id)
            elif tool_name == "update_task":
                # For update_task, title and description are optional
                task_id = params["task_id"]
                title = params.get("title")
                description = params.get("description")
                result = await func(session, user_id, task_id, title, description)
            else:
                result = await func(session, **params)

            return result
        else:
            return {"error": f"Unknown tool: {tool_name}"}