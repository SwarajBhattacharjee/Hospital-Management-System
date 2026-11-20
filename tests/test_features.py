"""
test_features.py
Automated unit and integration tests for Feature Flag implementation.
Verifies defaults, environment overrides, runtime toggling, API endpoint,
and conditional Jinja template UI banner rendering.
"""

import os
import pytest
from app.features import FeatureFlagManager, feature_flags


def test_feature_defaults():
    """Verify default states of registered feature flags."""
    manager = FeatureFlagManager()
    assert manager.is_enabled('EMERGENCY_TRIAGE_MODE') is False
    assert manager.is_enabled('TELEMEDICINE_PORTAL') is False
    assert manager.is_enabled('DARK_MODE_THEME') is True
    assert manager.is_enabled('PATIENT_EXPORT_CSV') is True


def test_feature_runtime_override():
    """Verify dynamic runtime feature toggle overriding."""
    manager = FeatureFlagManager()
    assert manager.is_enabled('EMERGENCY_TRIAGE_MODE') is False

    # Dynamically toggle ON
    manager.set_override('EMERGENCY_TRIAGE_MODE', True)
    assert manager.is_enabled('EMERGENCY_TRIAGE_MODE') is True

    # Dynamically toggle OFF
    manager.set_override('EMERGENCY_TRIAGE_MODE', False)
    assert manager.is_enabled('EMERGENCY_TRIAGE_MODE') is False

    # Clear overrides returns to default
    manager.clear_overrides()
    assert manager.is_enabled('EMERGENCY_TRIAGE_MODE') is False


def test_feature_environment_override(monkeypatch):
    """Verify environment variable overrides take precedence over defaults."""
    manager = FeatureFlagManager()
    
    # Simulate FEATURE_EMERGENCY_TRIAGE_MODE=true in environment
    monkeypatch.setenv('FEATURE_EMERGENCY_TRIAGE_MODE', 'true')
    assert manager.is_enabled('EMERGENCY_TRIAGE_MODE') is True

    # Simulate FEATURE_EMERGENCY_TRIAGE_MODE=0 in environment
    monkeypatch.setenv('FEATURE_EMERGENCY_TRIAGE_MODE', '0')
    assert manager.is_enabled('EMERGENCY_TRIAGE_MODE') is False


def test_feature_api_endpoint(client):
    """Verify REST API /api/features exposes active flag state."""
    response = client.get('/api/features')
    assert response.status_code == 200
    data = response.get_json()
    assert 'EMERGENCY_TRIAGE_MODE' in data
    assert 'TELEMEDICINE_PORTAL' in data
    assert 'DARK_MODE_THEME' in data


def test_feature_ui_rendering_when_disabled(client):
    """Verify Emergency Triage banner is absent when feature flag is disabled."""
    feature_flags.set_override('EMERGENCY_TRIAGE_MODE', False)
    response = client.get('/login')
    assert response.status_code == 200
    assert b'emergency-triage-banner' not in response.data
    feature_flags.clear_overrides()


def test_feature_ui_rendering_when_enabled(client):
    """Verify Emergency Triage banner is rendered in HTML when feature flag is enabled."""
    feature_flags.set_override('EMERGENCY_TRIAGE_MODE', True)
    response = client.get('/login')
    assert response.status_code == 200
    assert b'emergency-triage-banner' in response.data
    assert b'EMERGENCY TRIAGE PROTOCOL ACTIVATED' in response.data
    feature_flags.clear_overrides()

