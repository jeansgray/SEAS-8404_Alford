# Summary Report: Secure Containerized Flask Application

## 1. Steps Taken

The project involved securing a deliberately vulnerable Python Flask web application running in a Docker container. The following steps were performed:

- Reviewed `app.py`, `Dockerfile`, and `docker-compose.yml` to understand the insecure implementation.
- Executed manual scans using **Bandit**, **pip-audit**, and **Docker Bench for Security** to identify code and configuration issues.
- Demonstrated insecure behavior through the `/ping` and `/calculate` endpoints.
- Remediated code vulnerabilities manually, then automated configuration fixes using a Python hardening script.
- Created a threat model using STRIDE and MITRE ATT&CK for Containers.
- Documented controls using NIST 800-53 mappings and created a secure deployment architecture diagram.
- Re-ran security scans to confirm that all major vulnerabilities were mitigated.

---

## 2. Vulnerabilities Found and Fixed

| Category                | Vulnerability                                   | Fix Implemented                                  |
|-------------------------|-------------------------------------------------|--------------------------------------------------|
| Code Injection          | Use of `eval()` in `/calculate`                | Replaced with `ast.literal_eval()`               |
| Command Injection       | Subprocess shell command in `/ping`            | Added input validation with regex                |
| Credential Disclosure   | Hardcoded password string                      | Replaced with `os.environ.get()`                 |
| Insecure Defaults       | Flask bound to all interfaces (`0.0.0.0`)      | Restricted to `127.0.0.1`                        |
| Container Privilege     | Lack of health checks and privilege controls   | Added `HEALTHCHECK`, `USER`, and `security_opt`  |
| Resource Abuse Potential| No resource limits in Compose config           | Added `read_only`, `mem_limit`, and `pids_limit` |

---

## 3. Architecture and How It Improves Security

The final hardened architecture separates services and applies the **principle of least privilege** across the application and container stack.

**Key Architecture Enhancements:**

- **Secure Flask App**: Inputs are validated, eval is removed, and secrets are externalized.
- **Hardened Dockerfile**: Uses a minimal base image, runs as non-root, and includes a health check.
- **Restricted Network Exposure**: Docker Compose binds services to localhost instead of exposing them globally.
- **Runtime Protections**: `docker-compose.yml` now enforces memory and process limits and blocks privilege escalation.
- **Auto-Hardening Script**: Ensures repeatable, consistent security configuration for all future builds.

These improvements significantly reduce the application’s attack surface and improve its resilience to common web and container threats.

---

## 4. Reflection on Lessons Learned

This exercise demonstrated how insecure code and misconfigured containers can create real security risks, even in simple applications. It reinforced several key security engineering practices:

- **Secure by Default**: It’s easier to build security in from the start than patch it later.
- **Automation is Critical**: Repeating manual fixes is error-prone. Automating with a hardening script ensures consistency and reduces effort.
- **Defense in Depth**: Applying validation in the app, constraints in the container, and controls in the infrastructure builds a layered defense.
- **Threat Modeling is Actionable**: Using STRIDE and MITRE ATT&CK helped guide control implementation, showing how vulnerabilities map to real-world attack techniques.

Overall, the project emphasized the importance of combining secure development, secure configuration, and automated tooling for scalable security.

