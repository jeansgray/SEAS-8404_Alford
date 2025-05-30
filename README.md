# IAM Architecture with Keycloak and Flask

This project implements a secure IAM (Identity and Access Management) architecture using Keycloak for authentication and authorization, with a Flask application serving as the protected API.

## Architecture Overview

The system consists of three main components:
1. Keycloak - Identity and Access Management server
2. PostgreSQL - Database for Keycloak
3. Flask Application - Protected API with token validation

## Prerequisites

- Docker and Docker Compose
- Python 3.9 or higher
- Make (optional, but recommended)

## Setup Instructions

1. Clone the repository
2. Start the services:
   ```bash
   make up
   ```
3. Configure Keycloak:
   ```bash
   make configure
   ```

## Available Commands

- `make up` - Start all services
- `make down` - Stop all services
- `make reset` - Reset everything (including volumes) and reconfigure
- `make configure` - Configure Keycloak (realm, client, users)
- `make test` - Run basic API tests

## API Endpoints

- `GET /api/public` - Public endpoint (no authentication required)
- `GET /api/protected` - Protected endpoint (requires valid JWT token)
- `GET /api/admin` - Admin endpoint (requires admin role)

## Default Users

- Regular user:
  - Username: testuser
  - Password: password
- Admin user:
  - Username: admin
  - Password: admin

## Security Features

1. JWT Token Validation
2. Role-based Access Control
3. Secure Password Storage
4. CORS Protection
5. Environment Variable Configuration

## Testing the API

1. Get a token from Keycloak:
   ```bash
   curl -X POST http://localhost:8080/realms/myrealm/protocol/openid-connect/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=password" \
     -d "client_id=flask-app" \
     -d "username=testuser" \
     -d "password=password"
   ```

2. Use the token to access protected endpoints:
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:5000/api/protected
   ```

## Security Considerations

1. All sensitive data is stored in environment variables
2. JWT tokens are validated using Keycloak's public keys
3. Role-based access control is implemented
4. CORS is properly configured
5. Passwords are securely stored in Keycloak

## Troubleshooting

If you encounter any issues:

1. Check if all services are running:
   ```bash
   docker-compose ps
   ```

2. View service logs:
   ```bash
   docker-compose logs
   ```

3. Reset the environment:
   ```bash
   make reset
   ``` 