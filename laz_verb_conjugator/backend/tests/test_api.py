# test_api.py

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

def test_api_status_codes():
    # Test basic endpoint availability
    response = app.test_client().get('/api/verbs')
    assert response.status_code == 200
    
    # Test missing required parameters
    response = app.test_client().get('/api/conjugate')
    assert response.status_code == 400
    
    # Test invalid verb
    response = app.test_client().get('/api/conjugate?infinitive=nonexistent&subject=all&tense=present')
    assert response.status_code == 404

def test_response_structure():
    # Test response format and structure
    response = app.test_client().get('/api/conjugate?infinitive=ot̆axu&subject=all&tense=present')
    data = response.json
    
    assert isinstance(data, dict)
    assert any(key in data for key in ['FA', 'AŞ', 'PZ', 'HO'])
    
    for dialect, conjugations in data.items():
        assert isinstance(conjugations, list)
        for conj in conjugations:
            assert ' : ' in conj

def test_region_filtering():
    # Test region filter parameter
    response = app.test_client().get('/api/conjugate?infinitive=ot̆axu&subject=all&tense=present&region=HO')
    data = response.json
    
    assert len(data) == 1
    assert 'HO' in data

def test_parameter_validation():
    # Test verb restrictions
    response = app.test_client().get('/api/conjugate?infinitive=coxons&subject=all&obj=O2_Singular&tense=present')
    assert response.status_code == 400
    assert "cannot have an object" in response.json.get('error', '')
    
    # Test imperative restrictions
    response = app.test_client().get('/api/conjugate?infinitive=ot̆axu&subject=S1_Singular&imperative=true')
    assert response.status_code == 400
    assert "Imperatives are only available for" in response.json.get('error', '')