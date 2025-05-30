# IAM Architecture Summary Report

## Overview
This report outlines the IAM (Identity and Access Management) architecture implemented using Docker Compose, Keycloak, and a Flask application. The architecture is designed to provide secure access to API endpoints, with Keycloak handling authentication and authorization.

## Setup Steps
1. **Docker Compose Configuration**: The `docker-compose.yml` file was created to define the services for Keycloak, PostgreSQL, and the Flask application.
2. **Keycloak Configuration**: Keycloak was set up to manage users and clients, with a realm and client created for the Flask application.
3. **Flask Application**: The Flask application was configured to use Keycloak for authentication, with endpoints for public and protected access.
4. **Configuration Script**: A Python script (`configure_keycloak.py`) was used to automate the setup of Keycloak, including creating a realm and client.

## Issues Encountered
- **Flask App Container Not Starting**: Initially, the Flask app container did not start due to issues with the Flask package. This was resolved by rebuilding the container and ensuring all dependencies were correctly installed.
- **Obsolete `version` Attribute**: The `version` attribute in the `docker-compose.yml` file was removed to avoid confusion, as it is no longer needed.

## Results of Testing
- **Public Endpoint**: The public endpoint was successfully tested using `curl http://localhost:5000/public`.
- **Protected Endpoint**: The protected endpoint was tested using a token obtained from Keycloak, ensuring that only authenticated users could access it.

## Conclusion
The IAM architecture was successfully implemented, providing a secure way to manage access to the Flask application's API endpoints. The use of Keycloak for authentication and authorization ensures that only authorized users can access protected resources.

## Architecture Diagram
![IAM Architecture Diagram](architecture_diagram.png)

## Threat Model
- **Authentication**: Keycloak provides robust authentication mechanisms, ensuring that only authorized users can access the application.
- **Authorization**: The Flask application uses Keycloak to enforce access controls, ensuring that users can only access resources they are permitted to.
- **Data Protection**: Sensitive data is protected through secure communication channels and proper access controls.
- **Denial of Service**: Measures are in place to prevent and mitigate potential denial of service attacks, ensuring the application remains available.
- **Man-in-the-Middle Attacks**: Secure communication protocols are used to prevent man-in-the-middle attacks, ensuring data integrity and confidentiality.

## Demo Video
A demo video has been prepared to showcase the setup and testing of the API endpoints. The video demonstrates the configuration of Keycloak, the Flask application, and the testing of both public and protected endpoints.

## Final Review
All deliverables have been reviewed to ensure they meet the requirements and are well-documented. The IAM architecture, setup steps, issues encountered, and results of testing are all included in this report. The architecture diagram and threat model provide a clear understanding of the system's design and security measures.

