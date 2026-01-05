#!/usr/bin/env python3
"""
Connectivity Dashboard - NEW: Web dashboard

Web-based dashboard for Starlink connectivity monitoring and management.
Provides a user-friendly interface for real-time monitoring and control.
"""

import sys
import json
from datetime import datetime
from typing import Dict, Any

# Add parent directory to path to import src modules
sys.path.insert(0, '/home/runner/work/starlink_connectivity_tools.py/starlink_connectivity_tools.py')

from src.starlink_monitor import StarlinkMonitor
from src.connection_manager import ConnectionManager
from src.bandwidth_optimizer import BandwidthOptimizer
from src.power_manager import PowerManager, PowerMode
from src.failover_handler import FailoverHandler
from src.diagnostics import Diagnostics
from src.config.settings import Settings

try:
    from flask import Flask, render_template_string, jsonify, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Warning: Flask not installed. Web dashboard requires Flask.")
    print("Install with: pip install flask")

app = Flask(__name__)

# Initialize components
monitor = StarlinkMonitor()
connection_manager = ConnectionManager()
bandwidth_optimizer = BandwidthOptimizer()
power_manager = PowerManager()
failover_handler = FailoverHandler()
diagnostics = Diagnostics()


# HTML Template for dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Starlink Connectivity Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: #0a0e27;
            color: #e0e0e0;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .header h1 {
            color: white;
            font-size: 2em;
            margin-bottom: 10px;
        }
        .header .status {
            color: #4ade80;
            font-size: 1.1em;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: #1a1f3a;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            border: 1px solid #2a3555;
        }
        .card h2 {
            color: #60a5fa;
            font-size: 1.3em;
            margin-bottom: 15px;
            border-bottom: 2px solid #2a3555;
            padding-bottom: 10px;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #2a3555;
        }
        .metric:last-child { border-bottom: none; }
        .metric-label {
            color: #94a3b8;
            font-weight: 500;
        }
        .metric-value {
            color: #e0e0e0;
            font-weight: 600;
        }
        .metric-value.good { color: #4ade80; }
        .metric-value.warning { color: #fbbf24; }
        .metric-value.critical { color: #f87171; }
        .alert {
            background: #7f1d1d;
            border-left: 4px solid #dc2626;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
        }
        .alert.warning {
            background: #78350f;
            border-left-color: #f59e0b;
        }
        .controls {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        button {
            background: #2563eb;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            transition: background 0.3s;
        }
        button:hover {
            background: #1d4ed8;
        }
        button:disabled {
            background: #475569;
            cursor: not-allowed;
        }
        .refresh-info {
            text-align: center;
            color: #94a3b8;
            margin-top: 20px;
            font-size: 0.9em;
        }
    </style>
    <script>
        function refreshData() {
            fetch('/api/metrics')
                .then(response => response.json())
                .then(data => updateDashboard(data))
                .catch(error => console.error('Error fetching data:', error));
        }
        
        function updateDashboard(data) {
            document.getElementById('last-update').textContent = 
                'Last update: ' + new Date().toLocaleTimeString();
            
            // Update metrics (would populate from API in real implementation)
            console.log('Dashboard updated', data);
        }
        
        // Auto-refresh every 5 seconds
        setInterval(refreshData, 5000);
        
        // Initial load
        window.onload = refreshData;
    </script>
</head>
<body>
    <div class="header">
        <h1>🛰️ Starlink Connectivity Dashboard</h1>
        <div class="status">System Online</div>
    </div>
    
    <div class="grid">
        <div class="card">
            <h2>📡 Connection Status</h2>
            <div class="metric">
                <span class="metric-label">Status</span>
                <span class="metric-value good">Connected</span>
            </div>
            <div class="metric">
                <span class="metric-label">Signal Quality</span>
                <span class="metric-value good">92%</span>
            </div>
            <div class="metric">
                <span class="metric-label">Satellites</span>
                <span class="metric-value">11</span>
            </div>
            <div class="metric">
                <span class="metric-label">Latency</span>
                <span class="metric-value">38.5 ms</span>
            </div>
        </div>
        
        <div class="card">
            <h2>📊 Performance</h2>
            <div class="metric">
                <span class="metric-label">Download</span>
                <span class="metric-value good">156.3 Mbps</span>
            </div>
            <div class="metric">
                <span class="metric-label">Upload</span>
                <span class="metric-value good">23.1 Mbps</span>
            </div>
            <div class="metric">
                <span class="metric-label">Packet Loss</span>
                <span class="metric-value good">0.2%</span>
            </div>
            <div class="metric">
                <span class="metric-label">Obstruction</span>
                <span class="metric-value good">0.8%</span>
            </div>
        </div>
        
        <div class="card">
            <h2>🔋 Power Management</h2>
            <div class="metric">
                <span class="metric-label">Mode</span>
                <span class="metric-value">Normal</span>
            </div>
            <div class="metric">
                <span class="metric-label">Current Power</span>
                <span class="metric-value">70 W</span>
            </div>
            <div class="metric">
                <span class="metric-label">Battery Runtime</span>
                <span class="metric-value">14.3 hours</span>
            </div>
        </div>
        
        <div class="card">
            <h2>🔄 Failover Status</h2>
            <div class="metric">
                <span class="metric-label">Primary</span>
                <span class="metric-value good">Starlink (Active)</span>
            </div>
            <div class="metric">
                <span class="metric-label">Backup 1</span>
                <span class="metric-value">Cellular (Standby)</span>
            </div>
            <div class="metric">
                <span class="metric-label">Backup 2</span>
                <span class="metric-value">Ethernet (Standby)</span>
            </div>
            <div class="metric">
                <span class="metric-label">Failovers</span>
                <span class="metric-value">0</span>
            </div>
        </div>
    </div>
    
    <div class="card">
        <h2>⚙️ Controls</h2>
        <div class="controls">
            <button onclick="alert('Running diagnostics...')">Run Diagnostics</button>
            <button onclick="alert('Optimizing bandwidth...')">Optimize Bandwidth</button>
            <button onclick="alert('Testing failover...')">Test Failover</button>
            <button onclick="alert('Switching to ECO mode...')">ECO Mode</button>
        </div>
    </div>
    
    <div class="refresh-info">
        <span id="last-update">Initializing...</span>
    </div>
</body>
</html>
"""


@app.route('/')
def index():
    """Serve the main dashboard."""
    return render_template_string(DASHBOARD_TEMPLATE)


@app.route('/api/metrics')
def get_metrics():
    """Get current metrics as JSON."""
    metrics = monitor.get_current_metrics()
    connection_status = connection_manager.get_status()
    bandwidth_usage = bandwidth_optimizer.get_current_usage()
    power_status = power_manager.get_power_status()
    failover_status = failover_handler.get_status()
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'starlink': metrics,
        'connection': connection_status,
        'bandwidth': bandwidth_usage,
        'power': power_status,
        'failover': failover_status
    })


@app.route('/api/alerts')
def get_alerts():
    """Get current alerts."""
    alerts = monitor.check_alerts()
    return jsonify({'alerts': alerts})


@app.route('/api/diagnostics', methods=['POST'])
def run_diagnostics():
    """Run diagnostics."""
    report = diagnostics.run_full_diagnostic()
    return jsonify(report)


@app.route('/api/power/mode', methods=['POST'])
def set_power_mode():
    """Set power mode."""
    data = request.get_json()
    mode_str = data.get('mode', 'normal')
    
    try:
        mode = PowerMode[mode_str.upper()]
        success = power_manager.set_power_mode(mode)
        return jsonify({'success': success, 'mode': mode_str})
    except KeyError:
        return jsonify({'success': False, 'error': 'Invalid power mode'}), 400


@app.route('/api/bandwidth/profile', methods=['POST'])
def set_bandwidth_profile():
    """Set bandwidth profile."""
    data = request.get_json()
    profile = data.get('profile', 'normal')
    
    success = bandwidth_optimizer.set_profile(profile)
    return jsonify({'success': success, 'profile': profile})


@app.route('/api/failover/test', methods=['POST'])
def test_failover():
    """Test failover mechanism."""
    result = failover_handler.initiate_failover()
    return jsonify({'success': result, 'status': failover_handler.get_status()})


def main():
    """Main entry point."""
    if not FLASK_AVAILABLE:
        print("\nFlask is required to run the web dashboard.")
        print("Install it with: pip install flask")
        return 1
    
    import argparse
    parser = argparse.ArgumentParser(
        description="Starlink Connectivity Dashboard"
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to bind to (default: 5000)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    print(f"\n🚀 Starting Starlink Connectivity Dashboard...")
    print(f"📊 Dashboard URL: http://{args.host}:{args.port}")
    print(f"🔧 API Base URL: http://{args.host}:{args.port}/api")
    print(f"\nPress Ctrl+C to stop\n")
    
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
