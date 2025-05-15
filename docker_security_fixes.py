import yaml
import os

print("==== HARDENING: Dockerfile ====")

dockerfile_path = "Dockerfile"
try:
    with open(dockerfile_path, "r") as f:
        lines = f.readlines()

    updated = False
    if not any("USER" in line for line in lines):
        lines.append("\nUSER appuser\n")
        updated = True

    if not any("HEALTHCHECK" in line for line in lines):
        lines.append("HEALTHCHECK CMD wget --spider --quiet localhost:5000 || exit 1\n")
        updated = True

    if updated:
        with open(dockerfile_path, "w") as f:
            f.writelines(lines)
        print( "Dockerfile updated.")
    else:
        print("ℹ Dockerfile already secure.")
except Exception as e:
    print(" Failed to update Dockerfile:", e)


print("\n==== HARDENING: docker-compose.yml ====")

compose_path = "docker-compose.yml"
try:
    with open(compose_path, "r") as f:
        compose = yaml.safe_load(f)

    web = compose.get("services", {}).get("web", {})
    updated = False

    if "read_only" not in web:
        web["read_only"] = True
        updated = True
    if "mem_limit" not in web:
        web["mem_limit"] = "256m"
        updated = True
    if "pids_limit" not in web:
        web["pids_limit"] = 100
        updated = True
    if "security_opt" not in web:
        web["security_opt"] = ["no-new-privileges:true"]
        updated = True

    if updated:
        compose["services"]["web"] = web
        with open(compose_path, "w") as f:
            yaml.dump(compose, f, default_flow_style=False)
        print(" docker-compose.yml updated.")
    else:
        print("ℹ docker-compose.yml already secure.")
except Exception as e:
    print(" Failed to update docker-compose.yml:", e)

