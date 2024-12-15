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
        if params['neg_imperative']:
            conjugations = self.process_negative_imperative(
                params['infinitive'], params['subject'], params['obj'],
                params['applicative'], params['causative'], params['region_filter'])
        elif params['imperative']:
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

    def process_imperative(self, infinitive, subject, obj, applicative, causative, region_filter):
        """Process imperative conjugations."""
        module = self.tense_modules.get('tve_past')
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

        imperatives = module.extract_imperatives(all_conjugations, subjects)
        return module.format_imperatives(imperatives)

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
        return module.format_neg_imperatives(neg_imperatives)

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
            subjects = self.ordered_subjects if subject == 'all' else [subject]
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

        return self._format_conjugations(conjugations, used_module)

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
                subjects = self.ordered_subjects if subject == 'all' else [subject]
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

        return self._format_conjugations(conjugations, used_module)

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

    def _format_conjugations(self, conjugations, module):
        """Format conjugations for response."""
        formatted = {}
        module_name = module.__name__.split('.')[-1]

        for region, forms in conjugations.items():
            personal_pronouns = module.get_personal_pronouns(region, module_name)
            formatted_forms = []

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
                formatted_forms.append(f"{subject_pronoun} {object_pronoun}: {conjugated_verb}")

            formatted[region] = formatted_forms

        return formatted