"""
Tag management module for dashboard integration
This module provides tag information for the test suite dashboard
"""
from tests.base.base_test import TestTags
from flask import jsonify

def get_tags_for_dashboard():
    """
    Get all tags organized for dashboard display
    Returns a dictionary with test types and their associated tags
    """
    return {
        'smoke': {
            'display_name': 'Smoke Tests',
            'description': 'Quick validation of critical functionality',
            'tags': TestTags.SMOKE_TAGS
        },
        'regression': {
            'display_name': 'Regression Tests', 
            'description': 'Comprehensive validation of all functionality',
            'tags': TestTags.REGRESSION_TAGS
        },
        'api': {
            'display_name': 'API Tests',
            'description': 'API endpoint and integration testing',
            'tags': {**TestTags.API_TAGS, **TestTags.SMOKE_TAGS}
        },
        'ui': {
            'display_name': 'UI Tests',
            'description': 'User interface and interaction testing', 
            'tags': {**TestTags.UI_TAGS, **TestTags.SMOKE_TAGS}
        }
    }

def generate_pytest_command(test_type, selected_tags=None, env='dev', browser='chrome'):
    """
    Generate pytest command based on test type and selected tags
    """
    base_commands = {
        'smoke': 'python -m pytest tests/smoke_tests/',
        'regression': 'python -m pytest tests/regression_tests/',
        'api': 'python -m pytest -m api',
        'ui': 'python -m pytest -m ui'
    }
    
    if test_type not in base_commands:
        return None
    
    cmd = base_commands[test_type]
    cmd += f' --env={env} --browser={browser}'
    
    if selected_tags:
        tag_expressions = [f"({test_type} and {tag})" for tag in selected_tags]
        combined_expression = ' or '.join(tag_expressions)
        cmd += f' -m "{combined_expression}"'
    
    cmd += ' --html=reports/test_report.html --alluredir=allure-results -v'
    return cmd
