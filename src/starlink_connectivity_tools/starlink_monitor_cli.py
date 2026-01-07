#!/usr/bin/env python3
"""Command-line interface for Starlink monitoring and management."""

import time
import sys
from datetime import datetime

import click
from rich.console import Console
from rich.table import Table
from loguru import logger

from starlink_connectivity_tools import (
    StarlinkAPI,
    SatelliteConnectionManager,
    CrisisMonitor,
    DiagnosticsEngine,
)
from starlink_connectivity_tools.satellite_connection_manager import ConnectionType
from starlink_connectivity_tools.crisis_monitor import ScenarioType


console = Console()


def get_status_color(status: str) -> str:
    """Get color for status display."""
    colors = {
        "healthy": "green",
        "connected": "green",
        "warning": "yellow",
        "degraded": "yellow",
        "critical": "red",
        "failed": "red",
        "disconnected": "red",
    }
    return colors.get(status.lower(), "white")


def create_status_table(health_data: dict) -> Table:
    """Create a table showing connection status."""
    table = Table(title="Connection Status", show_header=True)
    table.add_column("Connection", style="cyan")
    table.add_column("Type", style="blue")
    table.add_column("Status", style="white")
    table.add_column("Priority", justify="right")
    table.add_column("Latency (ms)", justify="right")
    table.add_column("Down (Mbps)", justify="right")
    table.add_column("Up (Mbps)", justify="right")

    for conn in health_data.get("connections", []):
        metrics = conn.get("metrics", {})
        status = conn.get("status", "unknown")
        color = get_status_color(status)

        table.add_row(
            conn.get("name", "Unknown"),
            conn.get("type", "unknown"),
            f"[{color}]{status}[/{color}]",
            str(conn.get("priority", 0)),
            f"{metrics.get('latency_ms', 0):.1f}",
            f"{metrics.get('downlink_mbps', 0):.1f}",
            f"{metrics.get('uplink_mbps', 0):.1f}",
        )

    return table


def create_issues_table(monitor_data: dict) -> Table:
    """Create a table showing active issues."""
    table = Table(title="Active Issues", show_header=True)
    table.add_column("Type", style="cyan")
    table.add_column("Severity", style="white")
    table.add_column("Description")
    table.add_column("Count", justify="right")

    for issue in monitor_data.get("active_issues", []):
        severity = issue.get("severity", "unknown")
        color = get_status_color(severity)

        table.add_row(
            issue.get("type", "unknown"),
            f"[{color}]{severity}[/{color}]",
            issue.get("description", "No description"),
            str(issue.get("occurrence_count", 1)),
        )

    if not monitor_data.get("active_issues"):
        table.add_row("None", "[green]healthy[/green]", "No issues detected", "0")

    return table


def create_alerts_table(diagnostic_data: dict) -> Table:
    """Create a table showing diagnostic alerts."""
    table = Table(title="Diagnostic Alerts", show_header=True)
    table.add_column("Type", style="cyan")
    table.add_column("Severity", style="white")
    table.add_column("Message")
    table.add_column("Recommendation")

    for alert in diagnostic_data.get("alerts", []):
        severity = alert.get("severity", "unknown")
        color = get_status_color(severity)

        table.add_row(
            alert.get("type", "unknown"),
            f"[{color}]{severity}[/{color}]",
            alert.get("message", "No message"),
            alert.get("recommendation", "No recommendation"),
        )

    if not diagnostic_data.get("alerts"):
        table.add_row(
            "None", "[green]info[/green]", "All systems normal", "Continue monitoring"
        )

    return table


@click.group()
@click.option("--debug", is_flag=True, help="Enable debug logging")
def cli(debug):
    """Starlink connectivity monitoring and management CLI."""
    if debug:
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.remove()
        logger.add(sys.stderr, level="INFO")


@cli.command()
@click.option(
    "--target", default=None, help="Starlink gRPC target (default: 192.168.100.1:9200)"
)
@click.option("--simulation", is_flag=True, help="Use simulation mode")
def status(target, simulation):
    """Display current Starlink status."""
    try:
        api = StarlinkAPI(target=target, simulation_mode=simulation)
        status_data = api.get_status()

        console.print("\n[bold cyan]Starlink Dish Status[/bold cyan]\n")

        # State
        state = status_data.get("state", "UNKNOWN")
        state_color = get_status_color(state)
        console.print(f"State: [{state_color}]{state}[/{state_color}]")

        # Metrics
        console.print(f"Uptime: {status_data.get('uptime', 0)} seconds")
        console.print(f"Latency: {status_data.get('ping_latency_ms', 0):.1f} ms")
        console.print(
            f"Downlink: {status_data.get('downlink_throughput_bps', 0) / 1_000_000:.1f} Mbps"
        )
        console.print(
            f"Uplink: {status_data.get('uplink_throughput_bps', 0) / 1_000_000:.1f} Mbps"
        )
        console.print(f"SNR: {status_data.get('snr', 0):.1f} dB")

        # Obstructions
        obstructed = status_data.get("obstructed", False)
        obs_color = "red" if obstructed else "green"
        obs_pct = status_data.get("obstruction_percent", 0) * 100
        console.print(
            f"Obstructed: [{obs_color}]{obstructed}[/{obs_color}] ({obs_pct:.1f}%)"
        )

        # Alerts
        alerts = status_data.get("alerts", [])
        if alerts:
            console.print("\n[yellow]Alerts:[/yellow]")
            for alert in alerts:
                console.print(f"  • {alert}")

        console.print()
        api.close()

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option("--interval", default=10, help="Update interval in seconds")
@click.option(
    "--scenario",
    type=click.Choice(["normal", "humanitarian", "medical", "disaster", "conflict"]),
    default="normal",
    help="Monitoring scenario",
)
@click.option("--simulation", is_flag=True, help="Use simulation mode")
def monitor(interval, scenario, simulation):
    """Real-time monitoring with automatic issue detection."""
    try:
        # Setup
        manager = SatelliteConnectionManager()
        manager.add_connection(
            "Starlink Primary",
            ConnectionType.STARLINK,
            priority=100,
            simulation_mode=simulation,
        )

        scenario_enum = ScenarioType[scenario.upper()]
        monitor = CrisisMonitor(manager, scenario=scenario_enum)
        diagnostics = DiagnosticsEngine(manager)

        # Connect
        if not manager.connect():
            console.print("[red]Failed to establish connection[/red]")
            sys.exit(1)

        console.print(
            f"[green]Monitoring started[/green] (scenario: {scenario}, interval: {interval}s)"
        )
        console.print("Press Ctrl+C to stop\n")

        try:
            while True:
                # Gather data
                health_data = monitor.check_health()
                diagnostic_data = diagnostics.run_full_diagnostic()

                # Clear screen and display
                console.clear()
                console.print(
                    f"[bold]Starlink Monitor[/bold] - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                console.print(
                    f"Scenario: [cyan]{scenario}[/cyan] | Status: [{get_status_color(health_data['status'])}]{health_data['status']}[/{get_status_color(health_data['status'])}]\n"
                )

                # Display tables
                console.print(create_status_table(health_data.get("health", {})))
                console.print()
                console.print(create_issues_table(health_data))
                console.print()
                console.print(create_alerts_table(diagnostic_data))

                time.sleep(interval)

        except KeyboardInterrupt:
            console.print("\n[yellow]Monitoring stopped[/yellow]")

        finally:
            manager.close_all()

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option("--hours", default=24, help="Hours of data to include in report")
@click.option("--output", default="performance_report.json", help="Output file path")
@click.option("--simulation", is_flag=True, help="Use simulation mode")
def report(hours, output, simulation):
    """Generate performance report."""
    try:
        manager = SatelliteConnectionManager()
        manager.add_connection(
            "Starlink Primary",
            ConnectionType.STARLINK,
            priority=100,
            simulation_mode=simulation,
        )

        monitor = CrisisMonitor(manager)

        if not manager.connect():
            console.print("[red]Failed to establish connection[/red]")
            sys.exit(1)

        console.print(f"Generating performance report for last {hours} hours...")

        # Collect some data
        for i in range(10):
            monitor.check_health()
            time.sleep(1)

        report_data = monitor.get_performance_report(hours=hours)

        # Display summary
        console.print("\n[bold cyan]Performance Summary[/bold cyan]\n")

        if "error" not in report_data:
            console.print(f"Samples: {report_data['samples']}")
            console.print("\nLatency:")
            console.print(f"  Average: {report_data['latency_ms']['avg']:.1f} ms")
            console.print(f"  Min: {report_data['latency_ms']['min']:.1f} ms")
            console.print(f"  Max: {report_data['latency_ms']['max']:.1f} ms")
            console.print(f"  P95: {report_data['latency_ms']['p95']:.1f} ms")

            console.print("\nDownlink:")
            console.print(f"  Average: {report_data['downlink_mbps']['avg']:.1f} Mbps")
            console.print(f"  Min: {report_data['downlink_mbps']['min']:.1f} Mbps")
            console.print(f"  Max: {report_data['downlink_mbps']['max']:.1f} Mbps")

            console.print("\nIssues:")
            console.print(f"  Total: {report_data['total_issues']}")
            console.print(f"  Resolved: {report_data['resolved_issues']}")
            console.print(f"  Active: {report_data['active_issues']}")

        # Export data
        monitor.export_data(output, hours=hours)
        console.print(f"\n[green]Report exported to {output}[/green]")

        manager.close_all()

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option("--target", default=None, help="Starlink gRPC target")
@click.option("--simulation", is_flag=True, help="Use simulation mode")
def reboot(target, simulation):
    """Reboot the Starlink dish."""
    try:
        api = StarlinkAPI(target=target, simulation_mode=simulation)

        if click.confirm("Are you sure you want to reboot the dish?"):
            console.print("Rebooting dish...")
            if api.reboot():
                console.print("[green]Reboot command sent successfully[/green]")
                console.print("Dish will be offline for approximately 1-2 minutes")
            else:
                console.print("[red]Failed to send reboot command[/red]")

        api.close()

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option("--target", default=None, help="Starlink gRPC target")
@click.option("--simulation", is_flag=True, help="Use simulation mode")
def stow(target, simulation):
    """Stow the Starlink dish."""
    try:
        api = StarlinkAPI(target=target, simulation_mode=simulation)

        if click.confirm("Stow the dish? (This will disconnect the connection)"):
            console.print("Stowing dish...")
            if api.stow():
                console.print("[green]Stow command sent successfully[/green]")
            else:
                console.print("[red]Failed to send stow command[/red]")

        api.close()

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option("--target", default=None, help="Starlink gRPC target")
@click.option("--simulation", is_flag=True, help="Use simulation mode")
def unstow(target, simulation):
    """Unstow the Starlink dish."""
    try:
        api = StarlinkAPI(target=target, simulation_mode=simulation)

        console.print("Unstowing dish...")
        if api.unstow():
            console.print("[green]Unstow command sent successfully[/green]")
            console.print("Dish will search for satellites")
        else:
            console.print("[red]Failed to send unstow command[/red]")

        api.close()

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option("--simulation", is_flag=True, help="Use simulation mode")
def diagnostics(simulation):
    """Run full diagnostics."""
    try:
        manager = SatelliteConnectionManager()
        manager.add_connection(
            "Starlink Primary",
            ConnectionType.STARLINK,
            priority=100,
            simulation_mode=simulation,
        )

        diagnostics_engine = DiagnosticsEngine(manager)

        if not manager.connect():
            console.print("[red]Failed to establish connection[/red]")
            sys.exit(1)

        console.print("Running diagnostics...\n")

        result = diagnostics_engine.run_full_diagnostic()

        status = result.get("status", "unknown")
        status_color = get_status_color(status)
        console.print(
            f"Overall Status: [{status_color}]{status.upper()}[/{status_color}]\n"
        )

        console.print(create_alerts_table(result))

        # Save report
        output_file = "diagnostic_report.json"
        diagnostics_engine.generate_diagnostic_report(output_file)
        console.print(f"\n[green]Full diagnostic report saved to {output_file}[/green]")

        manager.close_all()

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
