import pytest
import json
import sys
import os
from pprint import pprint
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

@pytest.mark.parametrize("log", json.load(open('valid_responses.json')))
def test_cleaned_logs(log):
    request_data = log['request']
    expected_response = log['response']

    # Print info about the current test case
    print("\n" + "="*80)
    print(f"Testing conjugation for: {request_data['infinitive']}")
    print(f"Parameters:")
    for key, value in request_data.items():
        if key != 'infinitive':
            print(f"  {key}: {value}")

    # Convert request_data into query parameters
    query_string = '&'.join(f"{key}={value}" for key, value in request_data.items())
    
    # Simulate the GET request
    response = app.test_client().get(f'/api/conjugate?{query_string}')
    
    # Check response status
    assert response.status_code == 200, f"Request failed with status {response.status_code}"
    
    response_data = json.loads(response.data)
    
    # Find the correct key in the response
    response_key = next((key for key in expected_response if key in response_data), None)
    assert response_key is not None, (
        f"Expected key not found in the response.\n"
        f"Expected one of: {list(expected_response.keys())}\n"
        f"Got: {list(response_data.keys())}"
    )

    # Compare the sorted lists and show detailed diff if they don't match
    expected_forms = sorted(expected_response[response_key])
    actual_forms = sorted(response_data[response_key])
    
    if expected_forms != actual_forms:
        print("\nMismatches found:")
        print(f"\nDialect: {response_key}")
        
        # Find differences
        expected_set = set(expected_forms)
        actual_set = set(actual_forms)
        
        missing = expected_set - actual_set
        extra = actual_set - expected_set
        
        if missing:
            print("\nMissing conjugations (expected but not found):")
            for form in sorted(missing):
                print(f"  {form}")
        
        if extra:
            print("\nExtra conjugations (found but not expected):")
            for form in sorted(extra):
                print(f"  {form}")
                
        # Show matching forms for context
        print("\nMatching conjugations:")
        for form in sorted(expected_set & actual_set):
            print(f"  {form}")
            
        # If lists have same length, show direct comparison
        if len(expected_forms) == len(actual_forms):
            print("\nDirect comparison:")
            for exp, act in zip(expected_forms, actual_forms):
                if exp != act:
                    print(f"  Expected: {exp}")
                    print(f"  Got:      {act}")
                    print(f"  Diff pos: {''.join(' ' if e == a else '^' for e, a in zip(exp, act))}")
                    print()

    assert expected_forms == actual_forms, (
        f"\nConjugation mismatch for {request_data['infinitive']} in dialect {response_key}"
    )