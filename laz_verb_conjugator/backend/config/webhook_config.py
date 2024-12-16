from dataclasses import dataclass
import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

# Define the config path directly here
WEBHOOK_CONFIG_PATH = os.getenv('WEBHOOK_CONFIG_PATH', '/var/www/webserver/config/webhook_config.json')
@dataclass
class WebhookConfig:
    secret: str
    git_repo_path: str
    service_name: str
    enabled: bool = True

    @classmethod
    def load(cls) -> Optional['WebhookConfig']:
        try:
            logger.info(f"Loading webhook config from {WEBHOOK_CONFIG_PATH}")
            with open(WEBHOOK_CONFIG_PATH, 'r') as f:
                config = json.load(f)
                
            required_fields = ['webhook_secret', 'git_repo_path', 'service_name']
            # Don't remove 'webhook_' prefix when checking
            missing_fields = [field for field in required_fields if field not in config]
            
            if missing_fields:
                logger.critical(f"Missing required config fields: {', '.join(missing_fields)}")
                return None

            return cls(
                secret=config['webhook_secret'],  # Get the full field name
                git_repo_path=config['git_repo_path'],
                service_name=config['service_name'],
                enabled=config.get('webhook_enabled', True)
            )
        except FileNotFoundError:
            logger.critical(f"Webhook config file not found at {WEBHOOK_CONFIG_PATH}")
            return None
        except json.JSONDecodeError:
            logger.critical("Webhook config file is not valid JSON")
            return None
        except Exception as e:
            logger.critical(f"Unexpected error loading webhook config: {e}")
            return None