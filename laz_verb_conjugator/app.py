from flask import Flask, request, jsonify, send_from_directory
import importlib
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    imperative = request.args.get('imperative', 'false').lower() == 'true'
    neg_imperative = request.args.get('neg_imperative', 'false').lower() == 'true'
    tense = request.args.get('tense')
    aspect = request.args.get('aspect')
    region_filter = request.args.get('region', None)

    logger.debug(f"Received request with parameters: {request.args}")

    if not infinitive or not subject or (not tense and not aspect and not imperative and not neg_imperative):
        return jsonify({"error": "Invalid input"}), 400

    conjugations_by_group = {}  # Initialize the dictionary to store conjugations by group
    module_found = False  # Flag to indicate if we found any valid module

    # Define ordered subjects and objects
    ordered_subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']
    ordered_objects = ['O1_Singular', 'O2_Singular', 'O3_Singular', 'O1_Plural', 'O2_Plural', 'O3_Plural']

    # Convert the region_filter to a set of regions if specified
    region_filter_set = set(region_filter.split(',')) if region_filter else None

    if neg_imperative:
        module = tense_modules.get('tve_present')
        if not module:
            return jsonify({"error": "Negative imperative forms not supported for this verb."}), 400

        try:
            if not hasattr(module, 'verbs') or infinitive not in module.verbs:
                return jsonify({"error": f"Infinitive {infinitive} not found in the database."}), 404

            subjects = ['S2_Singular', 'S2_Plural'] if subject == 'all' else [subject]
            objects = ordered_objects if obj == 'all' else [obj] if obj else [None]
            all_conjugations = {}

            for subj in subjects:
                for obj_item in objects:
                    result = module.collect_conjugations(infinitive, [subj], obj=obj_item, applicative=applicative, causative=causative)
                    for region, forms in result.items():
                        if region_filter_set and region not in region_filter_set:
                            continue
                        if region not in all_conjugations:
                            all_conjugations[region] = set()
                        all_conjugations[region].update(forms)

            neg_imperatives = module.extract_neg_imperatives(all_conjugations, subjects)
            formatted_conjugations = module.format_neg_imperatives(neg_imperatives)

            return jsonify(formatted_conjugations)

        except Exception as e:
            logger.error(f"Error while processing negative imperative: {e}")
            return jsonify({"error": str(e)}), 400

    if imperative:
        if subject not in ['S2_Singular', 'S2_Plural', 'all']:
            return jsonify({"error": "Imperatives are only available for S2_Singular, S2_Plural, or all"}), 400

        module = tense_modules.get('tve_past')  # Assuming imperative forms are handled in past tense module
        if not module:
            return jsonify({"error": "Imperative forms not supported for this verb."}), 400

        try:
            if not hasattr(module, 'verbs') or infinitive not in module.verbs:
                return jsonify({"error": f"Infinitive {infinitive} not found in the database."}), 404

            subjects = ['S2_Singular', 'S2_Plural'] if subject == 'all' else [subject]
            objects = ordered_objects if obj == 'all' else [obj] if obj else [None]
            all_conjugations = {}

            for subj in subjects:
                for obj_item in objects:
                    result = module.collect_conjugations(infinitive, [subj], obj=obj_item, applicative=applicative, causative=causative)
                    for region, forms in result.items():
                        if region_filter_set and region not in region_filter_set:
                            continue
                        if region not in all_conjugations:
                            all_conjugations[region] = set()
                        all_conjugations[region].update(forms)

            neg_imperatives = module.extract_imperatives(all_conjugations, subjects)
            formatted_conjugations = module.format_imperatives(neg_imperatives)

            return jsonify(formatted_conjugations)
        except Exception as e:
            logger.error(f"Error while processing imperative: {e}")
            return jsonify({"error": str(e)}), 400

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

                subjects = ordered_subjects if subject == 'all' else [subject]
                objects = ordered_objects if obj == 'all' else [obj] if obj else [None]

                current_group = actual_aspect  # Set the current group as the aspect

                for subj in subjects:
                    if obj == [None]:
                        if hasattr(module.collect_conjugations_all, '__code__') and 'mood' in module.collect_conjugations_all.__code__.co_varnames:
                            result = module.collect_conjugations_all(infinitive, subjects=[subj], applicative=applicative, causative=causative, mood=mood)
                        else:
                            result = module.collect_conjugations_all(infinitive, subjects=[subj], applicative=applicative, causative=causative)
                    else:
                        for obj_item in objects:
                            if hasattr(module, 'collect_conjugations'):
                                if hasattr(module.collect_conjugations, '__code__') and 'mood' in module.collect_conjugations.__code__.co_varnames:
                                    result = module.collect_conjugations(infinitive, [subj], obj=obj_item, applicative=applicative, causative=causative, mood=mood)
                                else:
                                    result = module.collect_conjugations(infinitive, [subj], obj=obj_item, applicative=applicative, causative=causative)
                            elif hasattr(module, 'collect_conjugations_all'):
                                if hasattr(module.collect_conjugations_all, '__code__') and 'mood' in module.collect_conjugations_all.__code__.co_varnames:
                                    result = module.collect_conjugations_all(infinitive, subjects=[subj], obj=obj_item, applicative=applicative, causative=causative, mood=mood)
                                else:
                                    result = module.collect_conjugations_all(infinitive, subjects=[subj], obj=obj_item, applicative=applicative, causative=causative)
                            else:
                                return "Invalid module", 400

                            for region, forms in result.items():
                                if region_filter_set and region not in region_filter_set:
                                    continue
                                if current_group not in conjugations_by_group:
                                    conjugations_by_group[current_group] = {}
                                if region not in conjugations_by_group[current_group]:
                                    conjugations_by_group[current_group][region] = set()
                                conjugations_by_group[current_group][region].update(forms)

                module_found = True

            except KeyError as e:
                logger.error(f"KeyError: {e} in module {actual_aspect}")
                continue
            except ValueError as e:
                logger.error(f"ValueError: {e}")
                return jsonify({"error": str(e)}), 400

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

            current_group = actual_tense  # Set the current group as the tense

            try:
                # Check if the infinitive exists in the current module
                if not hasattr(module, 'verbs') or infinitive not in module.verbs:
                    continue

                if actual_tense.startswith('tvm'):
                    if obj:
                        # Handle TVM verbs without objects
                        objects = [None]  # Set objects to None because TVM verbs cannot have objects
                else:
                    # Handle non-TVM verbs, allowing objects
                    subjects = ordered_subjects if subject == 'all' else [subject]
                    objects = ordered_objects if obj == 'all' else [obj] if obj else [None]

                # Continue with the existing logic to collect and format the conjugations
                for subj in subjects:
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
                            return jsonify({"error": "Invalid module"}), 400

                        for region, forms in result.items():
                            if region_filter_set and region not in region_filter_set:
                                continue
                            if current_group not in conjugations_by_group:
                                conjugations_by_group[current_group] = {}
                            if region not in conjugations_by_group[current_group]:
                                conjugations_by_group[current_group][region] = set()
                            conjugations_by_group[current_group][region].update(forms)

                module_found = True

            except KeyError as e:
                logger.error(f"KeyError: {e} in module {actual_tense}")
                continue
            except ValueError as e:
                logger.error(f"ValueError: {e}")
                return jsonify({"error": str(e)}), 400

    if not module_found:
        return jsonify({"error": f"Infinitive {infinitive} not found in any module."}), 404

    # Convert sets to lists for JSON serialization
    formatted_conjugations = {}
    for group, conjugations in conjugations_by_group.items():
        for region in conjugations:
            conjugations[region] = list(conjugations[region])
        formatted_conjugations[group] = format_conjugations(conjugations, tense_modules[group], ordered_subjects, ordered_objects)

    return jsonify(formatted_conjugations)

def format_conjugations(conjugations, module, ordered_subjects, ordered_objects):
    formatted_conjugations = {}

    for region, forms in conjugations.items():
        sorted_forms = sorted(forms, key=lambda x: (ordered_subjects.index(x[0]), ordered_objects.index(x[1]) if x[1] else -1))
        formatted_forms = []
        personal_pronouns = module.get_personal_pronouns(region)

        for form in sorted_forms:
            if len(form) != 3:
                continue

            subject, obj, conjugated_verb = form

            # Separate dictionaries for subject and object pronouns
            subject_pronoun = personal_pronouns.get(subject, subject)
            object_pronoun = personal_pronouns.get(obj, '') if obj else ''

            formatted_forms.append(f"{subject_pronoun} {object_pronoun}: {conjugated_verb}")

        formatted_conjugations[region] = formatted_forms

    return formatted_conjugations

if __name__ == '__main__':
    app.run(debug=True)
