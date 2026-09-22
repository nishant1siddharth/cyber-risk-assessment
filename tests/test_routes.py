def test_unauthenticated_access(client):
    response = client.get('/dashboard')
    # Should redirect to login
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

    response = client.get('/business/')
    assert response.status_code == 302

    response = client.get('/assets/')
    assert response.status_code == 302
    
    response = client.get('/assessment/new')
    assert response.status_code == 302
