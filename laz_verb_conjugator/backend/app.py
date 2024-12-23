from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import importlib
import logging
import os
import json
from datetime import datetime
from flask import make_response
from validators import ConjugationValidator
from services import ConjugationService

# Set up two loggers - one for general application logs and one for request/response logs
logging.basicConfig(level=logging.DEBUG)
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

app = Flask(__name__, static_folder='../frontend/dist')

# Enable CORS with specific configuration
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://lazuri.org",
            "http://lazuri.org",
            "https://lazverbcon.pages.dev",
        ],
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

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

def log_request_response(request_params, response_data, endpoint):
    """
    Log request parameters and response data to the log file
    """
    log_entry = {
        'request': request_params,
        'response': response_data
    }
    req_res_logger.info(json.dumps(log_entry, ensure_ascii=False))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/ping', methods=['GET'])
def hi():
    return jsonify({"response": "pong"})

def check_verb_existence(infinitive, tense_modules):
    """
    Check if a verb exists in IVD and/or TVE modules
    Returns: (bool, bool) - (exists_in_ivd, exists_in_tve)
    """
    logger.debug(f"Starting detailed verb check for infinitive: {infinitive}")
    
    # Check IVD verbs
    exists_in_ivd = False
    ivd_modules = ['ivd_present', 'ivd_past', 'ivd_pastpro', 'ivd_future']
    for module_name in ivd_modules:
        if hasattr(tense_modules[module_name], 'verbs'):
            verbs = tense_modules[module_name].verbs
            if infinitive in verbs:
                logger.debug(f"Found {infinitive} in {module_name} verbs dictionary")
                exists_in_ivd = True
                break
    
    # Check TVE verbs
    exists_in_tve = False
    tve_modules = ['tve_present', 'tve_past', 'tve_pastpro', 'tve_future']
    for module_name in tve_modules:
        if hasattr(tense_modules[module_name], 'verbs'):
            verbs = tense_modules[module_name].verbs
            if infinitive in verbs:
                logger.debug(f"Found {infinitive} in {module_name} verbs dictionary")
                exists_in_tve = True
                break
    
    logger.debug(f"Final result for {infinitive} - IVD: {exists_in_ivd}, TVE: {exists_in_tve}")
    return exists_in_ivd, exists_in_tve

@app.route('/api/conjugate', methods=['GET'])
def conjugate():
    # 1. Capture request parameters
    request_params = dict(request.args)
    infinitive = request_params.get('infinitive')
    
    logger.debug("1. Starting conjugation for infinitive: %s", infinitive)
    logger.debug("2. Full request params: %s", request_params)
    
    # 2. Basic checks
    if not infinitive:
        error_response = {"error": "Infinitive is required"}
        log_request_response(request_params, error_response, '/api/conjugate')
        return jsonify(error_response), 400

    # Special check for "guri mentxu"
    if infinitive == 'guri mentxu' and request_params.get('aspect') != 'potential':
        error_response = {
            "error": "This verb only exists in potential form. You need to select the potential form under 'Aspect' / "
                     "Bu fiil yalnızca yeterlilik kipinde vardır. 'Görünüş' altında yeterlilik kipini seçmeniz gerekiyor."
        }
        log_request_response(request_params, error_response, '/api/conjugate')
        return jsonify(error_response), 400

    # 3. Check if any markers are selected
    has_markers = any(request_params.get(marker) == 'true'
                      for marker in ['applicative', 'causative', 'optative'])

    # 4. Check verb existence and type
    exists_in_ivd, exists_in_tve = check_verb_existence(infinitive, tense_modules)
    
    # If it's EXCLUSIVELY an IVD verb (exists in IVD but NOT in TVE) and has markers, return error
    if exists_in_ivd and not exists_in_tve and has_markers:
        error_response = {
            "error": "This verb belongs to a verb group that cannot take additional markers "
                     "(applicative, causative, or optative) / "
                     "Bu fiil, ek işaretleyiciler (ettirgen, uygulamalı veya istek kipi) "
                     "alamayan bir fiil grubuna aittir."
        }
        log_request_response(request_params, error_response, '/api/conjugate')
        return jsonify(error_response), 400

    # 5. Prepare separate tense mappings for IVD and TVE
    ivd_mapping = {}
    tve_mapping = {}
    
    for tense, modules in simplified_tense_mapping.items():
        # modules can be a list or a single object, so check carefully
        if isinstance(modules, list):
            # separate out the modules that start with 'ivd_' vs. 'tve_' or are tuples (for tvm_tense)
            ivd_modules = [
                m for m in modules
                if isinstance(m, str) and m.startswith('ivd_')
            ]
            tvex_modules = [
                m for m in modules
                if (isinstance(m, tuple) or (isinstance(m, str) and m.startswith('tve_')))
            ]
            
            # Only assign the IVD mapping if the verb actually exists in IVD and no markers
            if ivd_modules and exists_in_ivd and not has_markers:
                ivd_mapping[tense] = ivd_modules
            
            # Assign TVE mapping if the verb exists in TVE
            if tvex_modules and exists_in_tve:
                tve_mapping[tense] = tvex_modules

        else:
            # If modules is not a list, you can decide if/how to handle it. For simplicity:
            pass

    # 6. Create a combined results dict
    results = {}

    # 7. IVD phase (only if exists_in_ivd and !has_markers)
    if exists_in_ivd and not has_markers:
        ivd_validator = ConjugationValidator(tense_modules, ivd_mapping, {})
        ivd_service = ConjugationService(tense_modules, ivd_mapping, {})
        ivd_params, ivd_error = ivd_validator.validate_request(request_params)
        
        if not ivd_error:
            ivd_results = ivd_service.conjugate(ivd_params)
            if ivd_results:
                # Just put them directly under results
                results.update(ivd_results)

    # 8. TVE phase (if exists_in_tve)
    if exists_in_tve:
        tve_validator = ConjugationValidator(tense_modules, tve_mapping, simplified_aspect_mapping)
        tve_service = ConjugationService(tense_modules, tve_mapping, simplified_aspect_mapping)
        tve_params, tve_error = tve_validator.validate_request(request_params)
        
        if not tve_error:
            tve_results = tve_service.conjugate(tve_params)
            if tve_results:
                # Merge them carefully so they don't overwrite any IVD keys
                for region in tve_results:
                    if region not in results:
                        results[region] = {}
                    results[region].update(tve_results[region])

    # 9. If we didn’t get any results from either approach, return 404
    if not results:
        error = {"error": f"Infinitive {infinitive} not found in any module."}
        log_request_response(request_params, error, '/api/conjugate')
        return jsonify(error), 404

    # 10. Otherwise, return everything
    log_request_response(request_params, results, '/api/conjugate')
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
