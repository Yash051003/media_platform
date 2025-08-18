# tests/test_auth.py
def test_create_and_login_user(client):
    """
    Tests the full signup, login, and protected route access flow.
    The 'client' fixture is automatically provided by conftest.py.
    """
    # --- Test Signup ---
    signup_response = client.post(
        "/auth/signup",
        json={"email": "testuser@example.com", "password": "testpassword"},
    )
    assert signup_response.status_code == 201, signup_response.text
    data = signup_response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data

    # --- Test Login ---
    login_response = client.post(
        "/auth/login",
        json={"email": "testuser@example.com", "password": "testpassword"},
    )
    assert login_response.status_code == 200, login_response.text
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    access_token = token_data["access_token"]

    # --- Test Protected Route ---
    headers = {"Authorization": f"Bearer {access_token}"}
    me_response = client.get("/auth/users/me", headers=headers)
    
    assert me_response.status_code == 200, me_response.text
    user_data = me_response.json()
    assert user_data["email"] == "testuser@example.com"