class ConjugationService:
    def __init__(self, tense_modules, simplified_tense_mapping, simplified_aspect_mapping):
        self.tense_modules = tense_modules
        self.simplified_tense_mapping = simplified_tense_mapping
        self.simplified_aspect_mapping = simplified_aspect_mapping
        self.ordered_subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural']
        self.ordered_objects = ['O1_Singular', 'O2_Singular', 'O3_Singular', 'O1_Plural', 'O2_Plural', 'O3_Plural']

    def conjugate(self, params):
        """Main entry point for conjugation processing."""
        conjugations = None
        
        # Check if it's a TVM verb
        is_tvm_verb = False
        for module_key, module in self.tense_modules.items():
            if module_key == 'tvm_tense':
                if hasattr(module, 'verbs') and params['infinitive'] in module.verbs:
                    is_tvm_verb = True
                    # If it's a TVM verb and there's an object, raise error
                    if params['obj']:
                        raise ValueError("This verb belongs to a verb group that cannot take an object / Bu fiil grubu nesne alamaz.")
                    break

        if params['neg_imperative']:
            if is_tvm_verb:
                # For TVM verbs, use tvm_tense with present tense
                conjugations = self.process_tvm_imperative(
                    params['infinitive'], params['subject'], params['obj'],
                    params['applicative'], params['causative'], params['region_filter'],
                    tense='present', is_negative=True)
            else:
                # For TVE verbs, use existing process
                conjugations = self.process_negative_imperative(
                    params['infinitive'], params['subject'], params['obj'],
                    params['applicative'], params['causative'], params['region_filter'])
        elif params['imperative']:
            if is_tvm_verb:
                # For TVM verbs, use tvm_tense with past tense
                conjugations = self.process_tvm_imperative(
                    params['infinitive'], params['subject'], params['obj'],
                    params['applicative'], params['causative'], params['region_filter'],
                    tense='past', is_negative=False)
            else:
                # For TVE verbs, use existing process
                conjugations = self.process_imperative(
                    params['infinitive'], params['subject'], params['obj'],
                    params['applicative'], params['causative'], params['region_filter'])
        elif params['aspect']:
            conjugations = self.process_aspect_conjugation(
                params['infinitive'], params['subject'], params['obj'],
                params['aspect'], params['tense'], params['applicative'],
                params['causative'], params['optative'], params['region_filter'])
        else:
            conjugations = self.process_tense_conjugation(
                params['infinitive'], params['subject'], params['obj'],
                params['tense'], params['applicative'], params['causative'],
                params['optative'], params['region_filter'])

        return conjugations

    def format_conjugations(self, conjugations, module):
        """Format conjugations for response with verb group information."""
        formatted = {}
        module_name = module.__name__.split('.')[-1]
        
        # More nuanced verb group determination
        if module_name.startswith('tve'):
            verb_group = "Ergative"
        elif module_name.startswith('ivd') or (module_name.startswith('tvm_tve') and any(x in module_name for x in ['potential', 'presentperf'])):
            verb_group = "Dative"
        elif module_name == 'tvm_tense' or (module_name.startswith('tvm_tve') and any(x in module_name for x in ['passive'])):
            verb_group = "Nominative"
        else:
            # For other cases, determine based on presence of certain patterns
            if 'tve' in module_name:
                verb_group = "Ergative"
            else:
                verb_group = "Unknown"

        for region, forms in conjugations.items():
            if region not in formatted:
                formatted[region] = {}
            
            if verb_group not in formatted[region]:
                formatted[region][verb_group] = []

            personal_pronouns = module.get_personal_pronouns(region, module_name)
            current_forms = []

            sorted_forms = sorted(
                forms,
                key=lambda x: (
                    self.ordered_subjects.index(x[0]),
                    self.ordered_objects.index(x[1]) if x[1] else -1
                )
            )

            for subject, obj, conjugated_verb in sorted_forms:
                if any(p is None for p in (subject, conjugated_verb)):
                    continue
                subject_pronoun = personal_pronouns.get(subject, subject)
                object_pronoun = personal_pronouns.get(obj, '') if obj else ''
                current_forms.append({
                    "subject": subject_pronoun,
                    "object": object_pronoun,
                    "conjugation": conjugated_verb
                })

            formatted[region][verb_group] = current_forms

        return formatted

    def _call_conjugation_method(self, module, infinitive, subjects, obj, tense=None,
                               applicative=False, causative=False, mood=None):
        """Helper method to call appropriate conjugation method based on module capabilities."""
        if hasattr(module, 'collect_conjugations'):
            if hasattr(module.collect_conjugations, '__code__') and 'mood' in module.collect_conjugations.__code__.co_varnames:
                return module.collect_conjugations(
                    infinitive, subjects, obj=obj,
                    applicative=applicative, causative=causative, mood=mood
                )
            else:
                return module.collect_conjugations(
                    infinitive, subjects, obj=obj,
                    applicative=applicative, causative=causative
                )
        elif hasattr(module, 'collect_conjugations_all'):
            if hasattr(module.collect_conjugations_all, '__code__') and 'mood' in module.collect_conjugations_all.__code__.co_varnames:
                return module.collect_conjugations_all(
                    infinitive, subjects=subjects, tense=tense,
                    obj=obj, applicative=applicative, causative=causative, mood=mood
                )
            else:
                return module.collect_conjugations_all(
                    infinitive, subjects=subjects, tense=tense,
                    obj=obj, applicative=applicative, causative=causative
                )
        else:
            raise ValueError("Invalid module")

    def process_imperative(self, infinitive, subject, obj, applicative, causative, region_filter):
        """Process imperative conjugations."""
        module = None
        if 'tve_past' in self.tense_modules and infinitive in self.tense_modules['tve_past'].verbs:
            module = self.tense_modules['tve_past']
        elif 'ivd_present' in self.tense_modules and infinitive in self.tense_modules['ivd_present'].verbs:
            module = self.tense_modules['ivd_present']

        if not module:
            return None


        subjects = ['S2_Singular', 'S2_Plural'] if subject == 'all' else [subject]
        objects = self.ordered_objects if obj == 'all' else [obj] if obj else [None]
        all_conjugations = {}

        for subj in subjects:
            for obj_item in objects:
                result = self._call_conjugation_method(
                    module, infinitive, [subj], obj_item,
                    applicative=applicative, causative=causative
                )
                
                for region, forms in result.items():
                    if region_filter and region not in region_filter.split(','):
                        continue
                    if region not in all_conjugations:
                        all_conjugations[region] = set()
                    all_conjugations[region].update(forms)

        imperatives = module.extract_imperatives(all_conjugations, subjects)
        return self.format_conjugations(imperatives, module)

    def process_negative_imperative(self, infinitive, subject, obj, applicative, causative, region_filter):
        """Process negative imperative conjugations."""
        module = self.tense_modules.get('tve_present')
        if not module or not hasattr(module, 'verbs') or infinitive not in module.verbs:
            return None

        subjects = ['S2_Singular', 'S2_Plural'] if subject == 'all' else [subject]
        objects = self.ordered_objects if obj == 'all' else [obj] if obj else [None]
        all_conjugations = {}

        for subj in subjects:
            for obj_item in objects:
                result = self._call_conjugation_method(
                    module, infinitive, [subj], obj_item,
                    applicative=applicative, causative=causative
                )
                
                for region, forms in result.items():
                    if region_filter and region not in region_filter.split(','):
                        continue
                    if region not in all_conjugations:
                        all_conjugations[region] = set()
                    all_conjugations[region].update(forms)

        neg_imperatives = module.extract_neg_imperatives(all_conjugations, subjects)
        return self.format_conjugations(neg_imperatives, module)

    def process_tvm_imperative(self, infinitive, subject, obj, applicative, causative, 
                             region_filter, tense, is_negative):
        """Process TVM imperative conjugations using tvm_tense module."""
        module = self.tense_modules.get('tvm_tense')
        if not module or not hasattr(module, 'verbs') or infinitive not in module.verbs:
            return None

        subjects = ['S2_Singular', 'S2_Plural'] if subject == 'all' else [subject]
        objects = self.ordered_objects if obj == 'all' else [obj] if obj else [None]
        all_conjugations = {}

        for subj in subjects:
            for obj_item in objects:
                result = self._call_conjugation_method(
                    module, infinitive, [subj], obj_item, tense,
                    applicative, causative
                )
                
                for region, forms in result.items():
                    if region_filter and region not in region_filter.split(','):
                        continue
                    if region not in all_conjugations:
                        all_conjugations[region] = set()
                    for form in forms:
                        # Add 'mot' prefix for negative imperatives
                        if is_negative:
                            neg_prefix = "mo" if region in ("HO", "AŞ") else "mot"
                            modified_form = (form[0], form[1], f"{neg_prefix} {form[2]}")
                            all_conjugations[region].add(modified_form)
                        else:
                            all_conjugations[region].add(form)

        return self.format_conjugations(all_conjugations, module)

    def process_aspect_conjugation(self, infinitive, subject, obj, aspect, tense,
                                 applicative, causative, optative, region_filter):
        """Process aspect-based conjugations."""
        conjugations = {}
        module_found = False
        used_module = None

        for actual_aspect in self.simplified_aspect_mapping[aspect]:
            module = self.tense_modules.get(actual_aspect)
            if not module or not hasattr(module, 'verbs') or infinitive not in module.verbs:
                continue

            mood = 'optative' if optative and 'tve' in actual_aspect else None
            subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural'] if subject == 'all' else [subject]
            objects = self.ordered_objects if obj == 'all' else [obj] if obj else [None]

            try:
                for subj in subjects:
                    for obj_item in objects:
                        result = self._call_conjugation_method(
                            module, infinitive, [subj], obj_item, tense,
                            applicative, causative, mood
                        )

                        for region, forms in result.items():
                            if region_filter and region not in region_filter.split(','):
                                continue
                            if region not in conjugations:
                                conjugations[region] = set()
                            conjugations[region].update(forms)
                            used_module = module
                            module_found = True

            except ValueError as e:
                raise ValueError(str(e))

        if not module_found:
            return None

        return self.format_conjugations(conjugations, used_module)

    def process_tense_conjugation(self, infinitive, subject, obj, tense,
                                applicative, causative, optative, region_filter):
        """Process tense-based conjugations."""
        conjugations = {}
        module_found = False
        used_module = None

        for mapping in self.simplified_tense_mapping[tense]:
            actual_tense, embedded_tense = mapping if isinstance(mapping, tuple) else (mapping, tense)
            
            if optative and actual_tense == 'tvm_tense':
                embedded_tense = 'optative'

            if actual_tense.startswith('tvm') and obj in self.ordered_objects:
                continue

            module = self.tense_modules.get(actual_tense)
            if not module or not hasattr(module, 'verbs') or infinitive not in module.verbs:
                continue

            try:
                subjects = ['S1_Singular', 'S2_Singular', 'S3_Singular', 'S1_Plural', 'S2_Plural', 'S3_Plural'] if subject == 'all' else [subject]
                objects = self.ordered_objects if obj == 'all' else [obj] if obj else [None]

                for subj in subjects:
                    for obj_item in objects:
                        result = self._call_conjugation_method(
                            module, infinitive, [subj], obj_item,
                            embedded_tense, applicative, causative,
                            'optative' if optative else None
                        )

                        for region, forms in result.items():
                            if region_filter and region not in region_filter.split(','):
                                continue
                            if region not in conjugations:
                                conjugations[region] = set()
                            conjugations[region].update(forms)
                            used_module = module
                            module_found = True

            except ValueError as e:
                raise ValueError(str(e))

        if not module_found:
            return None

        return self.format_conjugations(conjugations, used_module)