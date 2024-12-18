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
app.debug = False

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

@app.route('/api/conjugate', methods=['GET'])
def conjugate():
    # Capture request parameters
    request_params = dict(request.args)
    
    validator = ConjugationValidator(
        tense_modules, 
        simplified_tense_mapping,
        simplified_aspect_mapping
    )
    
    # Run all validations
    params, error = validator.validate_request(request_params)
    if error:
        error_response, status_code = error
        log_request_response(request_params, error_response, '/api/conjugate')
        return jsonify(error_response), status_code

    conjugation_service = ConjugationService(
        tense_modules, 
        simplified_tense_mapping,
        simplified_aspect_mapping
    )

    try:
        conjugations = conjugation_service.conjugate(params)
        if conjugations is None:
            error = {"error": f"Infinitive {params['infinitive']} not found in any module."}
            log_request_response(request_params, error, '/api/conjugate')
            return jsonify(error), 404

        log_request_response(request_params, conjugations, '/api/conjugate')
        return jsonify(conjugations)

    except ValueError as e:
        error = {"error": str(e)}
        log_request_response(request_params, error, '/api/conjugate')
        return jsonify(error), 400
    except Exception as e:
        error = {"error": str(e)}
        log_request_response(request_params, error, '/api/conjugate')
        return jsonify(error), 500

if __name__ == '__main__':
    app.run()