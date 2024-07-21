from flask import Flask, request, jsonify, send_from_directory
import importlib

app = Flask(__name__)

# Loading tense modules
tense_modules = {
    'ivd_present': importlib.import_module('notebooks.ivd_present'),
    'ivd_past': importlib.import_module('notebooks.ivd_past'),
    'ivd_pastpro': importlib.import_module('notebooks.ivd_pastpro'),
    'ivd_future': importlib.import_module('notebooks.ivd_future'),
    'tvm_tve_presentperf': importlib.import_module('notebooks.tvm_tve_presentperf'),
    'tvm_tve_potential': importlib.import_module('notebooks.tvm_tve_potential'),
    'tvm_tve_passive': importlib.import_module('notebooks.tvm_tve_passive'),
    'tvm_tense': importlib.import_module('notebooks.tvm_tense'),
    'tve_present': importlib.import_module('notebooks.tve_present'),
    'tve_pastpro': importlib.import_module('notebooks.tve_pastpro'),
    'tve_past': importlib.import_module('notebooks.tve_past'),
    'tve_future': importlib.import_module('notebooks.tve_future'),
}

# Mapping tenses to their modules
simplified_tense_mapping = {
    'present': ['ivd_present', 'tve_present', ('tvm_tense', 'present')],
    'past': ['ivd_past', 'tve_past', ('tvm_tense', 'past')],
    'future': ['ivd_future', 'tve_future', ('tvm_tense', 'future')],
    'pastpro': ['ivd_pastpro', 'tve_pastpro', ('tvm_tense', 'past progressive')],
    'presentperf': ['tvm_tve_presentperf'],
}

simplified_aspect_mapping = {
    'potential': ['tvm_tve_potential'],
    'passive': ['tvm_tve_passive'],
}

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/conjugate', methods=['GET'])
def conjugate():
    infinitive = request.args.get('infinitive')
    subject = request.args.get('subject')
    obj = request.args.get('obj', None)
    applicative = request.args.get('applicative', 'false').lower() == 'true'
    causative = request.args.get('causative', 'false').lower() == 'true'
    optative = request.args.get('optative', 'false').lower() == 'true'
    tense = request.args.get('tense')
    aspect = request.args.get('aspect')
    region_filter = request.args.get('region', None)

    if not infinitive or not subject or (not tense and not aspect):
        return jsonify({"error": "Invalid input"}), 400

    conjugations = {}
    module_found = False  # Flag to indicate if we found any valid module

    if aspect:
        if aspect not in simplified_aspect_mapping:
            return "Invalid aspect", 400

        for actual_aspect in simplified_aspect_mapping[aspect]:
            module = tense_modules.get(actual_aspect)
            if not module:
                continue

            embedded_tense = tense
            mood = 'optative' if optative and 'tve' in actual_aspect else None  # Apply optative as mood for 'tve' aspects

            try:
                # Check if the infinitive exists in the current module
                if not hasattr(module, 'verbs') or infinitive not in module.verbs:
                    continue

                subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural'] if subject == 'all' else [subject]
                objects = ['O1_Singular', 'O2_Singular', 'O3_Singular', 'O1_Plural', 'O2_Plural', 'O3_Plural'] if obj == 'all' else [obj] if obj else [None]

                print(f"Infinitive: {infinitive}, Subjects: {subjects}, Objects: {objects}, Aspect: {actual_aspect}, Embedded Tense: {embedded_tense}, Mood: {mood}, Region Filter: {region_filter}")

                for subj in subjects:
                    if obj == [None]:
                        if hasattr(module.collect_conjugations_all, '__code__') and 'mood' in module.collect_conjugations_all.__code__.co_varnames:
                            result = module.collect_conjugations_all(infinitive, subjects=[subj], tense=embedded_tense, applicative=applicative, causative=causative, mood=mood)
                        else:
                            result = module.collect_conjugations_all(infinitive, subjects=[subj], tense=embedded_tense, applicative=applicative, causative=causative)
                    else:
                        for obj_item in objects:
                            if hasattr(module, 'collect_conjugations'):
                                if hasattr(module.collect_conjugations, '__code__') and 'mood' in module.collect_conjugations.__code__.co_varnames:
                                    result = module.collect_conjugations(infinitive, [subj], obj=obj_item, applicative=applicative, causative=causative, mood=mood)
                                else:
                                    result = module.collect_conjugations(infinitive, [subj], obj=obj_item, applicative=applicative, causative=causative)
                            elif hasattr(module, 'collect_conjugations_all'):
                                if hasattr(module.collect_conjugations_all, '__code__') and 'mood' in module.collect_conjugations_all.__code__.co_varnames:
                                    result = module.collect_conjugations_all(infinitive, subjects=[subj], tense=embedded_tense, obj=obj_item, applicative=applicative, causative=causative, mood=mood)
                                else:
                                    result = module.collect_conjugations_all(infinitive, subjects=[subj], tense=embedded_tense, obj=obj_item, applicative=applicative, causative=causative)
                            else:
                                return "Invalid module", 400

                            print(f"Result for subj: {subj}, obj_item: {obj_item} -> {result}")

                            for region, forms in result.items():
                                if region_filter and region != region_filter:
                                    continue
                                if region not in conjugations:
                                    conjugations[region] = set()
                                conjugations[region].update(forms)

                module_found = True

            except KeyError as e:
                print(f"KeyError: {e} in module {actual_aspect}")
                # Continue to the next module if the current one does not contain the infinitive
                continue

    else:
        if tense not in simplified_tense_mapping:
            return "Invalid tense", 400

        for mapping in simplified_tense_mapping[tense]:
            if isinstance(mapping, tuple):
                actual_tense, embedded_tense = mapping
                if optative and actual_tense == 'tvm_tense':
                    embedded_tense = 'optative'
            else:
                actual_tense = mapping
                embedded_tense = tense

            module = tense_modules.get(actual_tense)
            if not module:
                continue

            mood = 'optative' if optative and 'tve' in actual_tense else None  # Apply optative as mood for 'tve' tenses

            try:
                # Check if the infinitive exists in the current module
                if not hasattr(module, 'verbs') or infinitive not in module.verbs:
                    continue

                subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural'] if subject == 'all' else [subject]
                objects = ['O1_Singular', 'O2_Singular', 'O3_Singular', 'O1_Plural', 'O2_Plural', 'O3_Plural'] if obj == 'all' else [obj] if obj else [None]

                print(f"Infinitive: {infinitive}, Subjects: {subjects}, Objects: {objects}, Tense: {actual_tense}, Embedded Tense: {embedded_tense}, Mood: {mood}, Region Filter: {region_filter}")

                print(f"Module verbs: {list(module.verbs.keys())}")  # Debugging: print available verbs in the module

                for subj in subjects:
                    if obj == [None]:
                        if hasattr(module.collect_conjugations_all, '__code__') and 'mood' in module.collect_conjugations_all.__code__.co_varnames:
                            result = module.collect_conjugations_all(infinitive, subjects=[subj], tense=embedded_tense, applicative=applicative, causative=causative, mood=mood)
                        else:
                            result = module.collect_conjugations_all(infinitive, subjects=[subj], tense=embedded_tense, applicative=applicative, causative=causative)
                    else:
                        for obj_item in objects:
                            if hasattr(module, 'collect_conjugations'):
                                if hasattr(module.collect_conjugations, '__code__') and 'mood' in module.collect_conjugations.__code__.co_varnames:
                                    result = module.collect_conjugations(infinitive, [subj], obj=obj_item, applicative=applicative, causative=causative, mood=mood)
                                else:
                                    result = module.collect_conjugations(infinitive, [subj], obj=obj_item, applicative=applicative, causative=causative)
                            elif hasattr(module, 'collect_conjugations_all'):
                                if hasattr(module.collect_conjugations_all, '__code__') and 'mood' in module.collect_conjugations_all.__code__.co_varnames:
                                    result = module.collect_conjugations_all(infinitive, subjects=[subj], tense=embedded_tense, obj=obj_item, applicative=applicative, causative=causative, mood=mood)
                                else:
                                    result = module.collect_conjugations_all(infinitive, subjects=[subj], tense=embedded_tense, obj=obj_item, applicative=applicative, causative=causative)
                            else:
                                return "Invalid module", 400

                            print(f"Result for subj: {subj}, obj_item: {obj_item} -> {result}")

                            for region, forms in result.items():
                                if region_filter and region != region_filter:
                                    continue
                                if region not in conjugations:
                                    conjugations[region] = set()
                                conjugations[region].update(forms)

                module_found = True

            except KeyError as e:
                print(f"KeyError: {e} in module {actual_tense}")
                if isinstance(module.verbs[infinitive], list):
                    print(f"Available forms in module for {infinitive}: {module.verbs[infinitive]}")
                else:
                    print(f"Available subjects in module for {infinitive}: {module.verbs[infinitive].keys()}")
                # Continue to the next module if the current one does not contain the infinitive
                continue

    if not module_found:
        return jsonify({"error": f"Infinitive {infinitive} not found in any module."}), 404

    # Convert sets to lists for JSON serialization and sort conjugations chronologically
    ordered_subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']
    ordered_objects = ['O1_Singular', 'O2_Singular', 'O3_Singular', 'O1_Plural', 'O2_Plural', 'O3_Plural']
    formatted_conjugations = {}

    for region, forms in conjugations.items():
        sorted_forms = sorted(forms, key=lambda x: (ordered_subjects.index(x[0]), ordered_objects.index(x[1]) if x[1] else -1))
        formatted_forms = []
        personal_pronouns = module.get_personal_pronouns(region)  # Get the personal pronouns from the module
        for form in sorted_forms:
            subject_pronoun = personal_pronouns.get(form[0], form[0])
            object_pronoun = personal_pronouns.get(form[1], '') if form[1] else ''
            formatted_forms.append(f"{subject_pronoun} {object_pronoun}: {form[2]}")
        formatted_conjugations[region] = formatted_forms

    return jsonify(formatted_conjugations)

if __name__ == '__main__':
    app.run(debug=True)