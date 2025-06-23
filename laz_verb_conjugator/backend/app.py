from flask import Flask, request, jsonify
from flask_cors import CORS
import importlib
import logging
import os
import json
from validators import ConjugationValidator
from services.conjugation import ConjugationService
from config.webhook_config import WebhookConfig
from services.webhook import WebhookService, WebhookError, SignatureVerificationError, WebhookDisabledError

from flask_jwt_extended import JWTManager

from .admin import admin
from .verbs import verbs

from . import db  # Should fail if the database is not set.

# Set up the login manager (for the admin part)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a separate logger for request/response logging
req_res_logger = logging.getLogger('request_response')
req_res_logger.setLevel(logging.INFO)

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Create a file handler for request/response logs
req_res_handler = logging.FileHandler('logs/request_response.log')
req_res_handler.setLevel(logging.INFO)

# Create a formatter that includes timestamp
formatter = logging.Formatter('%(asctime)s - %(message)s')
req_res_handler.setFormatter(formatter)

# Add the handler to the request/response logger
req_res_logger.addHandler(req_res_handler)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"

# Register blueprints
app.register_blueprint(
    admin, url_prefix="/api/admin"
)

app.register_blueprint(
    verbs, url_prefix="/api/verbs"
)

# Useful for admin authentication.
jwt = JWTManager(app)

app.debug = True

# Enable CORS with specific configuration
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://lazuri.org",
            "http://lazuri.org",
            "https://lazverbcon.pages.dev",
            "http://localhost:5173",
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize webhook configuration and service
webhook_config = WebhookConfig.load()
webhook_service = WebhookService(webhook_config)

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

# Mapping tenses to their modules (keep your existing mappings)
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

def log_request_response(request_params, response_data, endpoint):
    """Log request parameters and response data to the log file"""
    log_entry = {
        'request': request_params,
        'response': response_data
    }
    req_res_logger.info(json.dumps(log_entry, ensure_ascii=False))

@app.route('/update', methods=['POST'])
def webhook_update():
    try:
        webhook_service.verify_request(
            signature=request.headers.get('X-Hub-Signature-256'),
            payload=request.data,
            event_type=request.headers.get('X-GitHub-Event')
        )
        
        webhook_service.handle_update()
        return jsonify({'status': 'success'}), 200
        
    except WebhookDisabledError as e:
        logger.warning(str(e))
        return jsonify({'error': 'Webhook disabled'}), 404
        
    except SignatureVerificationError as e:
        logger.warning(str(e))
        return jsonify({'error': 'Invalid signature'}), 401
        
    except WebhookError as e:
        logger.warning(str(e))
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        logger.error(f"Unexpected error in webhook: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/ping', methods=['GET'])
def hi():
    return jsonify({"response": "pong!"})

def check_verb_existence(infinitive, tense_modules):
    """
    Check if a verb exists in IVD, TVE, and TVM modules.
    Also checks special case modules (tvm_tve_*) that can handle both TVE and TVM.
    Returns: (bool, bool, bool, bool) - (exists_in_ivd, exists_in_tve, exists_in_tvm, exists_in_tvm_tve)
    """
    logger.debug(f"Starting detailed verb check for infinitive: {infinitive}")
    
    # Normalize infinitive to lowercase
    infinitive = infinitive.lower().strip()
    
    # Check IVD verbs
    exists_in_ivd = False
    ivd_modules = ['ivd_present', 'ivd_past', 'ivd_pastpro', 'ivd_future']
    for module_name in ivd_modules:
        if hasattr(tense_modules[module_name], 'verbs'):
            verbs = {v.lower().strip(): v for v in tense_modules[module_name].verbs}
            if infinitive in verbs:
                exists_in_ivd = True
                break
    
    # Check TVE verbs
    exists_in_tve = False
    tve_modules = ['tve_present', 'tve_past', 'tve_pastpro', 'tve_future']
    for module_name in tve_modules:
        if hasattr(tense_modules[module_name], 'verbs'):
            verbs = {v.lower().strip(): v for v in tense_modules[module_name].verbs}
            if infinitive in verbs:
                exists_in_tve = True
                break

    # Check TVM verbs
    exists_in_tvm = False
    if hasattr(tense_modules['tvm_tense'], 'verbs'):
        verbs = {v.lower().strip(): v for v in tense_modules['tvm_tense'].verbs}
        if infinitive in verbs:
            exists_in_tvm = True

    # Check special TVM/TVE modules
    exists_in_tvm_tve = False
    tvm_tve_modules = ['tvm_tve_presentperf', 'tvm_tve_potential', 'tvm_tve_passive']
    for module_name in tvm_tve_modules:
        if hasattr(tense_modules[module_name], 'verbs'):
            verbs = {v.lower().strip(): v for v in tense_modules[module_name].verbs}
            if infinitive in verbs:
                exists_in_tvm_tve = True
                break
    
    logger.debug(f"Final result for {infinitive} - IVD: {exists_in_ivd}, TVE: {exists_in_tve}, TVM: {exists_in_tvm}, TVM/TVE: {exists_in_tvm_tve}")
    return exists_in_ivd, exists_in_tve, exists_in_tvm, exists_in_tvm_tve

@app.route('/api/conjugate', methods=['GET'])
def conjugate():
    request_params = dict(request.args)
    infinitive = request_params.get('infinitive', '').strip().lower()
    request_params['infinitive'] = infinitive
    aspect = request_params.get('aspect')
    tense = request_params.get('tense')

    # Make sure you define them up front
    has_applicative = (request_params.get('applicative') == 'true')
    has_causative   = (request_params.get('causative') == 'true')    

    if not infinitive:
        error_response = {"error": "Infinitive is required"}
        log_request_response(request_params, error_response, '/api/conjugate')
        return jsonify(error_response), 400

    # Special check for "guri mentxu"
    if infinitive == 'guri mentxu' and aspect != 'potential':
        error_response = {
            "error": "This verb only exists in potential form. You need to select the potential form under 'Aspect'"
        }
        log_request_response(request_params, error_response, '/api/conjugate')
        return jsonify(error_response), 400


    has_markers = any(request_params.get(marker) == 'true' 
                     for marker in ['applicative', 'causative', 'optative'])

    # 3) Extract object (obj) and convert empty or "None" -> real None
    obj = request_params.get('obj')
    if obj in ('', 'None'):
        obj = None
    # We can store that back into request_params if you want consistency
    request_params['obj'] = obj


    # Special check for "gexvamu" or "cexvamu"; add any verb that requires an applicative/causative to this block
    if infinitive in (('gexvamu', 'cexvamu', 'otebriǩu')) and aspect is None:
        # We specifically want at least one of 'applicative' or 'causative' to be true
        has_applicative = (request_params.get('applicative') == 'true')
        has_causative   = (request_params.get('causative') == 'true')
        
        if not (has_applicative or has_causative):
            error_response = {
                "error": "This verb requires a marker (applicative or causative)/bu fiile uygulamalı veya ettirgen belirteci gerekiyor."
            }
            log_request_response(request_params, error_response, '/api/conjugate')
            return jsonify(error_response), 400




    # Check verb existence in all types
    exists_in_ivd, exists_in_tve, exists_in_tvm, exists_in_tvm_tve = check_verb_existence(infinitive, tense_modules)

    # 6. Now do the direct object checks for Applicative / Causative
    if exists_in_tve and (has_applicative or has_causative):
        if has_applicative and not obj:
            error_response = {"error": "Applicative requires an object to be specified. / Uygulamalı belirteç bir nesnenin belirtilmesini gerektirir."}
            return jsonify(error_response), 400

        if has_causative and not obj:
            error_response = {"error": "Causative requires an object to be specified. / Ettirgen belirteç bir nesnenin belirtilmesini gerektirir"}
            return jsonify(error_response), 400

    # Handle aspect modules (only potential and passive)
    if aspect and aspect in simplified_aspect_mapping and exists_in_tvm_tve:
        aspect_validator = ConjugationValidator(
            tense_modules, 
            {}, 
            simplified_aspect_mapping
        )
        aspect_service = ConjugationService(
            tense_modules,
            {},
            simplified_aspect_mapping
        )
        aspect_params, aspect_error = aspect_validator.validate_request(request_params)
        if not aspect_error:
            results = aspect_service.conjugate(aspect_params)
            if results:
                log_request_response(request_params, results, '/api/conjugate')
                return jsonify(results)
    
    # Handle marker restrictions
    if exists_in_ivd and not (exists_in_tve or exists_in_tvm_tve) and has_markers:
        error_response = {
            "error": "This verb belongs to a verb group that cannot take additional markers"
        }
        log_request_response(request_params, error_response, '/api/conjugate')
        return jsonify(error_response), 400

    results = {}
    
    # Special handling for present perfect tense
    if tense == 'presentperf':
        validator = ConjugationValidator(
            tense_modules, 
            {'presentperf': ['tvm_tve_presentperf']},
            {}
        )
        service = ConjugationService(
            tense_modules, 
            {'presentperf': ['tvm_tve_presentperf']},
            {}
        )
        params, error = validator.validate_request(request_params)
        if not error:
            conjugations = service.conjugate(params)
            if conjugations:
                return jsonify(conjugations)
    else:
        # Regular tense handling with proper group separation
        # Prepare mappings
        ivd_mapping = {}
        tve_mapping = {}
        tvm_mapping = {}
        
        for tense, modules in simplified_tense_mapping.items():
            if isinstance(modules, list):
                ivd_modules = [m for m in modules if isinstance(m, str) and m.startswith('ivd_')]
                tve_modules = [m for m in modules if isinstance(m, str) and m.startswith('tve_')]
                tvm_modules = [m for m in modules if isinstance(m, tuple) or 
                             (isinstance(m, str) and m.startswith('tvm_'))]
                
                if ivd_modules and exists_in_ivd and not has_markers:
                    ivd_mapping[tense] = ivd_modules
                if tve_modules and exists_in_tve:
                    tve_mapping[tense] = tve_modules
                if tvm_modules and exists_in_tvm:
                    tvm_mapping[tense] = tvm_modules

        # Process IVD conjugations
        if exists_in_ivd and not has_markers:
            ivd_validator = ConjugationValidator(tense_modules, ivd_mapping, {})
            ivd_service = ConjugationService(tense_modules, ivd_mapping, {})
            ivd_params, ivd_error = ivd_validator.validate_request(request_params)
            if not ivd_error:
                ivd_results = ivd_service.conjugate(ivd_params)
                if ivd_results:
                    results.update(ivd_results)

        # Process TVE conjugations
        if exists_in_tve:
            tve_validator = ConjugationValidator(tense_modules, tve_mapping, {})
            tve_service = ConjugationService(tense_modules, tve_mapping, {})
            tve_params, tve_error = tve_validator.validate_request(request_params)
            if not tve_error:
                tve_results = tve_service.conjugate(tve_params)
                if tve_results:
                    for region in tve_results:
                        if region not in results:
                            results[region] = {}
                        results[region].update(tve_results[region])

        # Process TVM conjugations
        if exists_in_tvm:
            tvm_validator = ConjugationValidator(tense_modules, tvm_mapping, {})
            tvm_service = ConjugationService(tense_modules, tvm_mapping, {})
            tvm_params, tvm_error = tvm_validator.validate_request(request_params)
            if not tvm_error:
                tvm_results = tvm_service.conjugate(tvm_params)
                if tvm_results:
                    for region in tvm_results:
                        if region not in results:
                            results[region] = {}
                        results[region].update(tvm_results[region])

        if results:
            log_request_response(request_params, results, '/api/conjugate')
            return jsonify(results)

    error = {"error": f"Infinitive {infinitive} not found in any module."}
    log_request_response(request_params, error, '/api/conjugate')
    return jsonify(error), 404

if __name__ == '__main__':
    app.run(debug=True)
