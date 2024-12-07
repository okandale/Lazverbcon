import pytest
import json
from app import app

@pytest.mark.parametrize("log", json.load(open('valid_responses.json')))
def test_cleaned_logs(log):
    request_data = log['request']
    expected_response = log['response']
    
    # Convert request_data into query parameters (assuming it's a dict)
    query_string = '&'.join(f"{key}={value}" for key, value in request_data.items())
    
    # Simulate the GET request
    response = app.test_client().get(f'/api/conjugate?{query_string}')
    
    # Compare the simulated output to the expected output
    assert response.status_code == 200
    response_data = json.loads(response.data)

    # Find the correct key in the response (either 'HO' or 'PZ')
    response_key = next((key for key in expected_response if key in response_data), None)

    assert response_key is not None, "Expected key not found in the response"

    # Compare the sorted lists for the found key
    assert sorted(response_data[response_key]) == sorted(expected_response[response_key])
