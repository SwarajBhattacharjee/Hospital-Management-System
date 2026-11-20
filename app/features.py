"""
features.py
Feature flag management module for Hospital Management System.
Supports runtime feature toggling, environment-based configuration,
and conditional template context injection.
"""

import os
from typing import Dict, Any


class FeatureFlagManager:
    """
    Centralized feature flag evaluator supporting environment variable overrides
    and default values.
    """

    # Default feature toggles
    DEFAULTS: Dict[str, bool] = {
        'EMERGENCY_TRIAGE_MODE': False,
        'TELEMEDICINE_PORTAL': False,
        'MAINTENANCE_BANNER': False,
        'DARK_MODE_THEME': True,
        'PATIENT_EXPORT_CSV': True,
    }

    def __init__(self, app=None):
        self._overrides: Dict[str, bool] = {}
        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes feature flag context processor and registers API endpoint.
        """
        app.feature_flags = self

        # Context processor so Jinja2 templates can check {% if features.is_enabled('FLAG') %}
        @app.context_processor
        def inject_feature_flags():
            return {'features': self}

    def is_enabled(self, feature_name: str) -> bool:
        """
        Evaluates if a feature flag is enabled.
        Precedence:
        1. Runtime override
        2. Environment variable: FEATURE_<NAME> (case-insensitive, e.g. FEATURE_EMERGENCY_TRIAGE_MODE=1/true)
        3. Default value
        """
        key = feature_name.upper()

        # 1. Runtime override check
        if key in self._overrides:
            return self._overrides[key]

        # 2. Environment variable check
        env_var_name = f"FEATURE_{key}"
        env_val = os.environ.get(env_var_name)
        if env_val is not None:
            return env_val.strip().lower() in ('1', 'true', 'yes', 'on', 'enabled')

        # 3. Default fallback
        return self.DEFAULTS.get(key, False)

    def set_override(self, feature_name: str, enabled: bool):
        """Allows dynamic runtime overriding (useful for testing and admin toggle)."""
        self._overrides[feature_name.upper()] = bool(enabled)

    def clear_overrides(self):
        """Clears all runtime overrides."""
        self._overrides.clear()

    def get_all_flags(self) -> Dict[str, Any]:
        """Returns status of all registered feature flags."""
        return {k: self.is_enabled(k) for k in self.DEFAULTS}


# Global singleton instance
feature_flags = FeatureFlagManager()

