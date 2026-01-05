"""
Connectivity Diagnostics
Performs diagnostics and health checks on connectivity
"""

import logging
from typing import Dict, List
from datetime import datetime
Diagnostic tools for connectivity troubleshooting
"""
import json
import time
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import subprocess
import platform

logger = logging.getLogger(__name__)


class ConnectivityDiagnostics:
    """
    Performs comprehensive connectivity diagnostics
    """
    
    def __init__(self):
        """Initialize diagnostics system"""
        self.diagnostic_history: List[Dict] = []
        logger.info("ConnectivityDiagnostics initialized")
    
    def run_full_diagnostic(self) -> Dict:
        """
        Run full connectivity diagnostic
        
        Returns:
            Dictionary with diagnostic results
        """
        logger.info("Running full connectivity diagnostic...")
    """Comprehensive diagnostic tools for connectivity issues"""
    
    def __init__(self, log_directory: str = "./logs"):
        self.log_directory = log_directory
        self.diagnostic_history: List[Dict] = []
        self.max_history = 100  # Keep last 100 diagnostics
        
        # Create log directory if it doesn't exist
        import os
        os.makedirs(log_directory, exist_ok=True)
    
    def run_full_diagnostic(self) -> Dict:
        """Run comprehensive diagnostic tests"""
        logger.info("Running full connectivity diagnostic")
        
        diagnostic = {
            'timestamp': datetime.now().isoformat(),
            'tests': {},
            'overall_status': 'healthy'
        }
        
        # Simulate various diagnostic tests
        diagnostic['tests']['signal_test'] = self._test_signal()
        diagnostic['tests']['latency_test'] = self._test_latency()
        diagnostic['tests']['bandwidth_test'] = self._test_bandwidth()
        diagnostic['tests']['stability_test'] = self._test_stability()
        
        # Determine overall status
        failed_tests = [name for name, result in diagnostic['tests'].items() 
                       if result['status'] != 'passed']
        
        if failed_tests:
            diagnostic['overall_status'] = 'degraded'
            logger.warning(f"Diagnostic completed with issues: {failed_tests}")
        else:
            logger.info("Diagnostic completed - all tests passed")
        
        # Store in history
        self.diagnostic_history.append(diagnostic)
        
        return diagnostic
    
    def _test_signal(self) -> Dict:
        """Test signal strength"""
        # Simulate signal test
        signal_strength = -65.0  # dBm
        
        status = 'passed' if signal_strength > -75.0 else 'warning'
        
        return {
            'status': status,
            'signal_strength_dbm': signal_strength,
            'message': f"Signal strength: {signal_strength} dBm"
        }
    
    def _test_latency(self) -> Dict:
        """Test latency"""
        # Simulate latency test
        latency = 45.0  # ms
        
        status = 'passed' if latency < 100.0 else 'warning'
        
        return {
            'status': status,
            'latency_ms': latency,
            'message': f"Latency: {latency} ms"
        }
    
    def _test_bandwidth(self) -> Dict:
        """Test bandwidth"""
        # Simulate bandwidth test
        bandwidth_down = 85.0  # Mbps
        bandwidth_up = 15.0    # Mbps
        
        status = 'passed' if bandwidth_down > 10.0 else 'warning'
        
        return {
            'status': status,
            'bandwidth_down_mbps': bandwidth_down,
            'bandwidth_up_mbps': bandwidth_up,
            'message': f"Bandwidth: {bandwidth_down}/{bandwidth_up} Mbps"
        }
    
    def _test_stability(self) -> Dict:
        """Test connection stability"""
        # Simulate stability test
        packet_loss = 0.5  # percentage
        
        status = 'passed' if packet_loss < 2.0 else 'warning'
        
        return {
            'status': status,
            'packet_loss_percent': packet_loss,
            'message': f"Packet loss: {packet_loss}%"
        }
    
    def get_diagnostic_history(self, limit: int = 10) -> List[Dict]:
        """
        Get recent diagnostic history
        
        Args:
            limit: Maximum number of results to return
            
        Returns:
            List of recent diagnostics
        """
        return self.diagnostic_history[-limit:]
            'summary': {
                'status': 'unknown',
                'issues_found': 0,
                'recommendations': []
            }
        }
        
        # Run individual tests
        diagnostic['tests']['system'] = self._check_system_status()
        diagnostic['tests']['network_interfaces'] = self._check_network_interfaces()
        diagnostic['tests']['dns'] = self._check_dns_resolution()
        diagnostic['tests']['gateway'] = self._check_gateway_connectivity()
        diagnostic['tests']['internet'] = self._check_internet_connectivity()
        diagnostic['tests']['satellite_status'] = self._check_satellite_status()
        
        # Analyze results
        self._analyze_diagnostic(diagnostic)
        
        # Log and store
        self._log_diagnostic(diagnostic)
        self.diagnostic_history.append(diagnostic)
        
        # Keep history within limit
        if len(self.diagnostic_history) > self.max_history:
            self.diagnostic_history = self.diagnostic_history[-self.max_history:]
        
        return diagnostic
    
    def _check_system_status(self) -> Dict:
        """Check system health status"""
        status = {
            'operating_system': platform.system(),
            'release': platform.release(),
            'cpu_usage': self._get_cpu_usage(),
            'memory_usage': self._get_memory_usage(),
            'disk_usage': self._get_disk_usage(),
            'uptime': self._get_system_uptime()
        }
        
        # Check for issues
        issues = []
        if status['cpu_usage'] > 90:
            issues.append('High CPU usage')
        if status['memory_usage'] > 90:
            issues.append('High memory usage')
        if status['disk_usage'] > 90:
            issues.append('Low disk space')
        
        status['issues'] = issues
        status['healthy'] = len(issues) == 0
        
        return status
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        try:
            import psutil
            return psutil.cpu_percent(interval=1)
        except:
            return 0.0
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage percentage"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return memory.percent
        except:
            return 0.0
    
    def _get_disk_usage(self) -> float:
        """Get disk usage percentage"""
        try:
            import psutil
            disk = psutil.disk_usage('/')
            return disk.percent
        except:
            return 0.0
    
    def _get_system_uptime(self) -> float:
        """Get system uptime in seconds"""
        try:
            import psutil
            return time.time() - psutil.boot_time()
        except:
            return 0.0
    
    def _check_network_interfaces(self) -> Dict:
        """Check network interfaces status"""
        interfaces = {
            'interfaces': [],
            'issues': [],
            'healthy': False
        }
        
        try:
            import netifaces
            iface_list = netifaces.interfaces()
            
            for iface in iface_list:
                iface_info = {
                    'name': iface,
                    'status': 'unknown',
                    'addresses': []
                }
                
                # Get addresses
                try:
                    addrs = netifaces.ifaddresses(iface)
                    if netifaces.AF_INET in addrs:
                        for addr in addrs[netifaces.AF_INET]:
                            iface_info['addresses'].append({
                                'ip': addr.get('addr'),
                                'netmask': addr.get('netmask')
                            })
                            iface_info['status'] = 'up'
                except:
                    iface_info['status'] = 'error'
                
                interfaces['interfaces'].append(iface_info)
            
            # Check if any interface has IP address
            has_ip = any(
                len(iface['addresses']) > 0 
                for iface in interfaces['interfaces']
            )
            
            interfaces['healthy'] = has_ip
            if not has_ip:
                interfaces['issues'].append('No network interface has IP address')
        
        except Exception as e:
            interfaces['error'] = str(e)
            interfaces['issues'].append(f'Failed to check interfaces: {e}')
        
        return interfaces
    
    def _check_dns_resolution(self) -> Dict:
        """Check DNS resolution capability"""
        test_domains = [
            'google.com',
            'cloudflare.com',
            'example.com'
        ]
        
        results = {
            'domains': {},
            'healthy': False,
            'issues': []
        }
        
        import socket
        
        for domain in test_domains:
            try:
                start = time.time()
                socket.gethostbyname(domain)
                resolve_time = (time.time() - start) * 1000  # Convert to ms
                
                results['domains'][domain] = {
                    'resolved': True,
                    'resolve_time_ms': resolve_time
                }
            except socket.gaierror:
                results['domains'][domain] = {
                    'resolved': False,
                    'resolve_time_ms': None
                }
                results['issues'].append(f'Failed to resolve: {domain}')
        
        # Consider healthy if at least one domain resolves
        successful = sum(1 for d in results['domains'].values() if d['resolved'])
        results['healthy'] = successful > 0
        
        if not results['healthy']:
            results['issues'].append('DNS resolution completely failed')
        
        return results
    
    def _check_gateway_connectivity(self) -> Dict:
        """Check connectivity to default gateway"""
        result = {
            'reachable': False,
            'latency_ms': None,
            'healthy': False,
            'issues': []
        }
        
        try:
            # Get default gateway
            import netifaces
            
            gateways = netifaces.gateways()
            if 'default' in gateways and netifaces.AF_INET in gateways['default']:
                gateway_ip = gateways['default'][netifaces.AF_INET][0]
                
                # Ping gateway
                latency = self._ping_host(gateway_ip)
                
                if latency is not None:
                    result['reachable'] = True
                    result['latency_ms'] = latency
                    result['healthy'] = latency < 100  # Threshold
                else:
                    result['issues'].append('Gateway not reachable')
            else:
                result['issues'].append('No default gateway found')
        
        except Exception as e:
            result['issues'].append(f'Gateway check failed: {e}')
        
        return result
    
    def _check_internet_connectivity(self) -> Dict:
        """Check general internet connectivity"""
        test_hosts = [
            '8.8.8.8',  # Google DNS
            '1.1.1.1',  # Cloudflare DNS
            'www.google.com'
        ]
        
        results = {
            'hosts': {},
            'healthy': False,
            'issues': []
        }
        
        for host in test_hosts:
            try:
                latency = self._ping_host(host)
                
                results['hosts'][host] = {
                    'reachable': latency is not None,
                    'latency_ms': latency
                }
                
                if latency is None:
                    results['issues'].append(f'Host unreachable: {host}')
            except Exception as e:
                results['hosts'][host] = {
                    'reachable': False,
                    'latency_ms': None,
                    'error': str(e)
                }
                results['issues'].append(f'Error pinging {host}: {e}')
        
        # Consider healthy if at least one host is reachable
        reachable = sum(1 for h in results['hosts'].values() if h['reachable'])
        results['healthy'] = reachable > 0
        
        if not results['healthy']:
            results['issues'].append('No internet connectivity')
        
        return results
    
    def _ping_host(self, host: str, count: int = 3) -> Optional[float]:
        """Ping a host and return average latency"""
        try:
            import ping3
            
            latencies = []
            for _ in range(count):
                latency = ping3.ping(host, timeout=2)
                if latency is not None:
                    latencies.append(latency * 1000)  # Convert to ms
                time.sleep(0.5)
            
            return sum(latencies) / len(latencies) if latencies else None
        
        except:
            # Fallback to system ping
            try:
                param = '-n' if platform.system().lower() == 'windows' else '-c'
                command = ['ping', param, str(count), host]
                output = subprocess.run(
                    command, 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                
                # Parse output for latency
                import re
                match = re.search(r'time=([\d.]+)\s*ms', output.stdout)
                if match:
                    return float(match.group(1))
            except:
                pass
        
        return None
    
    def _check_satellite_status(self) -> Dict:
        """Check satellite-specific status"""
        # This would interface with Starlink API in real implementation
        status = {
            'connected': False,
            'signal_quality': 'unknown',
            'obstruction_percent': 0.0,
            'satellites_visible': 0,
            'healthy': False,
            'issues': []
        }
        
        # Simulated check
        try:
            # Simulate satellite status
            import random
            status['connected'] = random.random() > 0.3
            status['signal_quality'] = random.choice(['excellent', 'good', 'fair', 'poor'])
            status['obstruction_percent'] = random.uniform(0, 10)
            status['satellites_visible'] = random.randint(3, 12)
            
            # Determine health
            status['healthy'] = (
                status['connected'] and
                status['signal_quality'] in ['excellent', 'good'] and
                status['obstruction_percent'] < 5
            )
            
            if not status['healthy']:
                if not status['connected']:
                    status['issues'].append('Not connected to satellite')
                if status['signal_quality'] in ['fair', 'poor']:
                    status['issues'].append(f'Poor signal quality: {status["signal_quality"]}')
                if status['obstruction_percent'] >= 5:
                    status['issues'].append(f'High obstruction: {status["obstruction_percent"]:.1f}%')
        
        except Exception as e:
            status['error'] = str(e)
            status['issues'].append(f'Satellite check failed: {e}')
        
        return status
    
    def _analyze_diagnostic(self, diagnostic: Dict):
        """Analyze diagnostic results and generate summary"""
        issues = []
        recommendations = []
        
        # Check system issues
        system_issues = diagnostic['tests']['system'].get('issues', [])
        issues.extend([f"System: {issue}" for issue in system_issues])
        
        # Check network issues
        network_issues = diagnostic['tests']['network_interfaces'].get('issues', [])
        issues.extend([f"Network: {issue}" for issue in network_issues])
        
        # Check DNS issues
        dns_issues = diagnostic['tests']['dns'].get('issues', [])
        issues.extend([f"DNS: {issue}" for issue in dns_issues])
        
        # Check gateway issues
        gateway_issues = diagnostic['tests']['gateway'].get('issues', [])
        issues.extend([f"Gateway: {issue}" for issue in gateway_issues])
        
        # Check internet issues
        internet_issues = diagnostic['tests']['internet'].get('issues', [])
        issues.extend([f"Internet: {issue}" for issue in internet_issues])
        
        # Check satellite issues
        satellite_issues = diagnostic['tests']['satellite_status'].get('issues', [])
        issues.extend([f"Satellite: {issue}" for issue in satellite_issues])
        
        # Generate recommendations
        if issues:
            if any('DNS' in issue for issue in issues):
                recommendations.append("Try using alternative DNS servers (1.1.1.1, 8.8.8.8)")
            
            if any('Gateway' in issue for issue in issues):
                recommendations.append("Check router/gateway connectivity and power")
            
            if any('Satellite' in issue for issue in issues):
                recommendations.append("Reposition satellite dish for better line of sight")
                recommendations.append("Check for obstructions (trees, buildings)")
            
            if any('No internet connectivity' in issue for issue in issues):
                recommendations.append("Reset network equipment")
                recommendations.append("Contact service provider")
        
        # Update summary
        diagnostic['summary']['status'] = 'healthy' if len(issues) == 0 else 'unhealthy'
        diagnostic['summary']['issues_found'] = len(issues)
        diagnostic['summary']['issues'] = issues
        diagnostic['summary']['recommendations'] = recommendations
    
    def _log_diagnostic(self, diagnostic: Dict):
        """Log diagnostic results to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.log_directory}/diagnostic_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(diagnostic, f, indent=2, default=str)
            logger.info(f"Diagnostic logged to {filename}")
        except Exception as e:
            logger.error(f"Failed to log diagnostic: {e}")
    
    def get_historical_diagnostics(self, 
                                  hours: int = 24) -> List[Dict]:
        """Get diagnostics from the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        recent = []
        for diag in self.diagnostic_history:
            diag_time = datetime.fromisoformat(diag['timestamp'])
            if diag_time >= cutoff:
                recent.append(diag)
        
        return recent
    
    def generate_health_report(self) -> Dict:
        """Generate a comprehensive health report"""
        # Run fresh diagnostic
        current = self.run_full_diagnostic()
        
        # Get recent history
        recent = self.get_historical_diagnostics(hours=24)
        
        # Calculate statistics
        total_diagnostics = len(recent)
        healthy_count = sum(1 for d in recent 
                          if d['summary']['status'] == 'healthy')
        health_percentage = (healthy_count / total_diagnostics * 100) if total_diagnostics > 0 else 0
        
        # Common issues
        all_issues = []
        for diag in recent:
            all_issues.extend(diag['summary'].get('issues', []))
        
        from collections import Counter
        common_issues = Counter(all_issues).most_common(5)
        
        report = {
            'current_status': current['summary']['status'],
            'health_over_last_24h': {
                'total_checks': total_diagnostics,
                'healthy_checks': healthy_count,
                'health_percentage': health_percentage
            },
            'common_issues': common_issues,
            'current_diagnostic': current,
            'timestamp': datetime.now().isoformat()
        }
        
        return report
Diagnostics Module

Provides diagnostic tools and health checks for Starlink connections.
"""


class Diagnostics:
    """Provides diagnostic capabilities for Starlink connections."""

    def __init__(self):
        """Initialize the Diagnostics module."""
        self.test_results = []
        self.health_status = "unknown"

    def run_health_check(self):
        """
        Run a comprehensive health check.

        Returns:
            dict: Health check results
        """
        results = {
            "status": "healthy",
            "tests_passed": 0,
            "tests_failed": 0,
            "details": [],
        }

        # Placeholder implementation
        self.health_status = results["status"]
        return results

    def test_connectivity(self):
        """
        Test connection to Starlink satellite.

        Returns:
            dict: Connectivity test results
        """
        result = {
            "test": "connectivity",
            "status": "passed",
            "latency": 0,
            "packet_loss": 0,
        }
        self.test_results.append(result)
        return result

    def test_bandwidth(self):
        """
        Test available bandwidth.

        Returns:
            dict: Bandwidth test results
        """
        result = {
            "test": "bandwidth",
            "status": "passed",
            "download_speed": 0,
            "upload_speed": 0,
        }
        self.test_results.append(result)
        return result

    def get_signal_strength(self):
        """
        Get current signal strength.

        Returns:
            dict: Signal strength information
        """
        return {
            "signal_strength": 0,
            "quality": "unknown",
            "satellites_visible": 0,
        }

    def get_test_history(self):
        """
        Get history of diagnostic tests.

        Returns:
            list: List of test results
        """
        return self.test_results

    def clear_test_history(self):
        """
        Clear diagnostic test history.

        Returns:
            bool: True if history cleared successfully
        """
        self.test_results = []
        return True

    def get_system_info(self):
        """
        Get system information and statistics.

        Returns:
            dict: System information
        """
        return {
            "health_status": self.health_status,
            "total_tests_run": len(self.test_results),
            "uptime": 0,
        }
