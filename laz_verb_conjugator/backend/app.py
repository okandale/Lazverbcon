from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
import json

from backend.db_query import get_verb_id, get_conjugation_rows, reverse_lookup, reverse_suggestions
from flask_jwt_extended import JWTManager

from backend.config.webhook_config import WebhookConfig
from backend.services.webhook import (
    WebhookService,
    WebhookError,
    SignatureVerificationError,
    WebhookDisabledError,
)

from backend.admin import admin
from backend.verbs import verbs
from backend import db  # Should fail if the database is not set.


# -----------------------
# Logging
# -----------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

req_res_logger = logging.getLogger("request_response")
req_res_logger.setLevel(logging.INFO)

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

req_res_handler = logging.FileHandler(
    os.path.join(LOG_DIR, "request_response.log"),
    encoding="utf-8"
)
req_res_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(message)s")
req_res_handler.setFormatter(formatter)

if not any(
    isinstance(h, logging.FileHandler)
    and getattr(h, "baseFilename", "") == req_res_handler.baseFilename
    for h in req_res_logger.handlers
):
    req_res_logger.addHandler(req_res_handler)


def log_request_response(request_params, response_data, endpoint):
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

app.register_blueprint(admin, url_prefix="/api/admin")
app.register_blueprint(verbs, url_prefix="/api/verbs")

jwt = JWTManager(app)

app.debug = True

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://lazuri.org",
                "http://lazuri.org",
                "https://lazverbcon.pages.dev",
                "http://localhost:5173",
                "http://localhost:5174",
            ],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)

webhook_config = WebhookConfig.load()
webhook_service = WebhookService(webhook_config)


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
# Helpers
# -----------------------
def _bool_arg(name: str) -> bool:
    return (request.args.get(name, "") or "").lower() == "true"


# -----------------------
# Conjugation (DB-backed)
# -----------------------
@app.route("/api/conjugate", methods=["GET"])
def conjugate():
    request_params = dict(request.args)

    infinitive = request.args.get("infinitive", "").strip()
    tense = request.args.get("tense", "present")

    # Support both old frontend ("aspect", optative/imperative flags)
    # and newer frontend ("derivation", "mood")
    aspect = request.args.get("aspect", "")
    derivation = request.args.get("derivation")
    if not derivation:
        derivation = aspect if aspect in ("passive", "potential") else "none"

    mood = request.args.get("mood")
    optative = _bool_arg("optative")
    imperative = _bool_arg("imperative")
    neg_imperative = _bool_arg("neg_imperative")

    if not mood:
        if optative:
            mood = "optative"
        elif imperative:
            mood = "imperative"
        elif neg_imperative:
            mood = "negative_imperative"
        else:
            mood = "indicative"

    is_applicative = _bool_arg("applicative")
    is_causative = _bool_arg("simple_causative")
    is_double_causative = _bool_arg("causative")

    subject = request.args.get("subject", "all")
    obj = request.args.get("obj", "")
    region_csv = request.args.get("region", "")

    if not infinitive:
        payload = {
            "error": "Missing infinitive"
        }
        log_request_response(request_params, payload, "/api/conjugate")
        return jsonify(payload), 400

    # Your actual DB mapping
    dialects = {
        1: "AŞ",
        2: "PZ",
        3: "FA",
        4: "HO",
    }

    selected_region_codes = []
    if region_csv.strip():
        selected_region_codes = [r.strip() for r in region_csv.split(",") if r.strip()]

    if selected_region_codes:
        dialects = {
            dialect_id: code
            for dialect_id, code in dialects.items()
            if code in selected_region_codes
        }

    frames = ["Dative", "Ergative", "Nominative"]
    results = {}

    for dialect_id, dialect_code in dialects.items():
        verb_id = get_verb_id(infinitive, dialect_id)
        if verb_id is None:
            continue

        results[dialect_code] = {}

        for frame in frames:
            rows = get_conjugation_rows(
                verb_id=verb_id,
                tense=tense,
                frame=frame,
                mood=mood,
                derivation=derivation,
                is_applicative=is_applicative,
                is_causative=is_causative,
                is_double_causative=is_double_causative,
                subject_filter=subject,
                object_filter=obj,
            )

            forms = []
            for r in rows:
                form = r["spelling"]
                if r["optional_prefix"]:
                    form = f"{r['optional_prefix']} {form}"

                forms.append({
                    "subject": r["subject"],
                    "object": r["object"],
                    "subject_code": r["subject_code"],
                    "object_code": r["object_code"],
                    "conjugation": form
                })

            results[dialect_code][frame] = forms

    if not results:
        payload = {
            "error": "Verb not found"
        }
        log_request_response(request_params, payload, "/api/conjugate")
        return jsonify(payload), 404

    payload = {
        "result": results,
        "meta": {
            "selected": {
                "tense": tense,
                "mood": mood,
                "derivation": derivation,
                "subject": subject,
                "object": obj,
                "regions": selected_region_codes,
                "is_applicative": is_applicative,
                "is_causative": is_causative,
                "is_double_causative": is_double_causative,
            }
        }
    }

    log_request_response(request_params, payload, "/api/conjugate")
    return jsonify(payload), 200


# -----------------------
# Reverse lookup
# -----------------------

# -----------------------
# Reverse lookup
# -----------------------
@app.route("/api/reverse", methods=["GET"])
def reverse():
    request_params = dict(request.args)

    spelling = request.args.get("spelling", "").strip()

    if not spelling:
        payload = {"error": "Missing spelling"}
        log_request_response(request_params, payload, "/api/reverse")
        return jsonify(payload), 400

    matches = reverse_lookup(spelling)
    match_type = matches[0].get("match_type", "exact") if matches else "none"

    payload = {
        "query": spelling,
        "match_type": match_type,
        "matches": matches,
    }

    log_request_response(request_params, payload, "/api/reverse")
    return jsonify(payload), 200


@app.route("/api/reverse/suggestions", methods=["GET"])
def reverse_suggestions_route():
    request_params = dict(request.args)

    q = request.args.get("q", "").strip()

    if not q:
        payload = {"suggestions": []}
        log_request_response(request_params, payload, "/api/reverse/suggestions")
        return jsonify(payload), 200

    suggestions = reverse_suggestions(q)

    payload = {"suggestions": suggestions}
    log_request_response(request_params, payload, "/api/reverse/suggestions")
    return jsonify(payload), 200
# -----------------------
# Run
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)