# Research Summary: Todo AI Chatbot Implementation

## Decision 1: Cohere API Integration
- **What was chosen**: Direct Cohere API integration using cohere package with tool calling functionality
- **Rationale**: Cohere's command-r-plus model offers excellent tool calling capabilities that can be adapted from OpenAI-style patterns. The cohere package provides native tool calling support without requiring langchain-cohere wrapper initially.
- **Alternatives considered**:
  - langchain-cohere: More abstracted but potentially adds complexity
  - Direct HTTP calls to Cohere API: Less convenient but more control
- **Implementation approach**: Using cohere.ChatMessage to handle conversation history and cohere.function_call to handle tool calls

## Decision 2: MCP Server Configuration
- **What was chosen**: FastMCP implementation with official Python SDK for MCP protocol
- **Rationale**: FastMCP is the recommended MCP server implementation that follows the official specification. It provides proper tool registration and JSON schema validation.
- **Alternatives considered**:
  - Custom MCP implementation: Would require more work and potential non-compliance
  - Third-party MCP servers: May not follow specification correctly
- **Implementation approach**: Creating separate tools module with proper JSON schemas for each of the 5 required tools

## Decision 3: OpenAI ChatKit Integration
- **What was chosen**: OpenAI ChatKit embeddable component with custom backend connection
- **Rationale**: OpenAI ChatKit provides a ready-made, well-designed chat interface that can be connected to custom backends via API endpoints.
- **Alternatives considered**:
  - Building custom chat UI: More time-consuming but more customizable
  - Alternative chat components: Might lack the features of ChatKit
- **Implementation approach**: Using ChatKit's custom domain setup to connect to our /api/{user_id}/chat endpoint

## Decision 4: Floating Chat Icon Component
- **What was chosen**: React floating action button with Tailwind CSS for styling
- **Rationale**: Tailwind provides responsive design capabilities and integrates well with Next.js. A floating action button pattern is familiar to users.
- **Alternatives considered**:
  - Custom SVG icons: More control over appearance
  - Third-party icon libraries: Might add bundle size
- **Implementation approach**: Fixed positioning with Tailwind classes, smooth animations using CSS transitions

## Decision 5: Environment Variables Configuration
- **What was chosen**: Standard environment variable setup with proper separation of frontend/backend variables
- **Rationale**: Following standard practices for secure handling of API keys and configuration
- **Variables identified**:
  - Backend: COHERE_API_KEY, BETTER_AUTH_SECRET, DATABASE_URL
  - Frontend: NEXT_PUBLIC_API_URL, NEXT_PUBLIC_OPENAI_DOMAIN_KEY
- **Implementation approach**: Adding to .env.example files and documenting in README

## Decision 6: Database Transaction Patterns
- **What was chosen**: Async SQLModel sessions with proper error handling and user_id filtering
- **Rationale**: Maintains consistency with existing codebase while ensuring security and performance
- **Implementation approach**: Using existing session factory pattern from database.py with additional user_id validation

## Decision 7: JWT Token Extraction for Identity Queries
- **What was chosen**: Direct extraction from authorization header in chat endpoint
- **Rationale**: Efficient way to access user identity without additional database queries
- **Implementation approach**: Extending existing JWT validation utility to extract user email when needed

## Decision 8: Conversation State Management
- **What was chosen**: Server-side stateless design with database persistence
- **Rationale**: Aligns with constitutional requirement for statelessness while ensuring data persistence
- **Implementation approach**: Each chat request retrieves conversation history from DB, processes request, saves new messages to DB