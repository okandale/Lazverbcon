from flask import Flask, request, jsonify
from flask_cors import CORS
import importlib
import logging
import os
import json

from flask_jwt_extended import JWTManager

from config.webhook_config import WebhookConfig
from services.webhook import WebhookService, WebhookError, SignatureVerificationError, WebhookDisabledError

from .admin import admin
from .verbs import verbs
from . import db  # Should fail if the database is not set.

# NEW: pure-function conjugation orchestration
from conjugation import conjugate_verb


# -----------------------
# Logging
# -----------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

req_res_logger = logging.getLogger("request_response")
req_res_logger.setLevel(logging.INFO)

os.makedirs("logs", exist_ok=True)

req_res_handler = logging.FileHandler("logs/request_response.log", encoding="utf-8")

req_res_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(message)s")
req_res_handler.setFormatter(formatter)

# Avoid adding duplicate handlers if this file is imported multiple times
if not any(isinstance(h, logging.FileHandler) and getattr(h, "baseFilename", "") == req_res_handler.baseFilename
           for h in req_res_logger.handlers):
    req_res_logger.addHandler(req_res_handler)


def log_request_response(request_params, response_data, endpoint):
    """Log request parameters and response data to the log file"""
    log_entry = {
        "endpoint": endpoint,
        "request": request_params,
        "response": response_data,
    }
    req_res_logger.info(json.dumps(log_entry, ensure_ascii=False))


# -----------------------
# App setup
# -----------------------
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"

# Register blueprints
app.register_blueprint(admin, url_prefix="/api/admin")
app.register_blueprint(verbs, url_prefix="/api/verbs")

# Useful for admin authentication.
jwt = JWTManager(app)

app.debug = True

# Enable CORS with specific configuration
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://lazuri.org",
                "http://lazuri.org",
                "https://lazverbcon.pages.dev",
                "http://localhost:5173",
            ],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)

# Initialize webhook configuration and service
webhook_config = WebhookConfig.load()
webhook_service = WebhookService(webhook_config)


# -----------------------
# Load tense modules
# -----------------------
tense_modules = {
    "ivd_present": importlib.import_module("notebooks.ivd_present"),
    "ivd_past": importlib.import_module("notebooks.ivd_past"),
    "ivd_pastpro": importlib.import_module("notebooks.ivd_pastpro"),
    "ivd_future": importlib.import_module("notebooks.ivd_future"),
    "tvm_tve_presentperf": importlib.import_module("notebooks.tvm_tve_presentperf"),
    "tvm_tve_potential": importlib.import_module("notebooks.tvm_tve_potential"),
    "tvm_tve_passive": importlib.import_module("notebooks.tvm_tve_passive"),
    "tvm_tense": importlib.import_module("notebooks.tvm_tense"),
    "tve_present": importlib.import_module("notebooks.tve_present"),
    "tve_pastpro": importlib.import_module("notebooks.tve_pastpro"),
    "tve_past": importlib.import_module("notebooks.tve_past"),
    "tve_future": importlib.import_module("notebooks.tve_future"),
}


# -----------------------
# Webhook endpoints
# -----------------------
@app.route("/update", methods=["POST"])
def webhook_update():
    try:
        webhook_service.verify_request(
            signature=request.headers.get("X-Hub-Signature-256"),
            payload=request.data,
            event_type=request.headers.get("X-GitHub-Event"),
        )

        webhook_service.handle_update()
        return jsonify({"status": "success"}), 200

    except WebhookDisabledError as e:
        logger.warning(str(e))
        return jsonify({"error": "Webhook disabled"}), 404

    except SignatureVerificationError as e:
        logger.warning(str(e))
        return jsonify({"error": "Invalid signature"}), 401

    except WebhookError as e:
        logger.warning(str(e))
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logger.error(f"Unexpected error in webhook: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/ping", methods=["GET"])
def hi():
    return jsonify({"response": "pong!"})


# -----------------------
# Conjugation endpoint (thin wrapper)
# -----------------------
def _bool_arg(name: str) -> bool:
    return (request.args.get(name, "") or "").lower() == "true"


@app.route("/api/conjugate", methods=["GET"])

def conjugate():
    # Keep raw request params for logging
    request_params = dict(request.args)

    infinitive = request.args.get("infinitive", "")
    tense = request.args.get("tense")
    aspect = request.args.get("aspect")
    obj = request.args.get("obj")

    applicative = _bool_arg("applicative")
    causative = _bool_arg("causative")
    simple_causative = _bool_arg("simple_causative")
    subject = request.args.get("subject", "all")
    optative = _bool_arg("optative")
    imperative = _bool_arg("imperative")
    neg_imperative = _bool_arg("neg_imperative")

    payload = conjugate_verb(
        tense_modules=tense_modules,
        infinitive=infinitive,
        tense=tense,
        aspect=aspect,
        obj=obj,
        subject=subject,
        optative=optative,
        imperative=imperative,
        neg_imperative=neg_imperative,
        applicative=applicative,
        causative=causative,
        simple_causative=simple_causative,
    )

    # Status logic: mirror your old behavior roughly
    status = 200
    result = payload.get("result", {})
    if isinstance(result, dict) and "error" in result:
        reason = (payload.get("meta") or {}).get("selected", {}).get("reason")
        status = 404 if reason == "not_found" else 400

    log_request_response(request_params, payload, "/api/conjugate")
    return jsonify(payload), status


if __name__ == "__main__":
    app.run(debug=True)
