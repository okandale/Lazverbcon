class ConjugationValidator:
    def __init__(self, tense_modules, simplified_tense_mapping, simplified_aspect_mapping):
        self.tense_modules = tense_modules
        self.simplified_tense_mapping = simplified_tense_mapping
        self.simplified_aspect_mapping = simplified_aspect_mapping
        self.special_verb_errors = {
            "coxons": "This verb cannot have an object/bu fiil nesne alamaz.",
            "cozun": "This verb cannot have an object/bu fiil nesne alamaz.",
            "gyožin": "This verb cannot have an object/bu fiil nesne alamaz."
        }

    def validate_request(self, request_params):
        """Main validation method that runs all validations in sequence."""
        # Basic parameter validation
        params, error = self.validate_basic_params(request_params)
        if error:
            return None, error

        # Special verb validation
        error = self.validate_verb_constraints(params['infinitive'], params['obj'])
        if error:
            return None, error

        # TVM-only validation
        error = self.validate_tvm_only(params['infinitive'], params['obj'])
        if error:
            return None, error

        # Imperative validation
        if params['imperative'] or params['neg_imperative']:
            error = self.validate_imperative_subject(params['subject'])
            if error:
                return None, error

        # Aspect validation
        if params['aspect']:
            error = self.validate_aspect(params['aspect'])
            if error:
                return None, error

        # Tense validation when needed
        if not params['aspect'] and not params['imperative'] and not params['neg_imperative']:
            error = self.validate_tense(params['tense'])
            if error:
                return None, error

        return params, None

    def validate_basic_params(self, request_params):
        """Validate required parameters and normalize values."""
        infinitive = request_params.get('infinitive')
        if not infinitive:
            return None, ({"error": "Infinitive is required"}, 400)

        subject = request_params.get('subject')
        if not subject:
            return None, ({"error": "Subject is required"}, 400)

        # Process and normalize parameters
        params = {
            'infinitive': infinitive.lower().rstrip(),
            'subject': subject,
            'obj': request_params.get('obj'),
            'applicative': request_params.get('applicative', 'false').lower() == 'true',
            'causative': request_params.get('causative', 'false').lower() == 'true',
            'optative': request_params.get('optative', 'false').lower() == 'true',
            'imperative': request_params.get('imperative', 'false').lower() == 'true',
            'neg_imperative': request_params.get('neg_imperative', 'false').lower() == 'true',
            'tense': request_params.get('tense'),
            'aspect': request_params.get('aspect'),
            'region_filter': request_params.get('region')
        }

        # Normalize obj
        if params['obj'] in ['', 'None']:
            params['obj'] = None

        return params, None

    def validate_verb_constraints(self, infinitive, obj):
        """Validate verb-specific constraints."""
        if infinitive in self.special_verb_errors and obj:
            return {"error": self.special_verb_errors[infinitive]}, 400
        return None

    def validate_tvm_only(self, infinitive, obj):
        """Validate TVM-only verb constraints."""
        is_tvm_only = True
        for module_key, module in self.tense_modules.items():
            if hasattr(module, 'verbs') and infinitive in module.verbs:
                if not module_key.startswith('tvm'):
                    is_tvm_only = False
                    break

        if is_tvm_only and obj:
            return {"error": f"This verb cannot have an object/bu fiil nesne alamaz."}, 400
        return None

    def validate_aspect(self, aspect):
        """Validate aspect parameter."""
        if aspect and aspect not in self.simplified_aspect_mapping:
            return {"error": "Invalid aspect"}, 400
        return None

    def validate_tense(self, tense):
        """Validate tense parameter."""
        if tense and tense not in self.simplified_tense_mapping:
            return {"error": "Invalid tense"}, 400
        return None

    def validate_imperative_subject(self, subject):
        """Validate subject for imperative conjugations."""
        if subject not in ['S2_Singular', 'S2_Plural', 'all']:
            return {"error": "Imperatives are only available for S2_Singular, S2_Plural, or all"}, 400
        return None