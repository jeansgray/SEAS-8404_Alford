# Threat Model: Secure Containerized Microservices

## 1. Overview
This document outlines the threat modeling exercise performed on the initially insecure Flask-based application. The analysis follows STRIDE and MITRE ATT&CK for Containers methodologies and maps mitigation efforts to NIST 800-53 controls.

---

## 2. STRIDE Analysis (Updated)

| Threat Category       | Example                            | Impact                                 | Mitigation                                 |
|------------------------|------------------------------------|----------------------------------------|---------------------------------------------|
| **Spoofing**           | No authentication on `/calculate` | Unauthorized access to logic           | Input validation implemented; auth suggested in future |
| **Tampering**          | Unsafe IP input in `/ping`        | Command injection                      | Regex input validation + removed `shell=True` |
| **Repudiation**        | No logging or user tracking       | Difficult to audit misuse              | Recommend implementing structured logging |
| **Information Disclosure** | Hardcoded passwords          | Secret leakage in code                 | Replaced with `.env` + `os.environ.get()` |
| **Denial of Service**  | Open eval or ping functionality   | CPU/memory exhaustion                  | Input validation + memory & PID limits |
| **Elevation of Privilege** | Root container user (DB)      | Host compromise risk                   | Web container runs as non-root user |

---

## 3. MITRE ATT&CK Mapping (Containers)

| Tactic           | Technique ID | Technique Name                  | Application Relevance                 |
|------------------|--------------|----------------------------------|----------------------------------------|
| **Initial Access** | T1190       | Exploit Public-Facing App        | Command injection via `/ping`          |
| **Execution**     | T1059       | Command & Scripting Interpreter  | Use of `eval()` before remediation     |
| **Persistence**   | T1525       | Implant Container Image          | No image signing or validation         |
| **Privilege Esc.**| T1611       | Escape to Host                   | Root user in DB container (not remediated) |
| **Defense Evasion**| T1211      | Exploitation for Defense Evasion | Incomplete container isolation and defaults |

---

## 4. Controls Mapping (Expanded)

| Issue                      | Fix Implemented                               | Framework Reference                 |
|----------------------------|-----------------------------------------------|--------------------------------------|
| Hardcoded secrets          | Replaced with `.env` + `os.environ.get()`     | **NIST 800-53 SC-12**, **SC-28**     |
| Root container user        | `USER appuser` in Dockerfile                  | **NIST 800-53 AC-6**, **CM-6**       |
| Network binding wide open  | Changed to `127.0.0.1` binding in Flask + Compose | **NIST 800-53 SC-7**             |
| No health check            | `HEALTHCHECK` added in Dockerfile             | **CIS Docker Benchmark**, **SI-4**   |
| Dangerous eval() usage     | Replaced with `ast.literal_eval()`            | **NIST SA-11**, **SI-10**            |
| Command injection          | Removed `shell=True`; added regex input check | **NIST SC-39**, **SI-10**            |
| Resource limits missing    | Added `mem_limit`, `pids_limit`, `read_only`  | **NIST CM-6**, **SC-6**, **SC-39**   |
| Secrets exposed in image   | Used environment variables via `.env`         | **SC-28**, **SC-12**                 |

---

## 5. Risk Rating Summary

| Threat               | Risk     | Likelihood | Impact   | Mitigation Priority |
|----------------------|----------|------------|----------|----------------------|
| Command Injection     | High     | High       | Critical | Immediate            |
| Credential Exposure   | Medium   | High       | Medium   | High                 |
| Eval-based execution  | High     | Medium     | High     | Immediate            |
| Root user in container| High     | Medium     | Critical | High (web fixed; DB pending) |

---

## 6. Conclusion

This threat model highlights key vulnerabilities in the original containerized architecture, including use of `eval`, insecure input handling, hardcoded secrets, and insufficient runtime protections. After remediation, the application now implements least privilege (via non-root user), secure secret handling (via `.env`), input validation, network binding restrictions, and container resource limits. These changes significantly reduce the attack surface and align the deployment with industry best practices and NIST 800-53 controls.
