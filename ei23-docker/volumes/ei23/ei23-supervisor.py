"""
ei23 Smart Home Supervisor
==========================
Flask-based web dashboard for managing Docker containers, programs,
network scanning, and server administration.

Features:
    - Dashboard with live resource monitoring (CPU, RAM, Disk)
    - Container status display from docker-compose.yml
    - Program/link editor with drag-and-drop
    - Server action terminal with SSE streaming
    - Compose template manager
    - Local network scanner
    - Documentation server (MkDocs)
"""

"""
ei23 Smart Home Supervisor
==========================
Flask-based web dashboard for managing Docker containers, programs,
network scanning, and server administration.

Features:
    - Dashboard with live resource monitoring (CPU, RAM, Disk)
    - Container status display from docker-compose.yml
    - Program/link editor with drag-and-drop
    - Server action terminal with SSE streaming
    - Compose template manager
    - Local network scanner
    - Documentation server (MkDocs)
"""

import asyncio
import configparser
import json
import os
import shutil
import socket
import subprocess
import threading
import time
from datetime import datetime
from urllib.parse import urlparse
from typing import Union

import psutil
import requests
from flask import (
    Flask,
    Response,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from humanize import naturalsize
from ruamel.yaml import YAML
from waitress import serve


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

app = Flask(__name__, template_folder="web", static_folder="web/static")
app.config["TIMEOUT"] = 120

DEFAULT_CONFIG = {"Port": "80", "PeriodicScan": True}
CONFIG_FILE = "config.ini"

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
# Production layout:
#   /home/<user>/ei23-docker/volumes/ei23/ei23-supervisor.py  (this file)
#   /home/<user>/ei23.sh
#   /home/<user>/ei23-docker/                                 (Docker project root)
#
# All paths are derived from the script's own location, so it works regardless
# of CWD or whether the process runs as root or a regular user.

SUPERVISOR_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.path.abspath(os.path.join(SUPERVISOR_DIR, "..", "..", ".."))
DOCKERDIR = os.path.join(HOME_DIR, "ei23-docker")
EI23_SH = os.path.join(HOME_DIR, "ei23.sh")
PROGRAMS_JSON = os.path.join(SUPERVISOR_DIR, "web", "static", "programs.json")
PROGRAMS_TEMPLATES_JSON = os.path.join(SUPERVISOR_DIR, "web", "static", "programs_templates.json")
COMPOSE_TEMPLATES_DIR = os.path.join(DOCKERDIR, "compose_templates")
DOCKER_COMPOSE_FILE = os.path.join(DOCKERDIR, "docker-compose.yml")
MKDOCS_OUTPUT_DIR = "docs/site/"

# ei23.sh subcommands that require DOCKERDIR as working directory
EI23_COMMANDS_REQUIRING_DOCKERDIR = {"dc", "du", "update", "ei23update", "docs", "ha-addons"}

# Server actions – each maps to a shell command and a display label
SERVER_ACTIONS = {
    "update":       {"cmd": f"bash {EI23_SH} update",       "label": "System Update"},
    "dc":           {"cmd": f"bash {EI23_SH} dc",           "label": "Docker Compose"},
    "du":           {"cmd": f"bash {EI23_SH} du",           "label": "Docker Update"},
    "dstats":       {"cmd": "docker ps -a --format \"table {{.Names}}\\t{{.Status}}\\t{{.Ports}}\"", "label": "Docker Status"},
    "docker-prune": {"cmd": "docker image prune -a -f",     "label": "Docker Cleanup"},
    "docs":         {"cmd": f"bash {EI23_SH} docs",         "label": "Build Docs"},
    "ha-addons":    {"cmd": f"bash {EI23_SH} ha-addons",    "label": "HA Addons"},
    "ei23update":   {"cmd": f"bash {EI23_SH} ei23update",   "label": "ei23 Update"},
    "apt-update":   {"cmd": "sudo apt-get update -y && sudo apt-get upgrade -y", "label": "APT Update"},
    "reboot":       {"cmd": "sudo reboot",                  "label": "Reboot"},
}


def read_config() -> configparser.ConfigParser:
    """Read configuration from config.ini, falling back to defaults."""
    config = configparser.ConfigParser(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    return config


config = read_config()
port = config.get("DEFAULT", "Port")
periodic_scan = config.getboolean("DEFAULT", "PeriodicScan")


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

class ProgramInfo:
    """Represents a Docker service discovered from docker-compose.yml."""

    def __init__(self, name: str, ports: list[str], http: bool, network_mode: str):
        self.name = name
        self.ports = ports or []              # All external port mappings
        self.port = ports[0] if ports else "" # First port (backward compat)
        self.http = http                      # Whether HTTP responds on the port
        self.network_mode = network_mode or ""


# ---------------------------------------------------------------------------
# Global State
# ---------------------------------------------------------------------------

programs: list[ProgramInfo] = []
net_data: dict = {"devices": [], "timestamp": ""}

memory_usage: str = ""
disk_usage: str = ""
resource_data: dict = {
    "cpu": 0,
    "ram_used": 0,
    "ram_total": 1,
    "ram_pct": 0,
    "disk_used": "",
    "disk_total": "",
    "disk_pct": 0,
}

# Server action sessions: action_id -> {label, lines, running, status, exit_code, ...}
server_sessions: dict[str, dict] = {}


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def bytes_to_readable(num_bytes: float, suffix: str = "B") -> str:
    """Convert bytes to human-readable format (KB, MB, GB, etc.)."""
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:3.1f} {unit}{suffix}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} Y{suffix}"


def check_http(ip: str, port: int) -> bool:
    """Check if a service responds to HTTP on the given IP:port."""
    try:
        sock = socket.create_connection((ip, port), timeout=2)
        sock.close()
        requests.head(f"http://{ip}:{port}", timeout=10)
        return True
    except Exception:
        return False


def get_default_interface() -> Union[str, None]:
    """Detect the network interface used for the default route."""
    try:
        output = subprocess.check_output(["ip", "route", "show", "default"]).decode()
        return output.split()[4]
    except Exception as e:
        print(f"Failed to detect default interface: {e}")
        return None


# ---------------------------------------------------------------------------
# System Monitoring
# ---------------------------------------------------------------------------

def get_memory_usage() -> dict:
    """Get current RAM usage statistics."""
    mem = psutil.virtual_memory()
    return {
        "total": bytes_to_readable(mem.total),
        "available": bytes_to_readable(mem.available),
        "used": bytes_to_readable(mem.used),
        "free": bytes_to_readable(mem.free),
        "used_percentage": f"{mem.percent:.1f}%",
    }


def get_disk_usage(path: str = "/") -> dict:
    """Get disk usage statistics for the given mount point."""
    total, used, free = shutil.disk_usage(path)
    return {
        "total": bytes_to_readable(total),
        "used": bytes_to_readable(used),
        "free": bytes_to_readable(free),
        "used_percentage": f"{(used / total) * 100:.1f}%",
    }


async def resource_check() -> None:
    """Background task: poll CPU/RAM/Disk every 5 seconds."""
    global memory_usage, disk_usage, resource_data
    while True:
        disk = get_disk_usage("/")
        ram = get_memory_usage()
        cpu = psutil.cpu_percent(interval=1)

        disk_usage = f"DISK: [ {disk['used']} / {disk['total']} ] - {disk['used_percentage']}"
        memory_usage = f"RAM: [ {ram['used']} / {ram['total']} ] - {ram['used_percentage']}"
        resource_data = {
            "cpu": cpu,
            "ram_used": ram["used"],
            "ram_total": ram["total"],
            "ram_pct": float(ram["used_percentage"].rstrip("%")),
            "disk_used": disk["used"],
            "disk_total": disk["total"],
            "disk_pct": float(disk["used_percentage"].rstrip("%")),
        }
        await asyncio.sleep(5)


# ---------------------------------------------------------------------------
# Network Scanner
# ---------------------------------------------------------------------------

def ip_scan() -> None:
    """Scan the local network for devices using arp-scan."""
    global net_data
    net_data = {"devices": []}

    interface = get_default_interface()
    if not interface:
        print("No network interface found, skipping arp-scan.")
        return

    try:
        output = subprocess.check_output([
            "arp-scan", "--interface", interface, "--plain", "--ignoredups",
            "-l", "--resolve", "--format=${ip}\\t${Name}\\t${mac}\\t${vendor}"
        ]).decode()

        for line in output.splitlines():
            parts = line.split("\t")
            if len(parts) == 4:
                ip, host, mac, vendor = parts
                http_status = check_http(ip, 80)
                print(f"{host} {ip}")
                net_data["devices"].append({
                    "ip": ip, "host": host, "mac": mac,
                    "vendor": vendor, "http": http_status,
                })

    except subprocess.CalledProcessError:
        # Fallback: arp-scan without hostname resolution
        try:
            output = subprocess.check_output([
                "arp-scan", "--interface", interface, "--plain", "--ignoredups", "-l"
            ]).decode()
            for line in output.splitlines():
                parts = line.split("\t")
                if len(parts) == 3:
                    ip, mac, vendor = parts
                    http_status = check_http(ip, 80)
                    net_data["devices"].append({
                        "ip": ip, "host": ip, "mac": mac,
                        "vendor": vendor, "http": http_status,
                    })
        except subprocess.CalledProcessError as e:
            print(f"arp-scan failed: {e}")

    net_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


async def net_check() -> None:
    """Background task: refresh container status and scan network periodically."""
    global programs
    programs = get_yaml_programs()
    ip_scan()
    while periodic_scan:
        await asyncio.sleep(120)
        programs = get_yaml_programs()
        ip_scan()


# ---------------------------------------------------------------------------
# Docker Compose Parsing
# ---------------------------------------------------------------------------

def get_yaml_programs() -> list[ProgramInfo]:
    """Parse docker-compose.yml and return list of ProgramInfo for each service."""
    yaml = YAML(typ="safe", pure=True)
    with open(DOCKER_COMPOSE_FILE, "r") as f:
        data = yaml.load(f)

    result = []
    for service_name, service_config in data.get("services", {}).items():
        # Extract port mappings (host:container -> host_port)
        ports = []
        for p in service_config.get("ports", []):
            if isinstance(p, str):
                ports.append(p.split(":")[0])

        net_mode = service_config.get("network_mode", "")

        # Skip HTTP check for host networking or services without exposed ports
        if net_mode == "host" or not ports:
            http = False
        else:
            http = check_http("localhost", int(ports[0]))

        result.append(ProgramInfo(service_name, ports, http, net_mode))

    return result


# ---------------------------------------------------------------------------
# Dashboard Items (Homepage)
# ---------------------------------------------------------------------------

def create_items() -> str:
    """Build HTML for dashboard items from programs.json (active programs only)."""
    with open(PROGRAMS_JSON, "r") as f:
        program_list = json.load(f)["programs"]

    items = []
    parsed_url = urlparse(request.url_root)
    base_url = f"{parsed_url.scheme}://{parsed_url.hostname}"

    for program in program_list:
        if not program.get("active"):
            continue

        # Build link: custom_url overrides default port-based URL
        link = f"{base_url}:{program['port']}"
        if program.get("custom_url"):
            link = program["custom_url"]
            if link == "https":
                link = f"https://{parsed_url.hostname}:{program['port']}"

        items.append(f'''
            <section class="item-container">
                <a title="{program['name']} - {program['title']}" class="white" href="{link}" target="_blank" style="text-decoration: none;">
                    <div class="item">
                        <img class="app-icon" src="static/{program['img']}">
                        <div class="details">
                            <div class="title white">{program['name']}</div>
                            <small>{program['title']}</small>
                        </div>
                    </div>
                </a>
            </section>
        ''')

    return "".join(items)


# ---------------------------------------------------------------------------
# HTML Page Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Render the main dashboard."""
    header = render_template("dashboard-head.html")
    navbar = render_template("navbar.html").replace(
        'dashboard-placeholder"', 'active" aria-current="page"'
    )
    bottom_logo = render_template(
        "bottom-logo.html", disk=disk_usage, ram=memory_usage
    )
    return render_template(
        "index.html",
        header=header,
        navbar=navbar,
        items=create_items(),
        bottom_logo=bottom_logo,
    )


@app.route("/server")
def server():
    """Render the server administration page with container cards."""
    header = render_template("dashboard-head.html")
    navbar = render_template("navbar.html").replace(
        'server-placeholder"', 'active" aria-current="page"'
    )
    bottom_logo = render_template(
        "bottom-logo.html", disk=disk_usage, ram=memory_usage
    )

    # Build deduplicated container cards from docker-compose services
    container_cards = ""
    seen: set[str] = set()

    for pi in sorted(programs, key=lambda x: x.name):
        if pi.name in seen:
            continue
        seen.add(pi.name)

        # Port display label
        if pi.network_mode == "host":
            port_label = "Host Network"
        elif pi.ports:
            port_label = ", ".join(pi.ports)
        else:
            port_label = "internal"

        # Status badge
        if pi.http:
            status_cls, status_txt = "status-http", "HTTP Available"
        elif pi.network_mode == "host":
            status_cls, status_txt = "status-host", "Host Mode"
        elif pi.ports:
            status_cls, status_txt = "status-port", "Port Active"
        else:
            status_cls, status_txt = "status-internal", "Internal"

        # Link (only if HTTP responds)
        if pi.http and pi.port:
            link = f"href='{request.url_root.rstrip('/')}:{pi.port}' target='_blank'"
        elif pi.http:
            link = f"href='{request.url_root.rstrip('/')}' target='_blank'"
        else:
            link = ""

        status_html = f'<span class="container-status {status_cls}">{status_txt}</span>'
        container_cards += f'''
            <div class="col-md-3 col-6">
                <div class="card" style="background:rgba(0,0,0,0.4);border:1px solid #555;">
                    <div class="card-body p-2 text-center">
                        <a {link} style="text-decoration:none;color:#fff;">
                            <div class="fw-bold" style="font-size:0.9rem;">{pi.name}</div>
                            <small style="color:#999;">{port_label}</small><br>
                            {status_html}
                        </a>
                    </div>
                </div>
            </div>'''

    return render_template(
        "server.html",
        header=header,
        navbar=navbar,
        container_cards=container_cards,
        bottom_logo=bottom_logo,
    )


@app.route("/localnet")
def localnet():
    """Render the local network scan page."""
    header = render_template("dashboard-head.html")
    navbar = render_template("navbar.html").replace(
        'localnet-placeholder"', 'active" aria-current="page"'
    )
    bottom_logo = render_template(
        "bottom-logo.html", disk=disk_usage, ram=memory_usage
    )

    # Build device table rows
    scan_result = ""
    sorted_devices = sorted(net_data["devices"], key=lambda x: x["host"].casefold())
    for device in sorted_devices:
        ip_link = (
            f"<a href='http://{device['ip']}' target='_blank'>{device['ip']}</a>"
            if device["http"] else device["ip"]
        )
        host_link = (
            f"<a href='http://{device['host']}' target='_blank'>{device['host']}</a>"
            if device["http"] else device["host"]
        )
        scan_result += f"<tr><td>{host_link}</td><td>{ip_link}</td><td>{device['mac']}</td><td>{device['vendor']}</td></tr>"

    return render_template(
        "localnet.html",
        header=header,
        navbar=navbar,
        scan_result=scan_result,
        bottom_logo=bottom_logo,
    )


@app.route("/tree")
def tree():
    """Render the disk usage tree view."""
    header = render_template("dashboard-head.html")
    navbar = render_template("navbar.html").replace(
        'dashboard-placeholder"', 'active" aria-current="page"'
    )
    bottom_logo = render_template(
        "bottom-logo.html", disk=disk_usage, ram=memory_usage
    )
    path = request.args.get("path", "../../../")
    parent_path = os.path.dirname(path) if path != "." else None
    return render_template(
        "tree.html",
        tree=get_directory_size(path),
        path=path,
        parent_path=parent_path,
        header=header,
        navbar=navbar,
        bottom_logo=bottom_logo,
    )


def get_directory_size(start_path: str = ".") -> list[dict]:
    """Recursively calculate directory sizes, returning a tree structure."""
    def _get_size(path: str, depth: int):
        total_size = 0
        children = []
        for entry in os.scandir(path):
            if entry.is_file():
                size = entry.stat().st_size
                total_size += size
                children.append({
                    "path": entry.path,
                    "name": entry.name,
                    "size": size,
                    "size_hr": naturalsize(size),
                    "type": "file",
                })
            elif entry.is_dir():
                size, sub_children = _get_size(entry.path, depth + 1)
                total_size += size
                children.append({
                    "path": entry.path,
                    "name": entry.name,
                    "size": size,
                    "size_hr": naturalsize(size),
                    "type": "directory",
                    "children": sub_children,
                })
        children.sort(key=lambda x: x["size"], reverse=True)
        return total_size, children

    _, tree = _get_size(start_path, 0)
    return tree


@app.route("/scan")
def scan():
    """Trigger a network scan and redirect to localnet page."""
    ip_scan()
    return redirect(url_for("localnet"))


@app.route("/refresh_programs")
def refresh_programs():
    """Refresh container status from docker-compose.yml and redirect to server page."""
    global programs
    programs = get_yaml_programs()
    return redirect(url_for("server"))


@app.errorhandler(404)
def not_found_error(error):
    """Render custom 404 page."""
    return render_template("404.html"), 404


# ---------------------------------------------------------------------------
# Documentation Routes (MkDocs)
# ---------------------------------------------------------------------------

@app.route("/docs/")
@app.route("/docs/<path:filename>")
def serve_docs(filename: str = "index.html"):
    """Serve built MkDocs documentation, building on first access if needed."""
    if not os.path.exists(MKDOCS_OUTPUT_DIR):
        make_docs_cmd()

    full_path = os.path.join(MKDOCS_OUTPUT_DIR, filename)
    if os.path.isdir(full_path):
        filename = os.path.join(filename, "index.html")

    return send_from_directory(MKDOCS_OUTPUT_DIR, filename)


@app.route("/make_docs")
def make_docs():
    """Rebuild documentation and redirect to docs page."""
    make_docs_cmd()
    return redirect(url_for("server"))


def make_docs_cmd():
    """Build MkDocs documentation using the project's virtual environment."""
    docs_path = subprocess.check_output(["pwd"]).decode().strip()
    command = (
        f"bash -c 'cd {docs_path}/; "
        f"source .venv/bin/activate; cd docs/; mkdocs build; deactivate'"
    )
    subprocess.run(command, shell=True)


# ---------------------------------------------------------------------------
# Server Actions API (SSE with Session Tracking)
# ---------------------------------------------------------------------------

def start_server_session(action: str) -> Union[str, None]:
    """Start a server action as a background process with session tracking.

    Returns the session ID (same as action name), or None if action is unknown.
    If the action is already running, returns the existing session ID.
    """
    if action not in SERVER_ACTIONS:
        return None

    # Don't start duplicate processes
    if action in server_sessions and server_sessions[action]["running"]:
        return action

    info = SERVER_ACTIONS[action]
    cwd = DOCKERDIR if action in EI23_COMMANDS_REQUIRING_DOCKERDIR else None

    server_sessions[action] = {
        "label": info["label"],
        "lines": [],
        "running": True,
        "status": "running",
        "exit_code": None,
        "started_at": datetime.now().strftime("%H:%M:%S"),
    }

    def run_process():
        try:
            # Pass HOME so ei23.sh (which uses $HOME/ei23-docker) resolves correctly
            env = {**os.environ, "HOME": HOME_DIR}
            proc = subprocess.Popen(
                info["cmd"],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=cwd,
                env=env,
                text=True,
                bufsize=1,
            )
            for line in iter(proc.stdout.readline, ""):
                server_sessions[action]["lines"].append(line.rstrip())
            proc.stdout.close()
            proc.wait()
            server_sessions[action]["running"] = False
            server_sessions[action]["exit_code"] = proc.returncode
            server_sessions[action]["status"] = "success" if proc.returncode == 0 else "error"
        except Exception as e:
            server_sessions[action]["running"] = False
            server_sessions[action]["status"] = "error"
            server_sessions[action]["lines"].append(f"ERROR: {e}")

    threading.Thread(target=run_process, daemon=True).start()
    return action


@app.route("/api/server-action/<action>")
def server_action(action: str):
    """Stream server action output via Server-Sent Events (SSE).

    Supports reconnection: clients receive all buffered output from the start.
    """
    if action not in SERVER_ACTIONS:
        return jsonify({"error": "Unknown action"}), 400

    session_id = start_server_session(action)

    def generate():
        session = server_sessions.get(session_id)
        if not session:
            yield f"data: {json.dumps({'error': 'Session not found'})}\n\n"
            return

        yield f"data: {json.dumps({'start': True, 'label': session['label'], 'session_id': session_id})}\n\n"

        sent_count = 0
        while True:
            session = server_sessions.get(session_id)
            if not session:
                break

            # Send any new lines
            while sent_count < len(session["lines"]):
                yield f"data: {json.dumps({'line': session['lines'][sent_count]})}\n\n"
                sent_count += 1

            # Check if process finished
            if not session["running"]:
                yield f"data: {json.dumps({'done': True, 'status': session['status'], 'exit_code': session['exit_code']})}\n\n"
                break

            time.sleep(0.3)

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/api/server-sessions")
def api_server_sessions():
    """Return all server action sessions (for reconnection after page reload)."""
    result = [
        {
            "id": sid,
            "label": s["label"],
            "running": s["running"],
            "status": s["status"],
            "lines_count": len(s["lines"]),
            "started_at": s["started_at"],
        }
        for sid, s in server_sessions.items()
    ]
    return jsonify({"sessions": result})


@app.route("/api/server-action/<action>/cancel", methods=["POST"])
def cancel_server_action(action: str):
    """Remove a session from tracking (works for both running and finished)."""
    if action in server_sessions:
        server_sessions[action]["running"] = False
        server_sessions[action]["status"] = "cancelled"
        del server_sessions[action]
        return jsonify({"success": True})
    return jsonify({"error": "Session not found"}), 404


# ---------------------------------------------------------------------------
# Programs API
# ---------------------------------------------------------------------------

@app.route("/api/programs", methods=["GET"])
def api_get_programs():
    """Return all programs from programs.json."""
    try:
        with open(PROGRAMS_JSON, "r") as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/programs", methods=["POST"])
def api_save_programs():
    """Save programs list to programs.json.

    Expects JSON body: {"programs": [{name, img, active, port, custom_url, title}, ...]}
    """
    try:
        data = request.get_json()
        if not data or "programs" not in data:
            return jsonify({"success": False, "error": "Invalid data"}), 400

        for i, program in enumerate(data["programs"]):
            if "name" not in program or "img" not in program:
                return jsonify({"success": False, "error": f"Program {i+1} missing name or img"}), 400
            program.setdefault("active", False)
            program.setdefault("port", "")
            program.setdefault("custom_url", "")
            program.setdefault("title", "")

        with open(PROGRAMS_JSON, "w") as f:
            json.dump(data, f, indent=2)

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/programs/fill-from-templates", methods=["POST"])
def api_fill_from_templates():
    """Add missing programs from programs_templates.json (as inactive).

    Matches by 'img' field to avoid duplicates. Returns list of added names.
    """
    try:
        if not os.path.exists(PROGRAMS_TEMPLATES_JSON):
            return jsonify({"success": False, "error": "Template file not found"}), 404

        with open(PROGRAMS_JSON, "r") as f:
            current = json.load(f)

        with open(PROGRAMS_TEMPLATES_JSON, "r") as f:
            templates = json.load(f)

        existing_imgs = {p["img"] for p in current["programs"]}
        added = []

        for tpl in templates["programs"]:
            if tpl["img"] not in existing_imgs:
                new_entry = dict(tpl)
                new_entry["active"] = False
                current["programs"].append(new_entry)
                added.append(new_entry["name"])

        with open(PROGRAMS_JSON, "w") as f:
            json.dump(current, f, indent=2)

        return jsonify({"success": True, "added": added})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ---------------------------------------------------------------------------
# Compose Templates API
# ---------------------------------------------------------------------------

@app.route("/api/compose-templates")
def api_compose_templates():
    """List available compose templates with their installation status."""
    try:
        if not os.path.exists(COMPOSE_TEMPLATES_DIR):
            return jsonify({"templates": []})

        yaml = YAML(typ="safe", pure=True)
        with open(DOCKER_COMPOSE_FILE, "r") as f:
            dc_data = yaml.load(f)
        installed_services = set(dc_data.get("services", {}).keys())

        templates = []
        for fname in sorted(os.listdir(COMPOSE_TEMPLATES_DIR)):
            if not fname.endswith(".yml"):
                continue

            tpl_path = os.path.join(COMPOSE_TEMPLATES_DIR, fname)
            with open(tpl_path, "r") as f:
                tpl_data = yaml.load(f)

            tpl_services = list(tpl_data.get("services", {}).keys()) if tpl_data else []
            is_installed = all(svc in installed_services for svc in tpl_services) if tpl_services else False

            templates.append({
                "file": fname,
                "name": fname[:-4],  # strip .yml
                "services": tpl_services,
                "installed": is_installed,
            })

        return jsonify({"templates": templates})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/compose-templates/<filename>", methods=["POST"])
def api_compose_add_template(filename: str):
    """Append a compose template to docker-compose.yml and activate matching programs.

    After adding, run 'Docker Compose' action to start the new containers.
    """
    try:
        if not filename.endswith(".yml"):
            return jsonify({"success": False, "error": "Invalid file"}), 400

        tpl_path = os.path.join(COMPOSE_TEMPLATES_DIR, filename)
        if not os.path.exists(tpl_path):
            return jsonify({"success": False, "error": "Template not found"}), 404

        # Append template content to docker-compose.yml
        with open(tpl_path, "r") as f:
            tpl_content = f.read()

        with open(DOCKER_COMPOSE_FILE, "a") as f:
            f.write(f"\n\n{tpl_content}\n")

        # Activate matching programs in programs.json
        yaml = YAML(typ="safe", pure=True)
        with open(tpl_path, "r") as f:
            tpl_data = yaml.load(f)

        with open(PROGRAMS_JSON, "r") as f:
            programs_data = json.load(f)

        for svc_name in tpl_data.get("services", {}).keys():
            for entry in programs_data.get("programs", []):
                if entry["name"].lower() == svc_name.lower():
                    entry["active"] = True
                    break

        with open(PROGRAMS_JSON, "w") as f:
            json.dump(programs_data, f, indent=2)

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ---------------------------------------------------------------------------
# Resources API
# ---------------------------------------------------------------------------

@app.route("/api/resources")
def api_resources():
    """Return current CPU/RAM/Disk usage as JSON (polled by dashboard)."""
    return jsonify(resource_data)


# ---------------------------------------------------------------------------
# Server Startup
# ---------------------------------------------------------------------------

async def start_server() -> None:
    """Start the Waitress WSGI server in a background thread."""
    await asyncio.to_thread(serve, app, host="0.0.0.0", port=port)


async def main() -> None:
    """Launch all background tasks and the web server concurrently."""
    await asyncio.gather(
        resource_check(),
        start_server(),
        net_check(),
    )


if __name__ == "__main__":
    asyncio.run(main())
