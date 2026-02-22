from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent          # .../backend
DATA_DIR = BASE_DIR / "data"                        # .../backend/data


def _load_verb_data():
    """Load verb data JSON from backend/data/verb_data.json (stable path)."""
    path = DATA_DIR / "verb_data.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_ivd_verbs():
    """Load IVD (Intransitive Verbs) data from JSON file."""
    data = _load_verb_data()

    # Filter for IVD verbs only
    df_ivd = [row for row in data if row['Category'] == 'IVD']

    verbs = {}
    regions = {}

    for row in df_ivd:
        infinitive = row['Laz Infinitive']

        present_forms = []
        for key in [
            'Laz 3rd Person Singular Present',
            'Laz 3rd Person Singular Present Alternative 1',
            'Laz 3rd Person Singular Present Alternative 2'
        ]:
            if row.get(key):
                present_forms.append(row[key])

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

    return verbs, regions


def load_tve_verbs():
    """Load TVE (Transitive Verbs) data from JSON file."""
    data = _load_verb_data()

    df_tve = [row for row in data if row['Category'] == 'TVE']

    verbs = {}
    regions = {}
    co_verbs = []
    gyo_verbs = []
    no_verbs = []

    def check_prefix_in_words(form, prefix):
        if not form:
            return False
        words = form.split()
        return any(word.startswith(prefix) for word in words)

    for row in df_tve:
        infinitive = row['Laz Infinitive']

        present_forms = []
        for key in [
            'Laz 3rd Person Singular Present',
            'Laz 3rd Person Singular Present Alternative 1',
            'Laz 3rd Person Singular Present Alternative 2'
        ]:
            if row.get(key):
                present_forms.append(row[key])

        if any(form and (check_prefix_in_words(form, 'co') or check_prefix_in_words(form, 'cu'))
               for form in present_forms):
            co_verbs.append(infinitive)
        if any(form and (check_prefix_in_words(form, 'gyo') or check_prefix_in_words(form, 'gyu'))
               for form in present_forms):
            gyo_verbs.append(infinitive)
        if any(form and (check_prefix_in_words(form, 'no') or check_prefix_in_words(form, 'nu') or check_prefix_in_words(form, 'n'))
               for form in present_forms):
            no_verbs.append(infinitive)

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

    return verbs, regions, co_verbs, gyo_verbs, no_verbs


def load_tvm_tense():
    """Load TVM (Middle Voice) tense data from JSON file."""
    data = _load_verb_data()

    df_tvm = [row for row in data if row['Category'] == 'TVM']

    verbs = {}
    regions = {}
    co_verbs = []
    gyo_verbs = []
    no_verbs = []

    def check_prefix_in_words(form, prefix):
        if not form:
            return False
        words = form.split()
        return any(word.startswith(prefix) for word in words)

    for row in df_tvm:
        infinitive = row['Laz Infinitive']

        present_forms = []
        for key in [
            'Laz 3rd Person Singular Present',
            'Laz 3rd Person Singular Present Alternative 1',
            'Laz 3rd Person Singular Present Alternative 2'
        ]:
            if row.get(key):
                present_forms.append(row[key])

        if any(form and check_prefix_in_words(form, 'co') for form in present_forms):
            co_verbs.append(infinitive)
        if any(form and check_prefix_in_words(form, 'gyo') for form in present_forms):
            gyo_verbs.append(infinitive)
        if any(form and (check_prefix_in_words(form, 'no') or check_prefix_in_words(form, 'nu') or check_prefix_in_words(form, 'n'))
               for form in present_forms):
            no_verbs.append(infinitive)

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

    return verbs, regions, co_verbs, gyo_verbs, no_verbs


def load_tvm_tve_passive():
    """Load TVM and TVE passive forms from JSON file."""
    data = _load_verb_data()

    df_tve = [row for row in data if row['Category'] in ['TVE', 'TVM']]

    verbs = {}
    regions = {}

    for row in df_tve:
        infinitive = row['Laz Infinitive']

        passive_forms = []
        for key in [
            'Laz 3rd Person Singular Present',
            'Laz 3rd Person Singular Present Alternative 1',
            'Laz 3rd Person Singular Present Alternative 2'
        ]:
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
    data = _load_verb_data()

    df_tve = [row for row in data if row['Category'] in ['TVE', 'TVM']]

    verbs = {}
    regions = {}

    for row in df_tve:
        infinitive = row['Laz Infinitive']

        potential_forms = []
        for key in [
            'Laz 3rd Person Singular Present',
            'Laz 3rd Person Singular Present Alternative 1',
            'Laz 3rd Person Singular Present Alternative 2'
        ]:
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
    data = _load_verb_data()

    df_tve = [row for row in data if row['Category'] in ['TVE', 'TVM']]

    verbs = {}
    regions = {}

    for row in df_tve:
        infinitive = row['Laz Infinitive']

        present_perfect_forms = []
        for key in [
            'Laz 3rd Person Singular Present',
            'Laz 3rd Person Singular Present Alternative 1',
            'Laz 3rd Person Singular Present Alternative 2'
        ]:
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