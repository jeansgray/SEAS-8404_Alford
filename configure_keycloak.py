import requests
import time
import json

KEYCLOAK_URL = "http://localhost:8080"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"
REALM_NAME = "myrealm"
CLIENT_ID = "flask-app"
CLIENT_SECRET = "your-client-secret"

def get_admin_token():
    response = requests.post(
        f"{KEYCLOAK_URL}/realms/master/protocol/openid-connect/token",
        data={
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        }
    )
    return response.json()["access_token"]

def create_realm(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    realm_data = {
        "realm": REALM_NAME,
        "enabled": True
    }
    
    response = requests.post(
        f"{KEYCLOAK_URL}/admin/realms",
        headers=headers,
        json=realm_data
    )
    return response.status_code == 201

def create_client(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    client_data = {
        "clientId": CLIENT_ID,
        "secret": CLIENT_SECRET,
        "redirectUris": ["http://localhost:5000/*"],
        "webOrigins": ["http://localhost:5000"],
        "publicClient": False,
        "directAccessGrantsEnabled": True,
        "standardFlowEnabled": True
    }
    
    response = requests.post(
        f"{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/clients",
        headers=headers,
        json=client_data
    )
    return response.status_code == 201

def create_user(token, username, password, email):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    user_data = {
        "username": username,
        "email": email,
        "enabled": True,
        "credentials": [{
            "type": "password",
            "value": password,
            "temporary": False
        }]
    }
    
    response = requests.post(
        f"{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/users",
        headers=headers,
        json=user_data
    )
    return response.status_code == 201

def main():
    print("Waiting for Keycloak to start...")
    time.sleep(30)  # Wait for Keycloak to be ready
    
    try:
        token = get_admin_token()
        print("Got admin token")
        
        if create_realm(token):
            print(f"Created realm: {REALM_NAME}")
        
        if create_client(token):
            print(f"Created client: {CLIENT_ID}")
        
        if create_user(token, "testuser", "password", "test@example.com"):
            print("Created test user")
        
        if create_user(token, "admin", "admin", "admin@example.com"):
            print("Created admin user")
        
        print("Keycloak configuration completed successfully!")
        
    except Exception as e:
        print(f"Error during configuration: {str(e)}")

if __name__ == "__main__":
    main()