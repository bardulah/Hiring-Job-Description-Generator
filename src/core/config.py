"""
Configuration management system.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from .exceptions import ConfigurationError


class Config:
    """Configuration manager for the hiring system."""

    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._config:
            self.load_config()

    def load_config(self, config_path: Optional[str] = None):
        """Load configuration from YAML file."""
        if config_path is None:
            # Try environment variable first
            config_path = os.getenv('HIRING_SYSTEM_CONFIG')

            if config_path is None:
                # Use default config
                base_dir = Path(__file__).parent.parent.parent
                config_path = base_dir / 'config' / 'default.yaml'

        try:
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        except FileNotFoundError:
            raise ConfigurationError(f"Configuration file not found: {config_path}")
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML in configuration file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Example:
            config.get('analysis.min_job_descriptions')
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """Set configuration value using dot notation."""
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration."""
        return self._config.copy()

    def reload(self):
        """Reload configuration from file."""
        self._config = {}
        self.load_config()

    # Convenience properties
    @property
    def analysis_config(self) -> Dict[str, Any]:
        """Get analysis configuration."""
        return self.get('analysis', {})

    @property
    def generation_config(self) -> Dict[str, Any]:
        """Get generation configuration."""
        return self.get('generation', {})

    @property
    def interview_config(self) -> Dict[str, Any]:
        """Get interview configuration."""
        return self.get('interview', {})

    @property
    def timeline_config(self) -> Dict[str, Any]:
        """Get timeline configuration."""
        return self.get('timeline', {})

    @property
    def output_config(self) -> Dict[str, Any]:
        """Get output configuration."""
        return self.get('output', {})

    @property
    def api_config(self) -> Dict[str, Any]:
        """Get API configuration."""
        return self.get('api', {})

    @property
    def cache_config(self) -> Dict[str, Any]:
        """Get cache configuration."""
        return self.get('cache', {})

    @property
    def logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self.get('logging', {})

    @property
    def analytics_config(self) -> Dict[str, Any]:
        """Get analytics configuration."""
        return self.get('analytics', {})


# Global config instance
config = Config()
