"""
run with command:

pytest --tb=no tests/test_conjugations.py -v -s

"""
import pytest
import json
import sys
import os
from pprint import pprint
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_test_header(request_data):
    print("\n\n")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*100}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}Test Case: {request_data['infinitive']}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'-'*100}{Colors.ENDC}")
    
    print(f"{Colors.BLUE}Parameters:{Colors.ENDC}")
    for key, value in request_data.items():
        if key != 'infinitive':
            print(f"  {key:<15} : {value}")
    print(f"{Colors.HEADER}{'-'*100}{Colors.ENDC}")

@pytest.mark.parametrize("log", json.load(open('valid_responses.json')))
def test_cleaned_logs(log, capsys):
    with capsys.disabled():
        request_data = log['request']
        expected_response = log['response']
        header_printed = False

        # Prepare and execute request
        query_string = '&'.join(f"{key}={value}" for key, value in request_data.items())
        response = app.test_client().get(f'/api/conjugate?{query_string}')
        
        # Verify response status and show error details if failed
        if response.status_code != 200:
            if not header_printed:
                print_test_header(request_data)
                header_printed = True

            try:
                response_data = json.loads(response.data)
                if isinstance(response_data, dict):
                    error_message = (response_data.get('response', {}).get('error') or 
                                   response_data.get('error') or 
                                   response.data.decode('utf-8'))
                else:
                    error_message = str(response_data)
            except json.JSONDecodeError:
                error_message = response.data.decode('utf-8')
            except Exception as e:
                error_message = str(e)

            print(f"\n{Colors.RED}Server Error ({response.status_code}):{Colors.ENDC}")
            print(f"  {error_message}")
            print()
            assert False, f"Request failed with status {response.status_code}: {error_message}"
        
        response_data = json.loads(response.data)

        # Verify response structure
        response_key = next((key for key in expected_response if key in response_data), None)
        assert response_key is not None, (
            f"Expected key not found in response.\n"
            f"Expected one of: {list(expected_response.keys())}\n"
            f"Got: {list(response_data.keys())}"
        )

        # Compare results
        expected_forms = sorted(expected_response[response_key])
        actual_forms = sorted(response_data[response_key])

        if expected_forms != actual_forms:
            if not header_printed:
                print_test_header(request_data)
                header_printed = True

            print(f"\n{Colors.BOLD}Results Comparison:{Colors.ENDC}")
            print(f"Dialect: {response_key}")
            print(f"{Colors.HEADER}{'-'*100}{Colors.ENDC}")

            # Calculate differences
            expected_set = set(expected_forms)
            actual_set = set(actual_forms)
            missing = sorted(expected_set - actual_set)
            extra = sorted(actual_set - expected_set)
            matching = sorted(expected_set & actual_set)

            # Display differences side by side
            if missing or extra:
                print("\nDifferences:")
                print(f"{Colors.RED}Missing{Colors.ENDC}                              {Colors.YELLOW}Unexpected{Colors.ENDC}")
                print("-" * 75)
                
                max_len = max(len(missing) if missing else 0, len(extra) if extra else 0)
                for i in range(max_len):
                    left = f"- {missing[i]}" if i < len(missing) else ""
                    right = f"+ {extra[i]}" if i < len(extra) else ""
                    print(f"{Colors.RED}{left:<35}{Colors.ENDC} {Colors.YELLOW}{right}{Colors.ENDC}")

            # Display matching conjugations
            if matching:
                print(f"\n{Colors.GREEN}Matching Conjugations:{Colors.ENDC}")
                col_width = max(len(word) for word in matching) + 2
                num_cols = 3
                
                for i in range(0, len(matching), num_cols):
                    row = matching[i:i + num_cols]
                    formatted_row = "".join(f"✓ {item:<{col_width}}" for item in row)
                    print(f"{Colors.GREEN}{formatted_row}{Colors.ENDC}")

            # Show comparison in two columns
            if len(expected_forms) == len(actual_forms):
                print(f"\n{Colors.BLUE}Detailed Comparison:{Colors.ENDC}")
                
                # Split comparisons into two columns
                mismatches = [(exp, act) for exp, act in zip(expected_forms, actual_forms) if exp != act]
                half_len = (len(mismatches) + 1) // 2
                col_width = 50  # Adjust this value based on your needs
                
                for i in range(half_len):
                    # Left column
                    left_exp, left_act = mismatches[i]
                    left_col = (
                        f"{Colors.RED}Expected:{Colors.ENDC} {left_exp}\n"
                        f"{Colors.YELLOW}Actual  :{Colors.ENDC} {left_act}"
                    )
                    
                    # Right column (if exists)
                    right_col = ""
                    if i + half_len < len(mismatches):
                        right_exp, right_act = mismatches[i + half_len]
                        right_col = (
                            f"{Colors.RED}Expected:{Colors.ENDC} {right_exp}\n"
                            f"{Colors.YELLOW}Actual  :{Colors.ENDC} {right_act}"
                        )
                    
                    # Print both columns
                    left_lines = left_col.split('\n')
                    right_lines = right_col.split('\n') if right_col else ['', '']
                    
                    for left_line, right_line in zip(left_lines, right_lines):
                        print(f"  {left_line:<{col_width}}    {right_line}")
                    print()

            print()

            assert expected_forms == actual_forms, (
                f"\nConjugation mismatch for {request_data['infinitive']} "
                f"in dialect {response_key}"
            )