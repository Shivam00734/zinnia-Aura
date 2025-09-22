from flask import Flask, render_template_string, request, jsonify, send_from_directory, abort
from flask_socketio import SocketIO, emit
import os
import json
import subprocess
from datetime import datetime
from jsonschema import validate as jsonschema_validate, ValidationError
import requests
import pandas as pd
import typing as t
import re as _re_for_paths
import io as _io_for_excel
import shutil
import threading
import queue
import sys
import time
import platform

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zinnia_dashboard_secret_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Cross-platform subprocess execution with real-time output
def execute_command_with_realtime_output(cmd, env=None, working_dir=None, emit_to_websocket=True):
    """
    Execute command with real-time output capture that works on both Windows and Unix
    Returns: (stdout_lines, stderr_lines, return_code)
    """
    stdout_lines = []
    stderr_lines = []
    
    try:
        # Use universal_newlines for cross-platform compatibility
        process = subprocess.Popen(
            cmd, 
            env=env, 
            cwd=working_dir,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            universal_newlines=True,
            bufsize=1  # Line buffered
        )
        
        # Use threading to handle stdout and stderr simultaneously
        stdout_queue = queue.Queue()
        stderr_queue = queue.Queue()
        
        def read_stdout():
            try:
                for line in process.stdout:
                    stdout_queue.put(line.rstrip())
                stdout_queue.put(None)  # Signal end
            except Exception as e:
                stdout_queue.put(f"STDOUT_ERROR: {e}")
                stdout_queue.put(None)
        
        def read_stderr():
            try:
                for line in process.stderr:
                    stderr_queue.put(line.rstrip())
                stderr_queue.put(None)  # Signal end
            except Exception as e:
                stderr_queue.put(f"STDERR_ERROR: {e}")
                stderr_queue.put(None)
        
        stdout_thread = threading.Thread(target=read_stdout)
        stderr_thread = threading.Thread(target=read_stderr)
        
        stdout_thread.start()
        stderr_thread.start()
        
        stdout_done = False
        stderr_done = False
        
        # Collect output with real-time logging
        while not (stdout_done and stderr_done):
            try:
                # Check stdout
                if not stdout_done:
                    try:
                        line = stdout_queue.get(timeout=0.1)
                        if line is None:
                            stdout_done = True
                        else:
                            stdout_lines.append(line)
                            print(f"STDOUT: {line}")  # Real-time console output
                            if emit_to_websocket:
                                try:
                                    socketio.emit('terminal_output', {'type': 'stdout', 'data': line})
                                except Exception:
                                    pass  # Ignore WebSocket errors
                    except queue.Empty:
                        pass
                
                # Check stderr
                if not stderr_done:
                    try:
                        line = stderr_queue.get(timeout=0.1)
                        if line is None:
                            stderr_done = True
                        else:
                            stderr_lines.append(line)
                            print(f"STDERR: {line}")  # Real-time console output
                            if emit_to_websocket:
                                try:
                                    socketio.emit('terminal_output', {'type': 'stderr', 'data': line})
                                except Exception:
                                    pass  # Ignore WebSocket errors
                    except queue.Empty:
                        pass
                        
            except KeyboardInterrupt:
                print("Execution interrupted by user")
                process.terminate()
                break
        
        # Wait for threads to complete
        stdout_thread.join(timeout=5)
        stderr_thread.join(timeout=5)
        
        # Wait for process to complete
        return_code = process.wait()
        
        return stdout_lines, stderr_lines, return_code
        
    except Exception as e:
        error_msg = f"Command execution failed: {e}"
        print(error_msg)
        return [error_msg], [], 1

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('status', {'msg': 'Connected to terminal stream'})
    print("Client connected to terminal stream")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print("Client disconnected from terminal stream")

@socketio.on('start_execution')
def handle_start_execution():
    """Handle start of test execution"""
    emit('terminal_output', {'type': 'info', 'data': '=== Test execution started ==='})

@socketio.on('clear_terminal')
def handle_clear_terminal():
    """Handle terminal clear request"""
    emit('terminal_clear', {})

# # -------- Excel Comparison Helpers --------
# def get_from_path(data: t.Any, path: str) -> t.Any:
#     """
#     Dot/bracket path lookup like 'a.b[0].c'. Use '.' or empty to refer to full object.
#     """
#     if path in (None, "", "."):
#         return data
#     cur = data
#     tokens = _re_for_paths.findall(r"[^\.\[\]]+|\[\d+\]", path)
#     for tok in tokens:
#         if tok.startswith('[') and tok.endswith(']'):
#             idx = int(tok[1:-1])
#             cur = cur[idx]
#         else:
#             cur = cur[tok]
#     return cur

# def compare_value(actual: t.Any, comparator: str, expected_raw: str) -> t.Tuple[bool, str]:
#     """
#     Supported comparators: eq, neq, gt, gte, lt, lte, contains, not_contains, regex, jsonschema, exists, not_exists
#     """
#     expected = expected_raw
#     try:
#         if comparator in {"eq","neq","contains","not_contains","jsonschema"}:
#             if comparator == "jsonschema":
#                 expected = json.loads(expected_raw)
#         else:
#             expected = float(expected_raw)
#     except Exception:
#         pass

#     try:
#         if comparator == "eq":
#             return (actual == expected, f"{actual} == {expected}")
#         if comparator == "neq":
#             return (actual != expected, f"{actual} != {expected}")
#         if comparator == "gt":
#             return (float(actual) > float(expected), f"{actual} > {expected}")
#         if comparator == "gte":
#             return (float(actual) >= float(expected), f"{actual} >= {expected}")
#         if comparator == "lt":
#             return (float(actual) < float(expected), f"{actual} < {expected}")
#         if comparator == "lte":
#             return (float(actual) <= float(expected), f"{actual} <= {expected}")
#         if comparator == "contains":
#             return (str(expected) in str(actual), f"{expected} in {actual}")
#         if comparator == "not_contains":
#             return (str(expected) not in str(actual), f"{expected} not in {actual}")
#         if comparator == "regex":
#             return (_re_for_paths.search(expected_raw, str(actual)) is not None, f"regex({expected_raw}) ~= {actual}")
#         if comparator == "exists":
#             return (actual is not None, "exists")
#         if comparator == "not_exists":
#             return (actual is None, "not_exists")
#         if comparator == "jsonschema":
#             jsonschema_validate(actual, expected)
#             return (True, "jsonschema: valid")
#     except ValidationError as ve:
#         return (False, f"jsonschema: {ve.message}")
#     except Exception as e:
#         return (False, f"comparison error: {e}")

#     return (False, f"unknown comparator: {comparator}")
# # -----------------------------------------



# Load API configuration
try:
    with open('tests/api_config.json', 'r') as f:
        api_config = json.load(f)
except FileNotFoundError:
    api_config = {
        "regions": {"QA": "https://qa-lcapi.se2.com", "UAT": "http://uat-lcapi.zinnia.com"},
        "apis": []
    }

# Get all Robot Framework test files
def get_api_tests():
    test_files = []
    api_test_dir = 'tests/api'
    for root, _, files in os.walk(api_test_dir):
        for file in files:
            if file.endswith('.robot'):
                test_files.append({
                    'name': os.path.splitext(file)[0].replace('_', ' ').title(),
                    'path': os.path.join(root, file),
                    'type': 'Robot'
                })
    return sorted(test_files, key=lambda x: x['name'])

# Group APIs by type
def group_apis_by_type():
    api_types = {}
    for api in api_config['apis']:
        api_type = api.get('api_type', 'Other')
        if api_type not in api_types:
            api_types[api_type] = []
        api_types[api_type].append(api)
    return api_types

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Zinnia Live-Aura Dashboard</title>
    <meta name="viewport" content="width=1200, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --zinnia-blue: #1a237e;
            --zinnia-gold: #ffd700;
            --zinnia-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        html {
            font-size: 16px;
        }
        
        body {
            margin: 0;
            padding: 0;
            font-family: 'Montserrat', sans-serif;
            background: #f0f2f5;
            display: flex;
            transform: scale(2);
            transform-origin: 0 0;
            width: 50vw;
            height: 50vh;
        }

        .sidebar {
            width: 250px;
            height: 100vh;
            background: white;
            position: fixed;
            left: 0;
            top: 0;
            box-shadow: var(--zinnia-shadow);
            display: flex;
            flex-direction: column;
            z-index: 100;
        }

        .sidebar-title {
            padding: 20px;
            font-size: 1rem;
            font-weight: 600;
            color: var(--zinnia-blue);
            border-bottom: 2px solid var(--zinnia-gold);
        }

        .sidebar-menu {
            list-style: none;
            padding: 0;
            margin: 0;
            flex-grow: 1;
        }

        .sidebar-menu li {
            padding: 0;
        }

        .sidebar-menu a {
            display: block;
            padding: 15px 20px;
            color: #333;
            text-decoration: none;
            transition: all 0.2s;
        }

        .sidebar-menu a:hover {
            background: #f0f2f5;
            color: var(--zinnia-blue);
        }

        .sidebar-menu a.active {
            background: #e8f0fe;
            color: var(--zinnia-blue);
            border-left: 4px solid var(--zinnia-blue);
        }

        .sidebar-footer {
            padding: 20px;
            text-align: center;
            font-size: 0.8em;
            color: #666;
            border-top: 1px solid #eee;
        }

        .main-content {
            margin-left: 250px;
            padding: 20px;
            width: calc(100% - 250px);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: white;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: var(--zinnia-shadow);
        }

        .header-inner {
            max-width: 1200px;
            margin: 0 auto;
        }

        .project-title {
            font-size: 1.5em;
            font-weight: 600;
            color: var(--zinnia-blue);
        }

        .gold-bar {
            height: 4px;
            background: var(--zinnia-gold);
            margin-top: 10px;
        }

        .card {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: var(--zinnia-shadow);
        }

        h2 {
            color: var(--zinnia-blue);
            margin-top: 0;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #333;
        }

        select, input {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e7ef;
            border-radius: 6px;
            font-family: inherit;
        }

        button {
            background: var(--zinnia-blue);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
        }

        button:hover {
            background: #283593;
            transform: translateY(-2px);
        }
        .api-section {
            margin-bottom: 30px;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: var(--zinnia-shadow);
        }
        .api-type-section {
            margin-bottom: 20px;
        }
        .api-type-title {
            font-size: 1.1em;
            font-weight: 600;
            color: var(--zinnia-blue);
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 2px solid var(--zinnia-gold);
        }
        .api-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }
        .api-card {
            background: #f8fafc;
            border: 2px solid #e0e7ef;
            border-radius: 8px;
            padding: 15px;
            transition: all 0.2s;
        }
        .api-card:hover {
            border-color: var(--zinnia-blue);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(26,35,126,0.1);
        }
        .api-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .api-name {
            font-weight: 600;
            color: var(--zinnia-blue);
        }
        .api-method-badge {
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75em;
            font-weight: 600;
            background: #e0e7ef;
            color: var(--zinnia-blue);
        }
        .api-details {
            font-size: 0.9em;
            color: #666;
            margin-top: 8px;
        }
        .api-endpoint {
            font-family: monospace;
            background: #f1f5f9;
            padding: 8px;
            border-radius: 4px;
            font-size: 0.85em;
            margin: 8px 0;
            word-break: break-all;
        }
        .test-section {
            margin-top: 30px;
        }
        .test-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
        }
        .test-card {
            background: #f8fafc;
            border: 2px solid #e0e7ef;
            border-radius: 8px;
            padding: 15px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .test-card:hover {
            border-color: var(--zinnia-blue);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(26,35,126,0.1);
        }
        .test-card.selected {
            background: #e8f0fe;
            border-color: var(--zinnia-blue);
        }
                /* Terminal Display Styles */
                .terminal-section {
                    margin-top: 30px;
                    background: white;
                    border-radius: 12px;
                    box-shadow: var(--zinnia-shadow);
                    overflow: hidden;
                }
                
                .terminal-header {
                    background: var(--zinnia-blue);
                    color: white;
                    padding: 15px 20px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .terminal-title {
                    font-weight: 600;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                
                .terminal-controls {
                    display: flex;
                    gap: 10px;
                }
                
                .terminal-btn {
                    background: rgba(255,255,255,0.2);
                    border: none;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 0.8em;
                }
                
                .terminal-btn:hover {
                    background: rgba(255,255,255,0.3);
                }
                
                .terminal-display {
                    background: #1e1e1e;
                    color: #f0f0f0;
                    font-family: 'Consolas', 'Monaco', monospace;
                    font-size: 13px;
                    line-height: 1.4;
                    padding: 20px;
                    height: 400px;
                    overflow-y: auto;
                    border: none;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }
                
                .terminal-line {
                    margin-bottom: 2px;
                }
                
                .terminal-stdout {
                    color: #4CAF50;
                }
                
                .terminal-stderr {
                    color: #f44336;
                }
                
                .terminal-info {
                    color: #2196F3;
                }
                
                .status-indicator {
                    display: inline-block;
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    margin-right: 8px;
                }
                
                .status-connected {
                    background: #4CAF50;
                }
                
                .status-disconnected {
                    background: #f44336;
                }
                
                .terminal-hidden {
                    display: none;
                }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-title">Menu</div>
        <ul class="sidebar-menu">
            <li><a href="/" class="active">API Testing</a></li>
            <li><a href="/performance">API Performance</a></li>
            <li><a href="/reports">All Reports</a></li>
        </ul>
        <div class="sidebar-footer">&copy; 2025 Zinnia Dashboard</div>
    </div>
    
    <div class="main-content">
        <div class="header">
            <div class="header-inner">
                <div class="project-title">Zinnia Live-Aura Dashboard</div>
            </div>
            <div class="gold-bar"></div>
        </div>
        <div class="container">
            <div class="card">
                <h2>Configuration</h2>
                <form id="testForm" method="post" action="/run-tests" onsubmit="return validateForm()" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="region">Environment</label>
                        <select id="region" name="region" required>
                            {% for region, url in regions.items() %}
                                <option value="{{ region }}">{{ region }} ({{ url }})</option>
                            {% endfor %}
                        </select>
                    </div>

                    {#
                    {#
                    <div class="api-section">
                        <h3>Available APIs</h3>
                        {% for api_type, apis in grouped_apis.items() %}
                        <div class="api-type-section" data-api-type="{{ api_type }}">
                            
                            <div class="api-grid">
                                {% for api in apis %}
                                <div class="api-card">
                                    <div class="api-header">
                                        <span class="api-name">{{ api.name }}</span>
                                        <span class="api-method-badge">{{ api.method }}</span>
                                    </div>
                                    <div class="api-endpoint">{{ api.endpoint }}</div>
                                    <div class="api-details">
                                        <div>
                                            <input type="checkbox" 
                                                   name="selected_apis" 
                                                   value="{{ api.name }}"
                                                   id="api_{{ api_type }}_{{ loop.index }}"
                                                   class="api-checkbox"
                                                   onchange="updateApiCard(this)">
                                            <label for="api_{{ api_type }}_{{ loop.index }}">Include in Test</label>
                                        </div>
                                    </div>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    #}
                    
                    
                    <div class="test-section">
                        <h3>Available Test Suites</h3>
                        <div class="test-grid">
                            {% for test in api_tests %}
                            <div class="test-card" onclick="toggleTest(this)">
                                <div class="test-name">{{ test.name }}</div>
                                <input type="checkbox" 
                                       name="selected_tests" 
                                       value="{{ test.path }}"
                                       style="margin-top: 10px;">
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                    

                    
                    

                    <div class="form-group" style="margin-top: 20px;">
                        <label for="test_type">Test Type</label>
                        <select id="test_type" name="test_type" required>
                            <option value="smoke">Smoke Test</option>
                            <option value="regression">Regression Test</option>
                            <option value="api">API Test</option>
                        </select>
                    </div>


                    <!--
                    <div class="form-group" style="margin-top: 20px;">
                        <label for="expected_excel">Expected Results (Excel)</label>
                        <input type="file" id="expected_excel" name="expected_excel" accept=".xlsx,.xls">
                        <label style="display:block; margin-top:10px;">
                            <input type="checkbox" name="do_compare" value="1"> Compare API responses to expected results
                        </label>
                    </div>
                    -->

                    <button type="submit">Run Selected Tests</button>
                </form>
            </div>
            
            <!-- Real-time Terminal Output -->
            <div class="terminal-section terminal-hidden" id="terminalSection">
                <div class="terminal-header">
                    <div class="terminal-title">
                        <span class="status-indicator status-disconnected" id="statusIndicator"></span>
                        Real-time Execution Output
                    </div>
                    <div class="terminal-controls">
                        <button class="terminal-btn" onclick="clearTerminal()">Clear</button>
                        <button class="terminal-btn" onclick="toggleTerminal()">Hide</button>
                    </div>
                </div>
                <div class="terminal-display" id="terminalOutput">
                    <div class="terminal-line terminal-info">Terminal ready. Start a test execution to see output...</div>
                </div>
            </div>
        </div>
    </div>

    <script>
    let socket;
    let terminalVisible = false;
    
    function toggleTest(card) {
        const checkbox = card.querySelector('input[type="checkbox"]');
        checkbox.checked = !checkbox.checked;
        card.classList.toggle('selected', checkbox.checked);
    }
    
    function showTerminal() {
        const terminalSection = document.getElementById('terminalSection');
        terminalSection.classList.remove('terminal-hidden');
        terminalVisible = true;
    }
    
    function hideTerminal() {
        const terminalSection = document.getElementById('terminalSection');
        terminalSection.classList.add('terminal-hidden');
        terminalVisible = false;
    }
    
    function toggleTerminal() {
        if (terminalVisible) {
            hideTerminal();
        } else {
            showTerminal();
        }
    }
    
    function clearTerminal() {
        const terminalOutput = document.getElementById('terminalOutput');
        terminalOutput.innerHTML = '<div class="terminal-line terminal-info">Terminal cleared...</div>';
    }
    
    function addTerminalLine(type, text) {
        const terminalOutput = document.getElementById('terminalOutput');
        const line = document.createElement('div');
        line.className = `terminal-line terminal-${type}`;
        line.textContent = text;
        terminalOutput.appendChild(line);
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }
    
    function updateConnectionStatus(connected) {
        const indicator = document.getElementById('statusIndicator');
        if (connected) {
            indicator.className = 'status-indicator status-connected';
        } else {
            indicator.className = 'status-indicator status-disconnected';
        }
    }
    
    // Initialize WebSocket connection
    document.addEventListener('DOMContentLoaded', function() {
        // Basic styling
        document.documentElement.style.fontSize = "16px";
        document.body.style.fontSize = "16px";
        
        // Initialize Socket.IO
        socket = io();
        
        socket.on('connect', function() {
            console.log('Connected to terminal stream');
            updateConnectionStatus(true);
            addTerminalLine('info', '=== Connected to real-time terminal stream ===');
        });
        
        socket.on('disconnect', function() {
            console.log('Disconnected from terminal stream');
            updateConnectionStatus(false);
            addTerminalLine('info', '=== Disconnected from terminal stream ===');
        });
        
        socket.on('terminal_output', function(data) {
            addTerminalLine(data.type, data.data);
            if (!terminalVisible) {
                showTerminal(); // Auto-show terminal when output starts
            }
        });
        
        socket.on('terminal_clear', function() {
            clearTerminal();
        });
        
        socket.on('status', function(data) {
            addTerminalLine('info', data.msg);
        });
        
        socket.on('execution_complete', function(data) {
            console.log('Execution completed:', data);
            addTerminalLine('info', '=== Execution completed ===');
            
            if (data.failures && data.failures.length > 0) {
                addTerminalLine('stderr', `Critical failures: ${data.failures.join(', ')}`);
            }
            
            if (data.report_generated) {
                addTerminalLine('stdout', 'Allure report generated successfully');
            }
            
            addTerminalLine('info', 'Results page will load automatically...');
            
            // Enable form submission again (if it was disabled)
            const submitButton = document.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Run Selected Tests';
            }
        });
        
        // Intercept form submission to show terminal and disable form
        const testForm = document.getElementById('testForm');
        if (testForm) {
            testForm.addEventListener('submit', function(e) {
                showTerminal();
                clearTerminal();
                addTerminalLine('info', '=== Test execution starting... ===');
                
                // Disable submit button during execution
                const submitButton = this.querySelector('button[type="submit"]');
                if (submitButton) {
                    submitButton.disabled = true;
                    submitButton.textContent = 'Running Tests...';
                }
                
                socket.emit('start_execution');
            });
        }
        
        console.log('Dashboard loaded with enhanced terminal integration');
    });
    </script>
</body>
</html>
"""

def get_report_status(report_path):
    """Check the status of a report"""
    if not os.path.exists(report_path):
        return "Missing"
    
    index_file = os.path.join(report_path, 'index.html')
    if not os.path.exists(index_file):
        return "Incomplete"
    
    # Check file size to ensure it's not empty
    if os.path.getsize(index_file) < 1000:  # Minimum size for a valid report
        return "Corrupted"
    
    return "Complete"

@app.route('/reports')
def view_reports():
    """View all Allure reports from single consolidated directory"""
    reports = []
    
    # Single directory for all reports
    allure_reports_dir = 'allure-report'
    if os.path.exists(allure_reports_dir):
        for item in os.listdir(allure_reports_dir):
            report_path = os.path.join(allure_reports_dir, item)
            if os.path.isdir(report_path):
                # Extract timestamp from folder name (e.g., run_20250913_170306)
                if item.startswith('run_'):
                    timestamp_str = item[4:]  # Remove 'run_' prefix
                    run_id = item  # Use the full folder name as Run ID
                    try:
                        # Parse timestamp to create readable format
                        timestamp_obj = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                        readable_date = timestamp_obj.strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        readable_date = timestamp_str
                    
                    status = get_report_status(report_path)
                    
                    reports.append({
                        'run_id': run_id,
                        'folder': item,
                        'date': readable_date,
                        'timestamp': timestamp_str,
                        'status': status,
                        'url': f'/allure-report/{item}',
                        'download_url': f'/download-report/{item}'
                    })
    
    # Sort reports by timestamp (newest first)
    reports.sort(key=lambda x: x['timestamp'], reverse=True)
    
    reports_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Historical Allure Reports</title>
        <meta name="viewport" content="width=1200, initial-scale=1.0">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --zinnia-blue: #1a237e;
                --zinnia-gold: #ffd700;
                --zinnia-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            body {
                margin: 0;
                padding: 0;
                font-family: 'Montserrat', sans-serif;
                background: #f0f2f5;
                display: flex;
                transform: scale(2);
                transform-origin: 0 0;
                width: 50vw;
                height: 50vh;
            }

            .sidebar {
                width: 250px;
                height: 100vh;
                background: white;
                position: fixed;
                left: 0;
                top: 0;
                box-shadow: var(--zinnia-shadow);
                display: flex;
                flex-direction: column;
                z-index: 100;
            }

            .sidebar-title {
                padding: 20px;
                font-size: 1.2em;
                font-weight: 600;
                color: var(--zinnia-blue);
                border-bottom: 2px solid var(--zinnia-gold);
            }

            .sidebar-menu {
                list-style: none;
                padding: 0;
                margin: 0;
                flex-grow: 1;
            }

            .sidebar-menu li {
                padding: 0;
            }

            .sidebar-menu a {
                display: block;
                padding: 15px 20px;
                color: #333;
                text-decoration: none;
                transition: all 0.2s;
            }

            .sidebar-menu a:hover {
                background: #f0f2f5;
                color: var(--zinnia-blue);
            }

            .sidebar-menu a.active {
                background: #e8f0fe;
                color: var(--zinnia-blue);
                border-left: 4px solid var(--zinnia-blue);
            }

            .sidebar-footer {
                padding: 20px;
                text-align: center;
                font-size: 0.8em;
                color: #666;
                border-top: 1px solid #eee;
            }

            .main-content {
                margin-left: 250px;
                padding: 20px;
                width: calc(100% - 250px);
            }

            .header {
                background: white;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: var(--zinnia-shadow);
            }

            .header-inner {
                max-width: 1200px;
                margin: 0 auto;
            }

            .project-title {
                font-size: 1.5em;
                font-weight: 600;
                color: var(--zinnia-blue);
            }

            .gold-bar {
                height: 4px;
                background: var(--zinnia-gold);
                margin-top: 10px;
            }

            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }

            .card {
                background: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: var(--zinnia-shadow);
            }

            h2 {
                color: var(--zinnia-blue);
                margin-top: 0;
            }
            .reports-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: var(--zinnia-shadow);
            }
            
            .reports-table thead {
                background: var(--zinnia-blue);
                color: white;
            }
            
            .reports-table th,
            .reports-table td {
                padding: 15px;
                text-align: left;
                border-bottom: 1px solid #e0e7ef;
            }
            
            .reports-table th:first-child,
            .reports-table td:first-child {
                text-align: center;
                width: 80px;
            }
            
            .reports-table th {
                font-weight: 600;
                font-size: 0.95em;
                letter-spacing: 0.5px;
            }
            
            .reports-table tbody tr {
                transition: background-color 0.2s;
            }
            
            .reports-table tbody tr:hover {
                background-color: #f8fafc;
            }
            
            .reports-table tbody tr:last-child td {
                border-bottom: none;
            }
            
            .serial-number {
                font-weight: 600;
                color: var(--zinnia-blue);
                text-align: center;
                display: inline-block;
                min-width: 30px;
            }
            
            .run-id {
                font-family: 'Consolas', monospace;
                font-weight: 600;
                color: var(--zinnia-blue);
            }
            
            .status {
                padding: 6px 12px;
                border-radius: 15px;
                font-size: 0.85em;
                font-weight: 600;
                text-align: center;
                min-width: 80px;
                display: inline-block;
            }
            
            .status.complete {
                background: #d4edda;
                color: #155724;
            }
            
            .status.incomplete {
                background: #fff3cd;
                color: #856404;
            }
            
            .status.missing {
                background: #f8d7da;
                color: #721c24;
            }
            
            .status.corrupted {
                background: #f5c6cb;
                color: #721c24;
            }
            
            .action-buttons {
                display: flex;
                gap: 8px;
                align-items: center;
            }
            
            .button {
                display: inline-block;
                background: var(--zinnia-blue);
                color: white;
                padding: 8px 16px;
                text-decoration: none;
                border-radius: 6px;
                font-size: 0.85em;
                transition: all 0.2s;
                cursor: pointer;
                border: none;
            }
            
            .button:hover {
                transform: translateY(-1px);
                box-shadow: 0 2px 6px rgba(26,35,126,0.3);
            }
            
            .button.view {
                background: var(--zinnia-blue);
            }
            
            .button.download {
                background: #28a745;
            }
            
            .button:disabled {
                background: #6c757d;
                cursor: not-allowed;
                transform: none;
            }
            .no-reports {
                text-align: center;
                color: #666;
                font-style: italic;
                padding: 40px;
            }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <div class="sidebar-title">Menu</div>
            <ul class="sidebar-menu">
                <li><a href="/">API Testing</a></li>
                <li><a href="/performance">API Performance</a></li>
                <li><a href="/reports" class="active"> All Reports</a></li>
            </ul>
            <div class="sidebar-footer">&copy; 2025 Zinnia Dashboard</div>
        </div>
        
        <div class="main-content">
            <div class="header">
                <div class="header-inner">
                    <div class="project-title">Zinnia Live-Aura Dashboard</div>
                </div>
                <div class="gold-bar"></div>
            </div>
            <div class="container">
                <div class="card">
                    <h2> Zinnia Live-Aura: Allure Test Reports</h2>
                    <p>Browse and download the results of every automated test run.</p>
                    
                    """ + ("""
                    <table class="reports-table">
                        <thead>
                            <tr>
                                <th>S.No.</th>
                                <th>Run ID</th>
                                <th>Date/Time</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                    """ + "".join([f"""
                            <tr>
                                <td><span class="serial-number">{idx + 1}</span></td>
                                <td><span class="run-id">{report['run_id']}</span></td>
                                <td>📅 {report['date']}</td>
                                <td><span class="status {report['status'].lower()}">{report['status']}</span></td>
                                <td>
                                    <div class="action-buttons">
                                        {'<a href="' + report['url'] + '" target="_blank" class="button view">View Report</a>' if report['status'] == 'Complete' else '<span class="button view" style="background: #ccc; cursor: not-allowed;">View Report</span>'}
                                        <a href="{report['download_url']}" class="button download">Download</a>
                                    </div>
                                </td>
                            </tr>
                    """ for idx, report in enumerate(reports)]) + """
                        </tbody>
                    </table>
                    """ if reports else """
                    <div class="no-reports">
                        📝 No reports found. Run some tests from the <a href="/" style="color: var(--zinnia-blue);">dashboard</a> to generate reports.
                    </div>
                    """) + """
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return reports_html

@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE,
        regions=api_config['regions'],
        grouped_apis=group_apis_by_type(),
        api_tests=get_api_tests()
    )

@app.route('/run-tests', methods=['POST'])
def run_tests():
    selected_tests = request.form.getlist('selected_tests')
    selected_apis = request.form.getlist('selected_apis')
    region = request.form.get('region')
    test_type = request.form.get('test_type')

    try:
        # Create results directory with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_dir = f'results/run_{timestamp}'
        os.makedirs(results_dir, exist_ok=True)
        
        # Create allure-results directory for the listener
        allure_results_dir = f'{results_dir}/allure-results'
        os.makedirs(allure_results_dir, exist_ok=True)

        # Prepare environment variables for the tests
        env = os.environ.copy()
        env['TEST_ENVIRONMENT'] = region
        env['SELECTED_APIS'] = ','.join(selected_apis)
        
        output = []
        comparison_table_html = ""
        try:
            if request.form.get("do_compare") == "1":
                upfile = request.files.get("expected_excel")
                excel_bytes = None
                if upfile and upfile.filename:
                    excel_bytes = upfile.read()
                else:
                    default_path = os.path.join("tests", "expected_results.xlsx")
                    if os.path.exists(default_path):
                        with open(default_path, "rb") as _f:
                            excel_bytes = _f.read()

                if excel_bytes:
                    try:
                        df = pd.read_excel(_io_for_excel.BytesIO(excel_bytes), sheet_name="Expectations")
                        base_url = api_config["regions"][region]
                        api_by_name = {a["name"]: a for a in api_config.get("apis", [])}

                        rows = []
                        for _, r in df.iterrows():
                            api_name = str(r["api_name"]).strip()
                            field_path = str(r["field_path"]).strip()
                            comparator = str(r["comparator"]).strip()
                            expected_value = str(r["expected_value"]).strip()

                            api_def = api_by_name.get(api_name)
                            if not api_def:
                                rows.append((api_name, field_path, comparator, expected_value, "SKIPPED", "api not in config"))
                                continue

                            url = base_url.rstrip("/") + api_def["endpoint"]
                            method = api_def.get("method","GET").upper()
                            headers = api_def.get("headers", {})
                            payload = api_def.get("payload")

                            data = None
                            json_body = None
                            if headers.get("Content-Type","").startswith("application/x-www-form-urlencoded"):
                                data = payload
                            else:
                                json_body = payload

                            try:
                                resp = requests.request(method, url, headers=headers, data=data, json=json_body, timeout=30)
                                actual_json = resp.json()
                                actual_value = get_from_path(actual_json, field_path)
                                ok, detail = compare_value(actual_value, comparator, expected_value)
                                rows.append((api_name, field_path, comparator, expected_value, "PASS" if ok else "FAIL", detail))
                            except Exception as e:
                                rows.append((api_name, field_path, comparator, expected_value, "ERROR", str(e)))

                        def esc(x): 
                            s = str(x)
                            return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                        table_rows = "\n".join(
                            f"<tr><td>{esc(a)}</td><td>{esc(fp)}</td><td>{esc(c)}</td><td>{esc(ev)}</td>"
                            f"<td style='font-weight:700;color:{{'green' if s=='PASS' else ('#d32f2f' if s=='FAIL' else '#ff8f00')}}'>{esc(s)}</td><td>{esc(d)}</td></tr>"
                            for (a,fp,c,ev,s,d) in rows
                        )
                        comparison_table_html = f"""
                        <div class="card" style="margin-top:20px">
                          <h3>Expected vs Actual (Excel)</h3>
                          <div style="overflow-x:auto">
                            <table style="width:100%; border-collapse:collapse">
                              <thead>
                                <tr style="text-align:left">
                                  <th>API</th><th>Field Path</th><th>Comparator</th><th>Expected</th><th>Result</th><th>Detail</th>
                                </tr>
                              </thead>
                              <tbody>
                                {table_rows}
                              </tbody>
                            </table>
                          </div>
                        </div>
                        """
                    except Exception as e:
                        comparison_table_html = f"<div class='card' style='margin-top:20px'><h3>Expected vs Actual</h3><div style='color:#d32f2f'>Comparison failed: {e}</div></div>"
        except Exception as _compare_outer_err:
            comparison_table_html = f"<div class='card' style='margin-top:20px'><h3>Expected vs Actual</h3><div style='color:#d32f2f'>Comparison init error: {_compare_outer_err}</div></div>"

        
        # If APIs are selected, run them through the API executor
        if selected_apis:
            api_executor_path = 'tests/api/api_config_executor.robot'
            
            # Enhanced Robot Framework command with better logging and console capture
            cmd = [
                'robot',
                '--outputdir', results_dir,
                '--variable', f'ENVIRONMENT:{region}',
                '--variable', f'SELECTED_APIS:{str(selected_apis)}',
                '--variable', f'TEST_TYPE:{test_type}',
                '--listener', f'allure_robotframework;{os.path.join(results_dir, "allure-results")}',
                '--listener', f'allure_console_listener.AllureConsoleListener:{os.path.join(results_dir, "allure-results")}',  # Custom console listener
                '--listener', f'DebugLibrary',  # Add debug listener for enhanced logging
                '--loglevel', 'INFO',  # Set log level to capture more details
                '--report', os.path.join(results_dir, 'detailed_report.html'),
                '--log', os.path.join(results_dir, 'detailed_log.html'),
                '--consolecolors', 'auto',  # Enable colored console output
                '--consolewidth', '100',  # Set console width for better formatting
                api_executor_path
            ]
            
            # Execute with improved real-time output capture
            stdout_lines, stderr_lines, return_code = execute_command_with_realtime_output(cmd, env=env)
            
            output.append(f"Running API Execution Test (Enhanced Logging)")
            output.append("=== API Test Console Output ===")
            output.extend(stdout_lines)
            
            if stderr_lines:
                output.append("=== API Test Errors ===")
                output.extend(stderr_lines)
            
            # Check API execution results
            if return_code > 1:  # Robot Framework: 0=pass, 1=test failures (normal), >1=execution error
                output.append(f"❌ API execution failed with critical error (exit code: {return_code})")
                socketio.emit('terminal_output', {'type': 'stderr', 'data': f'API execution failed with exit code {return_code}'})
                # Continue to generate report for analysis, but mark as failed
            
            # Create console log file for Allure attachment
            console_log_path = os.path.join(results_dir, 'api_console_output.log')
            with open(console_log_path, 'w', encoding='utf-8') as console_file:
                console_file.write("API Test Console Output\n")
                console_file.write("=" * 50 + "\n")
                console_file.write(f"Environment: {region}\n")
                console_file.write(f"Selected APIs: {selected_apis}\n")
                console_file.write(f"Test Type: {test_type}\n")
                console_file.write(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                console_file.write("=" * 50 + "\n\n")
                console_file.write("STDOUT:\n")
                console_file.write('\n'.join(stdout_lines))
                console_file.write("\n\nSTDERR:\n")
                console_file.write('\n'.join(stderr_lines))
                console_file.write(f"\n\nProcess Exit Code: {return_code}\n")
        
        # Run selected test suites with enhanced logging
        execution_failures = []
        for test in selected_tests:
            test_name = os.path.basename(test)
            
            # Enhanced Robot Framework command for test suites
            cmd = [
                'robot',
                '--outputdir', results_dir,
                '--variable', f'ENVIRONMENT:{region}',
                '--variable', f'SELECTED_APIS:{",".join(selected_apis)}',
                '--variable', f'TEST_TYPE:{test_type}',
                '--listener', f'allure_robotframework;{os.path.join(results_dir, "allure-results")}',
                '--listener', f'allure_console_listener.AllureConsoleListener:{os.path.join(results_dir, "allure-results")}',  # Custom console listener
                '--listener', f'DebugLibrary',  # Add debug listener for enhanced logging
                '--loglevel', 'INFO',  # Set log level to capture more details
                '--report', os.path.join(results_dir, f'{test_name}_detailed_report.html'),
                '--log', os.path.join(results_dir, f'{test_name}_detailed_log.html'),
                '--consolecolors', 'auto',  # Enable colored console output
                '--consolewidth', '100',  # Set console width for better formatting
                '--metadata', f'Test_Suite:{test_name}',
                '--metadata', f'Environment:{region}',
                '--metadata', f'Test_Type:{test_type}',
                test
            ]
            
            output.append(f"Running test suite: {test_name} (Enhanced Logging)")
            output.append(f"=== {test_name} Console Output ===")
            
            # Execute with improved real-time output capture
            stdout_lines, stderr_lines, return_code = execute_command_with_realtime_output(cmd, env=env)
            
            # Add outputs to main output list
            output.extend(stdout_lines)
            
            if stderr_lines:
                output.append(f"=== {test_name} Errors ===")
                output.extend(stderr_lines)
            
            # Check test execution results
            if return_code > 1:  # Robot Framework: 0=pass, 1=test failures (normal), >1=execution error
                execution_failures.append(f"{test_name} (exit code: {return_code})")
                output.append(f"❌ Test suite {test_name} failed with critical error (exit code: {return_code})")
                socketio.emit('terminal_output', {'type': 'stderr', 'data': f'Test suite {test_name} failed with exit code {return_code}'})
            elif return_code == 1:
                output.append(f"⚠️ Test suite {test_name} completed with test failures (exit code: {return_code})")
                socketio.emit('terminal_output', {'type': 'info', 'data': f'Test suite {test_name} completed with some test failures'})
            else:
                output.append(f"✅ Test suite {test_name} completed successfully (exit code: {return_code})")
                socketio.emit('terminal_output', {'type': 'stdout', 'data': f'Test suite {test_name} completed successfully'})
            
            # Create console log file for this test suite
            suite_console_log_path = os.path.join(results_dir, f'{test_name}_console_output.log')
            with open(suite_console_log_path, 'w', encoding='utf-8') as console_file:
                console_file.write(f"{test_name} Console Output\n")
                console_file.write("=" * 50 + "\n")
                console_file.write(f"Test Suite: {test_name}\n")
                console_file.write(f"Environment: {region}\n")
                console_file.write(f"Test Type: {test_type}\n")
                console_file.write(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                console_file.write("=" * 50 + "\n\n")
                console_file.write("STDOUT:\n")
                console_file.write('\n'.join(stdout_lines))
                console_file.write("\n\nSTDERR:\n")
                console_file.write('\n'.join(stderr_lines))
                console_file.write(f"\n\nProcess Exit Code: {return_code}\n")
            
            output.append(f"Console log saved: {suite_console_log_path}")
            output.append(f"Test suite {test_name} execution completed")

        # Check if we should continue with report generation
        if execution_failures:
            output.append(f"⚠️ Critical execution failures detected: {', '.join(execution_failures)}")
            socketio.emit('terminal_output', {'type': 'stderr', 'data': f'Critical failures: {", ".join(execution_failures)}'})
            
            # For critical failures, we could provide early termination option
            if len(execution_failures) > 2:  # If more than 2 critical failures
                output.append("🛑 Multiple critical failures detected - proceeding with limited report generation")
                socketio.emit('terminal_output', {'type': 'stderr', 'data': 'Multiple critical failures - limited report generation'})
        
        # Signal that main execution is complete
        socketio.emit('terminal_output', {'type': 'info', 'data': '=== Test execution phase completed ==='})
        
        # Generate Enhanced Allure report with console integration (with timeout and error handling)
        allure_report_generated = False
        
        # Check if there are allure results to process
        if os.path.exists(allure_results_dir) and os.listdir(allure_results_dir):
            try:
                output.append("Preparing enhanced Allure report with console integration...")
                socketio.emit('terminal_output', {'type': 'info', 'data': 'Generating Allure report...'})
                
                # Create consolidated console log for Allure
                consolidated_console_path = os.path.join(allure_results_dir, 'consolidated_console.txt')
                with open(consolidated_console_path, 'w', encoding='utf-8') as consolidated_file:
                    consolidated_file.write("Complete Test Execution Console Output\n")
                    consolidated_file.write("=" * 60 + "\n")
                    consolidated_file.write(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    consolidated_file.write(f"Environment: {region}\n")
                    consolidated_file.write(f"Test Type: {test_type}\n")
                    consolidated_file.write(f"Selected APIs: {selected_apis}\n")
                    consolidated_file.write(f"Selected Tests: {[os.path.basename(t) for t in selected_tests]}\n")
                    if execution_failures:
                        consolidated_file.write(f"Critical Failures: {execution_failures}\n")
                    consolidated_file.write("=" * 60 + "\n\n")
                    
                    # Include all console logs from individual files
                    for log_file in os.listdir(results_dir):
                        if log_file.endswith('_console_output.log'):
                            log_path = os.path.join(results_dir, log_file)
                            try:
                                with open(log_path, 'r', encoding='utf-8') as f:
                                    consolidated_file.write(f"\n=== {log_file} ===\n")
                                    consolidated_file.write(f.read())
                                    consolidated_file.write(f"\n=== End of {log_file} ===\n\n")
                            except Exception as e:
                                consolidated_file.write(f"Error reading {log_file}: {e}\n")
                
                # Create execution metadata for Allure
                metadata_path = os.path.join(allure_results_dir, 'execution_metadata.json')
                metadata = {
                    "execution_info": {
                        "timestamp": datetime.now().isoformat(),
                        "environment": region,
                        "test_type": test_type,
                        "selected_apis": selected_apis,
                        "selected_tests": [os.path.basename(t) for t in selected_tests],
                        "execution_failures": execution_failures,
                        "console_integration": "enabled",
                        "enhanced_logging": "enabled"
                    }
                }
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2)
                
                # Use the local allure installation
                allure_cmd_path = os.path.join('allure-2.34.1', 'allure-2.34.1', 'bin', 'allure.bat')
                
                # Check if local allure exists, otherwise try system allure
                if os.path.exists(allure_cmd_path):
                    allure_cmd = [allure_cmd_path, 'generate', allure_results_dir, '--clean', '--single-file', '-o', f'{results_dir}/allure-report']
                else:
                    allure_cmd = ['allure', 'generate', allure_results_dir, '--clean', '--single-file', '-o', f'{results_dir}/allure-report']
                
                output.append(f"Generating Allure report with command: {' '.join(allure_cmd)}")
                
                # Add timeout to prevent hanging
                try:
                    result = subprocess.run(
                        allure_cmd, 
                        check=False,  # Don't raise exception on non-zero exit
                        shell=True, 
                        capture_output=True, 
                        text=True, 
                        timeout=120  # 2 minute timeout
                    )
                    
                    if result.stdout:
                        output.append(f"Allure generation output: {result.stdout}")
                    if result.stderr:
                        output.append(f"Allure generation warnings: {result.stderr}")
                    
                    if result.returncode != 0:
                        output.append(f"⚠️ Allure generation returned exit code: {result.returncode}")
                        socketio.emit('terminal_output', {'type': 'stderr', 'data': f'Allure generation issues (exit code: {result.returncode})'})
                    
                except subprocess.TimeoutExpired:
                    output.append("❌ Allure report generation timed out after 2 minutes")
                    socketio.emit('terminal_output', {'type': 'stderr', 'data': 'Allure report generation timed out'})
                    # Continue without report
                
                # Check if the report was actually generated
                if os.path.exists(f'{results_dir}/allure-report/index.html'):
                    output.append("✅ Enhanced Allure report generated successfully with console integration")
                    socketio.emit('terminal_output', {'type': 'stdout', 'data': 'Allure report generated successfully'})
                    
                    # Copy report to consolidated allure-report directory
                    try:
                        serving_dir = f'allure-report/{os.path.basename(results_dir)}'
                        os.makedirs('allure-report', exist_ok=True)
                        
                        # Always copy to consolidated directory (overwrite if exists for fresh reports)
                        if os.path.exists(serving_dir):
                            shutil.rmtree(serving_dir)
                        
                        # Copy the generated report to the consolidated directory
                        shutil.copytree(f'{results_dir}/allure-report', serving_dir)
                        output.append(f"Enhanced Allure report saved to consolidated location: {serving_dir}")
                        output.append(f"Console logs integrated and available in report attachments")
                        
                        allure_report_generated = True
                        
                    except Exception as copy_error:
                        output.append(f"⚠️ Warning: Report generated but failed to copy to serving location: {str(copy_error)}")
                        allure_report_generated = True  # Report still exists in original location
                else:
                    output.append("⚠️ Allure report generation completed but index.html not found")
                    socketio.emit('terminal_output', {'type': 'stderr', 'data': 'Allure report index.html not found'})
                    
            except Exception as e:
                output.append(f"❌ Error generating Allure report: {str(e)}")
                socketio.emit('terminal_output', {'type': 'stderr', 'data': f'Allure report error: {str(e)}'})
        else:
            output.append("⚠️ No Allure results found - skipping Allure report generation")
            socketio.emit('terminal_output', {'type': 'info', 'data': 'No Allure results found'})

        # Signal completion to WebSocket clients
        socketio.emit('terminal_output', {'type': 'info', 'data': '=== Execution completed - generating results page ==='})
        socketio.emit('execution_complete', {
            'status': 'completed',
            'failures': execution_failures,
            'report_generated': allure_report_generated,
            'results_dir': results_dir
        })

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Execution Results</title>
            <meta name="viewport" content="width=1200, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
            <style>
                :root {{
                    --zinnia-blue: #1a237e;
                    --zinnia-gold: #ffd700;
                    --zinnia-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                body {{
                    font-family: 'Montserrat', sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: #f0f2f5;
                    transform: scale(2);
                    transform-origin: 0 0;
                    width: 50vw;
                    height: 50vh;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: var(--zinnia-shadow);
                }}
                h2 {{
                    color: var(--zinnia-blue);
                    margin-top: 0;
                }}
                .info-section {{
                    background: #f8fafc;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }}
                .info-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                }}
                .info-item {{
                    background: white;
                    padding: 15px;
                    border-radius: 6px;
                    box-shadow: var(--zinnia-shadow);
                }}
                .info-label {{
                    font-weight: 600;
                    color: var(--zinnia-blue);
                    margin-bottom: 5px;
                }}
                .output-section {{
                    background: #1e1e1e;
                    color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    margin-top: 20px;
                    overflow-x: auto;
                }}
                pre {{
                    margin: 0;
                    white-space: pre-wrap;
                    font-family: 'Consolas', monospace;
                }}
                .button {{
                    display: inline-block;
                    background: var(--zinnia-blue);
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 6px;
                    margin-top: 20px;
                    transition: all 0.2s;
                }}
                .button:hover {{
                    transform: translateY(-2px);
                    box-shadow: var(--zinnia-shadow);
                }}
                .allure-button {{
                    background: #4CAF50;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Test Execution Results</h2>
                <div class="info-section">
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">Environment</div>
                            <div>{region}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Test Type</div>
                            <div>{test_type}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Selected APIs</div>
                            <div>{', '.join(selected_apis)}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Selected Tests</div>
                            <div>{', '.join(os.path.basename(t) for t in selected_tests)}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Results Directory</div>
                            <div>{results_dir}</div>
                        </div>
                    </div>
                </div>
                
                {comparison_table_html}
                
                <div class="output-section">
                    <pre>{'\n'.join(output)}</pre>
                </div>
                
                <div style="margin-top: 20px;">
                    {'<a href="/allure-report/' + os.path.basename(results_dir) + '" target="_blank" class="button allure-button">View Allure Report</a>' if allure_report_generated else '<span class="button" style="background: #ccc; cursor: not-allowed;">Allure Report Not Available</span>'}
                    <a href="/" class="button">Back to Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        """

    except Exception as e:
        # Ensure WebSocket clients are notified of the error
        try:
            socketio.emit('terminal_output', {'type': 'stderr', 'data': f'Critical error: {str(e)}'})
            socketio.emit('execution_complete', {
                'status': 'error', 
                'error': str(e),
                'failures': [],
                'report_generated': False
            })
        except:
            pass  # Ignore WebSocket errors in error handler
            
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error - Test Execution</title>
            <meta name="viewport" content="width=1200, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
            <style>
                :root {{
                    --zinnia-blue: #1a237e;
                    --zinnia-gold: #ffd700;
                    --zinnia-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                body {{
                    font-family: 'Montserrat', sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: #f0f2f5;
                    transform: scale(2);
                    transform-origin: 0 0;
                    width: 50vw;
                    height: 50vh;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: var(--zinnia-shadow);
                }}
                h2 {{
                    color: #d32f2f;
                    margin-top: 0;
                }}
                .error-message {{
                    background: #ffebee;
                    color: #d32f2f;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    word-wrap: break-word;
                }}
                .error-details {{
                    font-family: 'Consolas', monospace;
                    font-size: 0.9em;
                    background: #f5f5f5;
                    padding: 15px;
                    border-radius: 4px;
                    margin-top: 10px;
                    overflow-x: auto;
                }}
                .button {{
                    display: inline-block;
                    background: var(--zinnia-blue);
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 6px;
                    transition: all 0.2s;
                    margin-right: 10px;
                }}
                .button:hover {{
                    transform: translateY(-2px);
                    box-shadow: var(--zinnia-shadow);
                }}
                .retry-button {{
                    background: #ff9800;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>❌ Test Execution Error</h2>
                <div class="error-message">
                    <strong>An error occurred during test execution:</strong>
                    <div class="error-details">{str(e)}</div>
                </div>
                <div style="margin-top: 20px;">
                    <p><strong>Possible solutions:</strong></p>
                    <ul>
                        <li>Check if Robot Framework is properly installed</li>
                        <li>Verify test files exist and are accessible</li>
                        <li>Check Allure installation if report generation failed</li>
                        <li>Review console output for detailed error information</li>
                    </ul>
                </div>
                <div style="margin-top: 30px;">
                    <a href="/" class="button">Back to Dashboard</a>
                    <a href="/reports" class="button">View Previous Reports</a>
                    <button onclick="window.location.reload()" class="button retry-button">Retry</button>
                </div>
            </div>
        </body>
        </html>
        """

# @app.route('/allure-report/<path:run_id>/<path:filename>')
# def serve_allure_report(run_id, filename):
#     """Serve Allure report files"""
#     try:
#         # Construct the path to the allure report
#         report_dir = os.path.join('results', run_id, 'allure-report')
        
#         # Security check: ensure the path is within our results directory
#         abs_report_dir = os.path.abspath(report_dir)
#         abs_results_dir = os.path.abspath('results')
        
#         if not abs_report_dir.startswith(abs_results_dir):
#             abort(403)  # Forbidden
        
#         # Check if the report directory exists
#         if not os.path.exists(report_dir):
#             abort(404)  # Not found
        
#         # Handle directory requests by serving index.html
#         full_path = os.path.join(report_dir, filename)
#         if os.path.isdir(full_path):
#             filename = os.path.join(filename, 'index.html')
        
#         # Serve the file
#         return send_from_directory(report_dir, filename)
    
#     except Exception as e:
#         print(f"Error serving allure report: {e}")
#         abort(404)

# @app.route('/allure-report/<path:run_id>')
# def serve_allure_report_index(run_id):
#     """Serve Allure report index page"""
#     return serve_allure_report(run_id, 'index.html')


@app.route('/allure-report/<path:run_id>/<path:filename>')
def serve_allure_report(run_id, filename):
    """Serve Allure report files from the top-level allure-report directory"""
    try:
        # Construct the path to the allure report in the top-level allure-report directory
        report_dir = os.path.join('allure-report', run_id)
        
        # Security check: ensure the path is within our allure-report directory
        abs_report_dir = os.path.abspath(report_dir)
        abs_allure_dir = os.path.abspath('allure-report')
        
        if not abs_report_dir.startswith(abs_allure_dir):
            abort(403)  # Forbidden
        
        # Check if the report directory exists
        if not os.path.exists(report_dir):
            abort(404)  # Not found
        
        # Handle directory requests by serving index.html
        full_path = os.path.join(report_dir, filename)
        if os.path.isdir(full_path):
            filename = os.path.join(filename, 'index.html')
        
        # Serve the file
        return send_from_directory(report_dir, filename)
    
    except Exception as e:
        print(f"Error serving allure report: {e}")
        abort(404)

@app.route('/allure-report/<path:run_id>')
def serve_allure_report_index(run_id):
    """Serve Allure report index page from the top-level allure-report directory"""
    return serve_allure_report(run_id, 'index.html')

@app.route('/download-report/<path:run_id>')
def download_report(run_id):
    """Download a report as a zip file"""
    import zipfile
    import io
    
    try:
        # Construct the path to the report directory
        report_dir = os.path.join('allure-report', run_id)
        
        # Security check: ensure the path is within our allure-report directory
        abs_report_dir = os.path.abspath(report_dir)
        abs_allure_dir = os.path.abspath('allure-report')
        
        if not abs_report_dir.startswith(abs_allure_dir):
            abort(403)  # Forbidden
        
        # Check if the report directory exists
        if not os.path.exists(report_dir):
            abort(404)  # Not found
        
        # Create a zip file in memory
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(report_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calculate the relative path within the zip file
                    arcname = os.path.relpath(file_path, report_dir)
                    zf.write(file_path, arcname)
        
        memory_file.seek(0)
        
        # Prepare the response
        from flask import make_response
        response = make_response(memory_file.getvalue())
        response.headers.set('Content-Disposition', f'attachment; filename={run_id}_report.zip')
        response.headers.set('Content-Type', 'application/zip')
        
        return response
    
    except Exception as e:
        print(f"Error downloading report: {e}")
        abort(404)




if __name__ == '__main__':
    print("Starting enhanced dashboard server with real-time terminal integration on http://localhost:5050")
    print("Features: WebSocket support, real-time execution output, cross-platform subprocess handling")
    print("Press Ctrl+C to stop the server")
    socketio.run(app, host='0.0.0.0', port=5050, debug=False)
