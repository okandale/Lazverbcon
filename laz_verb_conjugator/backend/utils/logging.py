import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
import json
from typing import Any, Dict, Optional
from ..config.base_config import LazuriConfig

class LazuriLogger:
    """Custom logger for Lazuri conjugator."""
    
    def __init__(self, name: str = 'lazuri'):
        self.config = LazuriConfig()
        self.logger = logging.getLogger(name)
        self._setup_logger()
        
    def _setup_logger(self) -> None:
        """Configure the logger based on configuration."""
        # Get config values
        log_level = self.config.get('logging.level', 'INFO')
        log_format = self.config.get('logging.format',
                                   '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_file = self.config.get('logging.file', 'logs/lazuri.log')
        
        # Set basic configuration
        self.logger.setLevel(getattr(logging, log_level))
        formatter = logging.Formatter(log_format)
        
        # Create logs directory if it doesn't exist
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # File handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _format_log_message(self, message: str, extra: Optional[Dict[str, Any]] = None) -> str:
        """Format log message with extra data if provided."""
        if not extra:
            return message
            
        try:
            extra_formatted = json.dumps(extra, ensure_ascii=False)
            return f"{message} | Extra Data: {extra_formatted}"
        except Exception:
            return message

    def conjugation_request(self, infinitive: str, params: Dict[str, Any]) -> None:
        """Log a conjugation request."""
        extra = {
            'verb': infinitive,
            'parameters': params,
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(
            self._format_log_message(f"Conjugation requested for: {infinitive}", extra)
        )

    def conjugation_result(self, infinitive: str, result: Dict[str, Any]) -> None:
        """Log a conjugation result."""
        extra = {
            'verb': infinitive,
            'result_summary': {
                'regions': list(result.keys()),
                'forms_count': sum(len(forms) for forms in result.values())
            },
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(
            self._format_log_message(f"Conjugation completed for: {infinitive}", extra)
        )

    def conjugation_error(self, infinitive: str, error: Exception, 
                         context: Optional[Dict[str, Any]] = None) -> None:
        """Log a conjugation error."""
        extra = {
            'verb': infinitive,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'timestamp': datetime.now().isoformat()
        }
        self.logger.error(
            self._format_log_message(f"Error conjugating: {infinitive}", extra),
            exc_info=True
        )

    def data_load_error(self, file_path: str, error: Exception) -> None:
        """Log a data loading error."""
        extra = {
            'file': file_path,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': datetime.now().isoformat()
        }
        self.logger.error(
            self._format_log_message(f"Error loading data from: {file_path}", extra),
            exc_info=True
        )

    def validation_error(self, infinitive: str, validation_issues: Dict[str, str]) -> None:
        """Log validation errors."""
        extra = {
            'verb': infinitive,
            'validation_issues': validation_issues,
            'timestamp': datetime.now().isoformat()
        }
        self.logger.warning(
            self._format_log_message(f"Validation failed for: {infinitive}", extra)
        )

    def cache_operation(self, operation: str, key: str, success: bool) -> None:
        """Log cache operations."""
        extra = {
            'operation': operation,
            'key': key,
            'success': success,
            'timestamp': datetime.now().isoformat()
        }
        self.logger.debug(
            self._format_log_message(f"Cache {operation}: {key}", extra)
        )

    def performance_metric(self, operation: str, duration_ms: float, 
                         context: Optional[Dict[str, Any]] = None) -> None:
        """Log performance metrics."""
        extra = {
            'operation': operation,
            'duration_ms': duration_ms,
            'context': context,
            'timestamp': datetime.now().isoformat()
        }
        self.logger.info(
            self._format_log_message(
                f"Performance metric - {operation}: {duration_ms}ms",
                extra
            )
        )