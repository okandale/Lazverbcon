import hmac
import hashlib
import logging
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)

class WebhookError(Exception):
    pass

class SignatureVerificationError(WebhookError):
    pass

class WebhookDisabledError(WebhookError):
    pass

class WebhookSignatureVerifier:
    def __init__(self, secret: str):
        self.secret = secret.encode()
    
    def verify(self, signature: Optional[str], payload: bytes) -> bool:
        if not signature or not signature.startswith('sha256='):
            return False
            
        expected = hmac.new(
            self.secret,
            payload,
            hashlib.sha256
        ).hexdigest()
        received = signature.replace('sha256=', '')
        
        return hmac.compare_digest(expected, received)

import threading
import time

class WebhookService:
    def handle_update(self) -> None:
        try:
            # Git pull
            result = subprocess.run(
                ['git', 'pull'],
                cwd=self.config.git_repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Git pull output: {result.stdout}")
            
            # Schedule the restart to happen after response is sent
            def delayed_restart():
                time.sleep(2)  # Wait 2 seconds
                subprocess.run(
                    ['sudo', 'systemctl', 'restart', 'flask-app.service'],
                    capture_output=True,
                    text=True,
                    check=True
                )
            
            thread = threading.Thread(target=delayed_restart)
            thread.daemon = True
            thread.start()
            
            logger.info("Service restart scheduled")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e.cmd}")
            logger.error(f"Output: {e.output}")
            raise WebhookError(f"Update failed: {e.output}")
    def __init__(self, config):
        self.config = config
        if config and config.enabled:
            self.signature_verifier = WebhookSignatureVerifier(config.secret)
        else:
            self.signature_verifier = None

    def handle_update(self) -> None:
        """Handle the actual git pull and service restart"""
        try:
            # Git pull
            result = subprocess.run(
                ['git', 'pull'],
                cwd='/var/www/webserver/Lazverbcon/laz_verb_conjugator/backend',
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Git pull output: {result.stdout}")
            
            # Restart service
            result = subprocess.run(
                ['sudo', 'systemctl', 'restart', 'flask-app.service'],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Service restart output: {result.stdout}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e.cmd}")
            logger.error(f"Output: {e.output}")
            raise WebhookError(f"Update failed: {e.output}")

    def verify_request(self, signature: Optional[str], payload: bytes, event_type: Optional[str]) -> None:
        if not self.config.enabled:
            raise WebhookDisabledError("Webhook functionality is disabled")
            
        if not self.signature_verifier.verify(signature, payload):
            raise SignatureVerificationError("Invalid signature")
            
        if event_type != 'push':
            raise WebhookError("Unsupported webhook event")