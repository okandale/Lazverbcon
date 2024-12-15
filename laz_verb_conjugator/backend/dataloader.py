import json

def load_ivd_verbs():
    """Load IVD (Intransitive Verbs) data from JSON file."""
    with open('data/verb_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter for IVD verbs only
    df_ivd = [row for row in data if row['Category'] == 'IVD']
    
    verbs = {}
    regions = {}
    
    for row in df_ivd:
        infinitive = row['Laz Infinitive']
        
        # Get present forms (maintaining pandas-like behavior)
        present_forms = []
        for key in ['Laz 3rd Person Singular Present', 
                   'Laz 3rd Person Singular Present Alternative 1', 
                   'Laz 3rd Person Singular Present Alternative 2']:
            if row.get(key):  # Handle None/null values like pandas
                present_forms.append(row[key])
        
        # Get regions (split and clean like pandas would)
        region_data = []
        for key in ['Region', 'Region Alternative 1', 'Region Alternative 2']:
            if row.get(key):
                region_data.append(row[key])
        
        # Process regions into list, similar to pandas str.split()
        regions_list = []
        for reg in region_data:
            if reg:
                regions_list.extend([r.strip() for r in reg.split(',')])
        
        if not regions_list:
            regions_list = ["All"]
        
        verbs[infinitive] = list(zip(present_forms, region_data))
        regions[infinitive] = regions_list

    return verbs, regions

def load_tve_verbs():
    """Load TVE (Transitive Verbs) data from JSON file."""
    with open('data/verb_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter for TVE verbs
    df_tve = [row for row in data if row['Category'] == 'TVE']
    
    verbs = {}
    regions = {}
    co_verbs = []
    gyo_verbs = []
    
    for row in df_tve:
        infinitive = row['Laz Infinitive']
        
        present_forms = []
        for key in ['Laz 3rd Person Singular Present', 
                   'Laz 3rd Person Singular Present Alternative 1', 
                   'Laz 3rd Person Singular Present Alternative 2']:
            if row.get(key):
                present_forms.append(row[key])
        
        # Check for co- and gyo- prefixes
        if any(form and form.startswith('co') for form in present_forms):
            co_verbs.append(infinitive)
        if any(form and form.startswith('gyo') for form in present_forms):
            gyo_verbs.append(infinitive)
        
        region_data = []
        for key in ['Region', 'Region Alternative 1', 'Region Alternative 2']:
            if row.get(key):
                region_data.append(row[key])
        
        regions_list = []
        for reg in region_data:
            if reg:
                regions_list.extend([r.strip() for r in reg.split(',')])
        
        if not regions_list:
            regions_list = ["All"]
        
        verbs[infinitive] = list(zip(present_forms, region_data))
        regions[infinitive] = regions_list

    return verbs, regions, co_verbs, gyo_verbs

def load_tvm_tense():
    """Load TVM (Middle Voice) tense data from JSON file."""
    with open('data/verb_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter for TVM verbs
    df_tvm = [row for row in data if row['Category'] == 'TVM']
    
    verbs = {}
    regions = {}
    
    for row in df_tvm:
        infinitive = row['Laz Infinitive']
        
        verb_forms = []
        for key in ['Laz 3rd Person Singular Present', 
                   'Laz 3rd Person Singular Present Alternative 1', 
                   'Laz 3rd Person Singular Present Alternative 2']:
            if row.get(key):
                verb_forms.append(row[key])
        
        region_data = []
        for key in ['Region', 'Region Alternative 1', 'Region Alternative 2']:
            if row.get(key):
                region_data.append(row[key])
        
        regions_list = []
        for reg in region_data:
            if reg:
                regions_list.extend([r.strip() for r in reg.split(',')])
        
        if not regions_list:
            regions_list = ["All"]
        
        verbs[infinitive] = list(zip(verb_forms, region_data))
        regions[infinitive] = regions_list

    return verbs, regions

def load_tvm_tve_passive():
    """Load TVM and TVE passive forms from JSON file."""
    with open('data/verb_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter for both TVE and TVM verbs
    df_tve = [row for row in data if row['Category'] in ['TVE', 'TVM']]
    
    verbs = {}
    regions = {}
    
    for row in df_tve:
        infinitive = row['Laz Infinitive']
        
        passive_forms = []
        for key in ['Laz 3rd Person Singular Present', 
                   'Laz 3rd Person Singular Present Alternative 1', 
                   'Laz 3rd Person Singular Present Alternative 2']:
            if row.get(key):
                passive_forms.append(row[key])
        
        region_data = []
        for key in ['Region', 'Region Alternative 1', 'Region Alternative 2']:
            if row.get(key):
                region_data.append(row[key])
        
        regions_list = []
        for reg in region_data:
            if reg:
                regions_list.extend([r.strip() for r in reg.split(',')])
        
        if not regions_list:
            regions_list = ["All"]
        
        verbs[infinitive] = list(zip(passive_forms, region_data))
        regions[infinitive] = regions_list

    return verbs, regions

def load_tvm_tve_potential():
    """Load TVM and TVE potential forms from JSON file."""
    with open('data/verb_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter for both TVE and TVM verbs
    df_tve = [row for row in data if row['Category'] in ['TVE', 'TVM']]
    
    verbs = {}
    regions = {}
    
    for row in df_tve:
        infinitive = row['Laz Infinitive']
        
        potential_forms = []
        for key in ['Laz 3rd Person Singular Present', 
                   'Laz 3rd Person Singular Present Alternative 1', 
                   'Laz 3rd Person Singular Present Alternative 2']:
            if row.get(key):
                potential_forms.append(row[key])
        
        region_data = []
        for key in ['Region', 'Region Alternative 1', 'Region Alternative 2']:
            if row.get(key):
                region_data.append(row[key])
        
        regions_list = []
        for reg in region_data:
            if reg:
                regions_list.extend([r.strip() for r in reg.split(',')])
        
        if not regions_list:
            regions_list = ["All"]
        
        verbs[infinitive] = list(zip(potential_forms, region_data))
        regions[infinitive] = regions_list

    return verbs, regions

def load_tvm_tve_presentperf():
    """Load TVM and TVE present perfect forms from JSON file."""
    with open('data/verb_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter for both TVE and TVM verbs
    df_tve = [row for row in data if row['Category'] in ['TVE', 'TVM']]
    
    verbs = {}
    regions = {}
    
    for row in df_tve:
        infinitive = row['Laz Infinitive']
        
        present_perfect_forms = []
        for key in ['Laz 3rd Person Singular Present', 
                   'Laz 3rd Person Singular Present Alternative 1', 
                   'Laz 3rd Person Singular Present Alternative 2']:
            if row.get(key):
                present_perfect_forms.append(row[key])
        
        region_data = []
        for key in ['Region', 'Region Alternative 1', 'Region Alternative 2']:
            if row.get(key):
                region_data.append(row[key])
        
        regions_list = []
        for reg in region_data:
            if reg:
                regions_list.extend([r.strip() for r in reg.split(',')])
        
        if not regions_list:
            regions_list = ["All"]
        
        verbs[infinitive] = list(zip(present_perfect_forms, region_data))
        regions[infinitive] = regions_list

    return verbs, regions