# Data Model: Todo AI Chatbot Extension

## Entity Definitions

### Conversation
- **Purpose**: Represents a user's chat session with the AI chatbot
- **Fields**:
  - `id`: UUID (Primary Key) - Unique identifier for the conversation
  - `user_id`: UUID (Foreign Key) - Links to the user who owns this conversation
  - `created_at`: DateTime - Timestamp when the conversation was initiated
  - `updated_at`: DateTime - Timestamp when the conversation was last updated
- **Relationships**: Belongs to one User, contains many Messages
- **Validation**: user_id must match authenticated user's ID for security

### Message
- **Purpose**: Represents individual messages exchanged between user and chatbot
- **Fields**:
  - `id`: UUID (Primary Key) - Unique identifier for the message
  - `user_id`: UUID (Foreign Key) - Links to the user who owns this message
  - `conversation_id`: UUID (Foreign Key) - Links to the conversation this message belongs to
  - `role`: String (Enum: "user", "assistant") - Indicates if message is from user or AI
  - `content`: String (Text) - The actual message content
  - `created_at`: DateTime - Timestamp when the message was created
- **Relationships**: Belongs to one Conversation and one User
- **Validation**: user_id must match authenticated user's ID, role must be either "user" or "assistant"

### Task (Existing - Extended)
- **Purpose**: Represents user tasks managed through the AI chatbot
- **Fields** (existing):
  - `id`: UUID (Primary Key) - Unique identifier for the task
  - `title`: String (Varchar) - Task title (1-255 characters)
  - `description`: String (Optional, Text) - Task description (up to 1000 characters)
  - `completed`: Boolean - Completion status of the task
  - `created_at`: DateTime - Timestamp when the task was created
  - `updated_at`: DateTime - Timestamp when the task was last updated
  - `user_id`: UUID (Foreign Key) - Links to the user who owns this task
- **Relationships**: Belongs to one User
- **Validation**: All existing validations remain, user_id must match authenticated user's ID

## Data Relationships

```
User (1) ←→ (Many) Conversation
User (1) ←→ (Many) Message
User (1) ←→ (Many) Task
Conversation (1) ←→ (Many) Message
```

## Security Constraints

- Every database query must filter by `user_id` to ensure proper user isolation
- No cross-user data access is permitted
- Conversation and Message entities inherit user_id from the authenticated user
- All operations must validate that the authenticated user owns the accessed data

## State Transitions

### Task State Transitions
- `pending` → `completed`: When complete_task tool is called
- `completed` → `pending`: When update_task tool is called to uncomplete a task

### Message Creation Flow
1. User sends message → New Message record created with role="user"
2. AI responds → New Message record created with role="assistant"
3. Both messages linked to same Conversation and authenticated user_id

## Indexing Strategy

- Index on `user_id` for all entities (Conversation, Message, Task) for efficient filtering
- Index on `conversation_id` in Message table for efficient conversation history retrieval
- Index on `created_at` in Message table for chronological ordering