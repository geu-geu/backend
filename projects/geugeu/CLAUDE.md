# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important Development Workflow

**ALWAYS commit your changes after completing each job or task.** When you finish implementing a feature, fixing a bug, or completing any development task, create a git commit with a clear, descriptive message. This ensures:
- Progress is saved incrementally
- Changes can be reviewed individually
- Easy rollback if needed
- Clear development history

## Development Commands

### Running the Application
- `uv run uvicorn app.main:app --reload` - Start development server with auto-reload
- `docker-compose up` - Start PostgreSQL database service
- `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000` - Production server

### Testing
- `uv run pytest` - Run all tests
- `uv run pytest tests/test_specific.py` - Run specific test file
- `uv run pytest -v` - Run tests with verbose output
- `uv run pytest --cov=app` - Run tests with coverage report
- `uv run pytest tests/test_specific.py::test_function_name` - Run specific test

### Database Operations
- `uv run alembic upgrade head` - Apply database migrations
- `uv run alembic revision --autogenerate -m "description"` - Generate new migration
- `uv run alembic downgrade -1` - Rollback one migration

### Dependencies
- `uv add package_name` - Add production dependency
- `uv add --dev package_name` - Add development dependency
- `uv sync` - Install dependencies from lockfile

## Architecture Overview

### Project Structure
This is a FastAPI-based web application with the following architecture:

**Core Components:**
- `app/main.py` - FastAPI application entry point
- `app/core/` - Core configuration, database, and security modules
- `app/models.py` - SQLAlchemy ORM models (centralized)
- `app/schemas/` - Pydantic models for request/response validation
- `app/services/` - Business logic layer
- `app/api/` - API routing and endpoint definitions

**Key Models:**
- User, Post, Drawing, Image, Comment with soft deletion support
- All models use nanoid-generated `code` fields as public identifiers
- Relationships handle soft deletion via `deleted_at` filters

### Authentication & Authorization
- JWT-based authentication using Bearer tokens
- OAuth integration with Google and Apple
- User roles: regular users and admins
- Auth dependency injection via `CurrentUserDep` and `DatabaseDep`

### Database Architecture
- PostgreSQL with SQLAlchemy ORM
- Alembic for migrations
- Soft deletion pattern (deleted_at field)
- Foreign key relationships with proper cascading

#### Soft Delete Pattern
All models implement soft deletion using a `deleted_at` timestamp field:
- Records are never physically deleted from the database
- Deletion sets `deleted_at` to the current timestamp
- All queries automatically filter out soft-deleted records using `deleted_at IS NULL`
- Relationships use `primaryjoin` conditions to exclude soft-deleted related records
- This pattern preserves data integrity and allows for audit trails
- Example: `primaryjoin=lambda: and_(Post.id == Drawing.post_id, Drawing.deleted_at.is_(None))`

### Testing Strategy
- pytest with testcontainers for isolated testing
- Separate test database using PostgreSQL container
- LocalStack for AWS S3 testing
- Fixtures for common test data (users, authentication)
- Coverage reporting with pytest-cov

### File Upload & Storage
- AWS S3 integration for file storage
- Profile images and drawing images
- Environment-based configuration for different deployment targets

### Key Patterns
- Service layer pattern separating business logic from API routes
- Dependency injection for database sessions and current user
- Pydantic schemas for request/response validation
- Centralized configuration using pydantic-settings
- Error handling with appropriate HTTP status codes

### Environment Configuration
The application uses environment variables for configuration:
- Database connection (POSTGRES_*)
- JWT secret key
- AWS S3 credentials
- OAuth provider credentials (Google, Apple)

Always ensure `.env` file is properly configured for local development.
