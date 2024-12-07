import json
import os

def generate_test_cases():
    # Read the log file
    with open('request_response.log', 'r', encoding='utf-8') as f:
        log_content = f.read()
    
    # Parse log entries into test cases
    test_cases = []
    for line in log_content.split('\n'):
        if not line.strip():
            continue
        
        try:
            # Extract JSON part after timestamp more carefully
            parts = line.split(' - ', 1)  # Split only on first occurrence
            if len(parts) != 2:
                continue
                
            json_str = parts[1]
            log_data = json.loads(json_str)
            
            if log_data['endpoint'] == '/api/conjugate':
                test_case = {
                    'name': f"{log_data['request'].get('infinitive', 'unknown')}_{log_data['request'].get('tense', '')}_"
                           f"{log_data['request'].get('aspect', '')}_{log_data['request'].get('obj', 'no_obj')}",
                    'input': log_data['request'],
                    'expected_output': log_data['response']
                }
                test_cases.append(test_case)
        except Exception as e:
            print(f"Failed to parse line: {str(e)}")
            continue
    
    # Print some statistics
    verbs = set(case['input'].get('infinitive') for case in test_cases)
    print(f"\nFound {len(test_cases)} test cases")
    print(f"Testing {len(verbs)} unique verbs: {sorted(verbs)}\n")
    
    # Generate test file content
    test_file_content = '''import pytest
from flask import url_for
import json

# Test cases generated from request_response.log
test_cases = {test_cases}

@pytest.fixture
def client():
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize("test_case", test_cases, 
                        ids=lambda tc: tc['name'])
def test_conjugations(client, test_case):
    """Test conjugation with parameters from log data"""
    # Make request
    response = client.get('/api/conjugate', query_string=test_case["input"])
    
    # Check status code
    assert response.status_code == 200
    
    # Parse response
    result = json.loads(response.data)
    
    # Compare with expected output
    assert result == test_case["expected_output"], f"""
    Failed test case:
    Input: {{test_case['input']}}
    Expected: {{test_case['expected_output']}}
    Got: {{result}}
    """

def test_invalid_verb(client):
    """Test behavior with invalid verb"""
    response = client.get('/api/conjugate', query_string={{
        "infinitive": "invalidverb",
        "subject": "all",
        "tense": "present"
    }})
    assert response.status_code == 404
    result = json.loads(response.data)
    assert "error" in result

def test_invalid_input(client):
    """Test behavior with missing required parameters"""
    response = client.get('/api/conjugate', query_string={{
        "infinitive": "ot̆axu"  # Missing required parameters
    }})
    assert response.status_code == 400
    result = json.loads(response.data)
    assert "error" in result

def test_special_verb_restrictions(client):
    """Test special verbs that cannot take objects"""
    special_verbs = ["coxons", "cozun", "gyožin"]
    
    for verb in special_verbs:
        response = client.get('/api/conjugate', query_string={{
            "infinitive": verb,
            "subject": "all",
            "obj": "O2_Singular",
            "tense": "present"
        }})
        assert response.status_code == 400
        result = json.loads(response.data)
        assert "error" in result
        assert "cannot have an object" in result["error"]
'''.format(test_cases=json.dumps(test_cases, indent=4, ensure_ascii=False))

    # Write the test file
    with open('test_conjugator.py', 'w', encoding='utf-8') as f:
        f.write(test_file_content)

    print("Generated test_conjugator.py")

if __name__ == '__main__':
    generate_test_cases()