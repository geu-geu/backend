# GeuGeu Development Checklist

## 🎯 Project Overview
A mobile platform connecting people who want drawings with artists who can create them.

## ✅ Completed Features

### Core Infrastructure
- [x] FastAPI application setup
- [x] PostgreSQL database with Docker Compose
- [x] SQLAlchemy ORM models
- [x] Alembic migrations
- [x] Environment configuration with pydantic-settings
- [x] Soft deletion pattern implementation
- [x] Nanoid-based code generation for public IDs

### Authentication & Authorization
- [x] JWT-based authentication with Bearer tokens
- [x] User registration and login
- [x] OAuth integration (Google and Apple)
- [x] CurrentUserDep dependency injection
- [x] Password hashing with bcrypt

### User Management
- [x] User model with multiple auth providers (LOCAL, GOOGLE, APPLE)
- [x] User profile endpoints
- [x] Profile image upload to S3

### Posts (Drawing Requests)
- [x] Create, read, update, delete posts
- [x] Post listing with pagination
- [x] Post filtering (recent, popular)
- [x] Image attachments for posts

### Drawings (Artist Submissions)
- [x] Submit drawings to posts
- [x] Drawing listing with pagination
- [x] Drawing filtering (recent, popular)
- [x] Image attachments for drawings
- [x] Link drawings to specific posts

### Comments System
- [x] Comments on posts
- [x] Comments on drawings
- [x] Nested comments (parent-child relationships)
- [x] Comment CRUD operations

### File Storage
- [x] AWS S3 integration
- [x] Image upload endpoints
- [x] File validation
- [x] Secure presigned URLs

### Testing Infrastructure
- [x] pytest setup with testcontainers
- [x] Test fixtures for users and authentication
- [x] LocalStack for S3 testing
- [x] Test coverage configuration

## 🚧 In Progress Features

### Interest/Hand Raise System ("관심있어요")
- [ ] Create Interest model
- [ ] Add interest endpoints (add/remove interest)
- [ ] Count interests on posts
- [ ] List users who expressed interest
- [ ] Check if current user has expressed interest

## 📋 TODO Features

### Gallery & Display Features
- [ ] Gallery endpoint for all drawings across posts
- [ ] User's drawings collection in profile
- [ ] Drawing count aggregation on posts
- [ ] Grid view support for drawings

### Business Rules
- [ ] Implement one drawing per user per post limitation
- [ ] Add validation to prevent duplicate submissions

### API Enhancements
- [ ] Add relative time formatting utility
- [ ] Implement sorting options for lists
- [ ] Add search functionality for posts
- [ ] Add search functionality for drawings
- [ ] Implement user blocking/reporting

### Performance Optimizations
- [ ] Add database indexes for common queries
- [ ] Implement caching strategy
- [ ] Optimize N+1 queries with eager loading
- [ ] Add query result pagination metadata

### Admin Features
- [ ] Admin dashboard endpoints
- [ ] Content moderation tools
- [ ] User management (ban/unban)
- [ ] Analytics endpoints

### Notification System
- [ ] Notification model
- [ ] Push notification integration
- [ ] Email notifications
- [ ] In-app notification endpoints

## 🐛 Known Issues
- [ ] None currently documented

## 🔧 Technical Debt
- [ ] Add comprehensive API documentation
- [ ] Improve error handling consistency
- [ ] Add request/response logging
- [ ] Implement rate limiting
- [ ] Add API versioning strategy

## 📊 Testing Goals
- [ ] Achieve 80%+ test coverage
- [ ] Add integration tests for complex workflows
- [ ] Add performance tests
- [ ] Add security tests

## 🚀 Deployment Preparation
- [ ] Create production Dockerfile
- [ ] Setup CI/CD pipeline
- [ ] Configure production environment variables
- [ ] Setup monitoring and logging
- [ ] Create deployment documentation

## 📝 Documentation
- [ ] API documentation with examples
- [ ] Deployment guide
- [ ] Contributing guide
- [ ] Architecture decision records (ADRs)

---

Last Updated: 2025-07-11
