from datetime import datetime
from flask import Flask, render_template, redirect, url_for, send_from_directory, request, jsonify
from ruamel.yaml import YAML
from waitress import serve
from humanize import naturalsize
import requests
import json, socket, subprocess, os
import shutil
import psutil
import asyncio
import configparser

app = Flask(__name__, template_folder='web', static_folder='web/static')
app.config['TIMEOUT'] = 120

# Default Config
DEFAULT_CONFIG = {
    'Port': '80', 
    'PeriodicScan': True
}

CONFIG_FILE = 'config.ini'
# create config.ini like this
# [DEFAULT]
# Port = 8080
# PeriodicScan = False


def read_config():
    config = configparser.ConfigParser(DEFAULT_CONFIG)
    # Prüfen, ob die Konfigurationsdatei existiert
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    return config

config = read_config()
port = config.get('DEFAULT', 'Port')
periodic_scan = config.getboolean('DEFAULT', 'PeriodicScan')

# url_root_without_port = request.url_root.rstrip.replace(f':{request.environ["SERVER_PORT"]}', '')

@app.route('/')
def index():
    header = render_template('dashboard-head.html')
    navbar = render_template('navbar.html').replace("dashboard-placeholder\"", "active\" aria-current=\"page\"")
    items = create_items()
    disk = disk_usage
    ram = memory_usage
    bottom_logo = render_template('bottom-logo.html', disk=disk, ram=ram)
    return render_template('index.html', header=header, navbar=navbar, items=items, bottom_logo=bottom_logo)

def get_directory_size(start_path='.'):
    tree = []
    def _get_size(path, depth):
        total_size = 0
        children = []
        for entry in os.scandir(path):
            if entry.is_file():
                size = entry.stat().st_size
                total_size += size
                children.append({
                    'path': entry.path,
                    'name': entry.name,
                    'size': size,
                    'size_hr': naturalsize(size),
                    'type': 'file'
                })
            elif entry.is_dir():
                size, sub_children = _get_size(entry.path, depth + 1)
                total_size += size
                children.append({
                    'path': entry.path,
                    'name': entry.name,
                    'size': size,
                    'size_hr': naturalsize(size),
                    'type': 'directory',
                    'children': sub_children
                })
        children.sort(key=lambda x: x['size'], reverse=True)
        return total_size, children

    total_size, tree = _get_size(start_path, 0)
    return tree

# Treesize Speicherbelegung
@app.route('/tree')
def tree():
    header = render_template('dashboard-head.html')
    navbar = render_template('navbar.html').replace("dashboard-placeholder\"", "active\" aria-current=\"page\"")
    items = create_items()
    disk = disk_usage
    ram = memory_usage
    bottom_logo = render_template('bottom-logo.html', disk=disk, ram=ram)
    path = request.args.get('path', '../../../')
    tree = get_directory_size(path)
    parent_path = os.path.dirname(path) if path != '.' else None
    return render_template('tree.html', tree=tree, path=path, parent_path=parent_path, header=header, navbar=navbar, bottom_logo=bottom_logo)

@app.route('/localnet')
def localnet():
    global net_data
    header = render_template('dashboard-head.html')
    navbar = render_template('navbar.html').replace("localnet-placeholder\"", "active\" aria-current=\"page\"")
    disk = disk_usage
    ram = memory_usage
    bottom_logo = render_template('bottom-logo.html', disk=disk, ram=ram)
    scan_result = ""
    data = net_data
    sorted_devices = sorted(data['devices'], key=lambda x: x['host'].casefold())
    for device in sorted_devices:
        ip_link = f"<a href={'http://' + device['ip']} target='_blank'>{device['ip']}</a>" if device['http'] else device['ip']
        host_link = f"<a href={'http://' + device['host']} target='_blank'>{device['host']}</a>" if device['http'] else device['host']
        
        scan_result += f"<tr><td>{host_link}</td><td>{ip_link}</td><td>{device['mac']}</td><td>{device['vendor']}</td></tr>"

    return render_template('localnet.html', header=header, navbar=navbar, scan_result=scan_result, bottom_logo=bottom_logo)


@app.route('/scan')
def scan():
    ip_scan()
    return redirect(url_for('localnet'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Docs Ansicht
mkdocs_directory = 'docs/site/'
@app.route('/docs/')
@app.route('/docs/<path:filename>')
def serve_docs(filename='index.html'):
    # build docs wenn nicht vorhanden
    if not os.path.exists(mkdocs_directory):
        make_docs_cmd()
    full_path = os.path.join(mkdocs_directory, filename)
    # Überprüfe, ob der angegebene Dateiname ein Verzeichnis ist
    if os.path.isdir(full_path):
        # Wenn es sich um ein Verzeichnis handelt, füge 'index.html' hinzu
        filename = os.path.join(filename, 'index.html')
    return send_from_directory(mkdocs_directory, filename)

@app.route('/make_docs')
def make_docs():
    make_docs_cmd()
    return redirect(url_for('server'))

def make_docs_cmd():
    # pfad fuer root command holen
    docs_path = subprocess.check_output(['pwd']).decode('utf-8')
    # build docs
    command = 'bash -c \'cd '+docs_path+'/; source .venv/bin/activate; cd docs/; mkdocs build; deactivate\''
    subprocess.run(command, shell=True)

# Server Ansicht
@app.route('/server')
def server():
    global programs
    header = render_template('dashboard-head.html')
    navbar = render_template('navbar.html').replace("server-placeholder\"", "active\" aria-current=\"page\"")
    disk = disk_usage
    ram = memory_usage
    bottom_logo = render_template('bottom-logo.html', disk=disk, ram=ram)
    table = ""
    sorted_programs = sorted(programs, key=lambda x: x.name)
    for programm_info in sorted_programs:
        port = programm_info.port
        if not programm_info.port:
            port = "HOST/INTERN"
        if programm_info.http:
            table += f"<tr><td><a href='{request.url_root.rstrip('/')}:{port}' target='_blank' >{programm_info.name} ({port})</a></td><td>{port}</td><td>{'&#x2705;' if programm_info.http else '&#x274C;'}</td></tr>\n"
        else:
            table += f"<tr><td>{programm_info.name} ({port})</td><td>{port}</td><td>{'&#x2705;' if programm_info.http else '&#x274C;'}</td></tr>\n"
    return render_template('server.html', header=header, navbar=navbar, table=table, bottom_logo=bottom_logo)

@app.route('/refresh_programs')
def refresh_programs():
    global programs
    merge_json_files('web/static/programs.json', 'web/static/programs_templates.json')
    programs = get_yaml_programs()
    return redirect(url_for('server'))

# Neue Programme in programs.json aus Template einfügen
def merge_json_files(target_filename, template_filename):
    # Öffne die JSON-Dateien
    with open(target_filename, 'r') as target_file:
        target_data = json.load(target_file)

    with open(template_filename, 'r') as template_file:
        template_data = json.load(template_file)

    # Liste für spezielle Einträge
    special_entries = []

    # Iteriere durch die Einträge der Vorlagendatei
    for template_entry in template_data['programs']:
        template_img = template_entry['img']

        # Überprüfe, ob der Eintrag bereits in der Zieldatei vorhanden ist
        existing_entry = next((entry for entry in target_data['programs'] if entry['img'] == template_img), None)

        # Füge den Eintrag hinzu, falls er nicht vorhanden ist
        if existing_entry is None:
            if template_img == "img/docs.png":
                special_entries.append(template_entry)
            else:
                target_data['programs'].append(template_entry)

    # Füge die speziellen Einträge ans Ende der Liste
    target_data['programs'].extend(special_entries)

    # Schreibe die aktualisierten Daten zurück in die Zieldatei
    with open(target_filename, 'w') as updated_file:
        json.dump(target_data, updated_file, indent=None)

    # Füge manuell Zeilenumbrüche nach "},{" hinzu
    with open(target_filename, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace('}, {', '},\n{').replace('[{', '[\n{').replace(']}', '\n]}'))

def get_default_interface():
    # Ermittelt das Interface, das für die Standardroute verwendet wird
    try:
        route_output = subprocess.check_output(['ip', 'route', 'show', 'default']).decode('utf-8')
        # Extrahiere das Interface (5. Feld)
        interface = route_output.split()[4]
        return interface
    except Exception as e:
        print(f"Fehler beim Ermitteln des Standard-Interfaces: {e}")
        return None

net_data = []

def ip_scan():
    global net_data
    net_data = {'devices': []}

    interface = get_default_interface()
    if interface is None:
        print("Kein Interface gefunden, arp-scan kann nicht ausgeführt werden.")
        return

    try:
        # arp-scan --plain --ignoredups -l --format='${ip}\t${Name}\t${mac}\t${vendor}'
        arp_scan_output = subprocess.check_output([
            'arp-scan', '--interface', interface, '--plain', '--ignoredups', '-l', '--resolve', 
            '--format=${ip}\t${Name}\t${mac}\t${vendor}'
        ]).decode('utf-8')
        for line in arp_scan_output.splitlines():
            parts = line.split('\t')
            if len(parts) == 4:
                ip, host, mac, vendor = parts
                http_status = check_http(ip, 80)
                print(host+" "+ip)
                net_data['devices'].append({'ip': ip, 'host': host, 'mac': mac, 'vendor': vendor, 'http': http_status})
    except subprocess.CalledProcessError:
        # Fehler beim arp-scan Aufruf - alternativen Aufruf hier einfügen
        try:
            arp_scan_output = subprocess.check_output(['arp-scan', '--interface', interface, '--plain', '--ignoredups', '-l']).decode('utf-8')
            for line in arp_scan_output.splitlines():
                parts = line.split('\t')
                if len(parts) == 3:
                    ip, mac, vendor = parts
                    http_status = check_http(ip, 80)
                    net_data['devices'].append({'ip': ip, 'host': ip, 'mac': mac, 'vendor': vendor, 'http': http_status})
        except subprocess.CalledProcessError as e:
            print(f"Ein allgemeiner Fehler ist aufgetreten: {e}")
    except:
        print("Ein allgemeiner Fehler ist aufgetreten: {e}")
    
    net_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check_http(ip, port):
    url = f"http://{ip}:{port}"
    try:
        # Check if the port is available
        sock = socket.create_connection((ip, port), timeout=2)
        sock.close()
        # Check if the server responds to a HTTP request
        requests.head(url, timeout=10)
        return True
    except requests.RequestException:
        return False
    except:
        return False

class ProgramInfo:
    def __init__(self, name, port, http):
        self.name = name
        self.port = port
        self.http = http

programs = []

def get_yaml_programs():
    global programs
    yaml = YAML(typ='safe', pure=True)
    with open('../../docker-compose.yml', 'r') as yaml_file:
        data = yaml.load(yaml_file)
    programs = []
    for service_name, service_config in data.get('services', {}).items():
        ports = service_config.get('ports', [])
        added = False
        for port in ports:
            if isinstance(port, str):
                external_port = port.split(":")[0]
                http = check_http("localhost", external_port)
                programm_info = ProgramInfo(service_name, external_port, http)
                programs.append(programm_info)
                added = True
        if not added:
            programm_info = ProgramInfo(service_name, False, False)
            programs.append(programm_info)
            
    return programs

memory_usage = ""
disk_usage = ""

async def resource_check():
    global memory_usage, disk_usage
    while True:
        current_disk_usage = get_disk_usage("/")
        current_memory_usage = get_memory_usage()
        disk_usage = f"DISK: [ {current_disk_usage['used']} / {current_disk_usage['total']} ] - {current_disk_usage['used_percentage']}"
        memory_usage = f"RAM: [ {current_memory_usage['used']} / {current_memory_usage['total']} ] - {current_memory_usage['used_percentage']}"
        await asyncio.sleep(60)

async def net_check():
    global programs, net_data, periodic_scan
    programs = get_yaml_programs()
    ip_scan()
    while periodic_scan:
        await asyncio.sleep(120)
        programs = get_yaml_programs()
        ip_scan()

def bytes_to_readable(bytes, suffix="B"):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(bytes) < 1024.0:
            return f"{bytes:3.1f} {unit}{suffix}"
        bytes /= 1024.0
    return f"{bytes:.1f} Y{suffix}"

def get_memory_usage():
    memory_info = psutil.virtual_memory()
    used_percentage = memory_info.percent
    return {
        "total": bytes_to_readable(memory_info.total),
        "available": bytes_to_readable(memory_info.available),
        "used": bytes_to_readable(memory_info.used),
        "free": bytes_to_readable(memory_info.free),
        "used_percentage": f"{used_percentage:.1f}%"
    }

def get_disk_usage(path="/"):
    total, used, free = shutil.disk_usage(path)
    used_percentage = (used / total) * 100
    return {
        "total": bytes_to_readable(total),
        "used": bytes_to_readable(used),
        "free": bytes_to_readable(free),
        "used_percentage": f"{used_percentage:.1f}%" 
    }

# Dashboard Items
def create_items():
    global programs
    with open('web/static/programs.json', 'r') as json_file:
        program_list = json.load(json_file)['programs']

    program_names = [p.name for p in programs] 
    program_ports = [p.port for p in programs]
    program_filterlist = ["nodered","homeassistant","esphome","vscode","docs","immich"] 
    items = []
    for program in program_list:
        program_name = program['img'].split('/')[-1].split('.')[0] # "img/name.png" zu "name."
        if (program_name in program_names and program['port'] in program_ports) or (program['custom_url'] != "" and program['active']) or (program_name in program_filterlist and program['active']):
            link = f"{request.url_root.rstrip('/')}:{program['port']}"
            link = program['custom_url'] if program['custom_url'] else link
            if program['custom_url'] == "https":
                link = f"https://{request.host}:{program['port']}"

            item_html = f'''
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
            '''

            items.append(item_html)

    return ''.join(items)


async def start_server():
    global port
    await asyncio.to_thread(serve, app, host='0.0.0.0', port=port)

async def main():
    task1 = asyncio.create_task(resource_check())
    task2 = asyncio.create_task(start_server())
    task3 = asyncio.create_task(net_check())
    await task1
    await task2
    await task3

if __name__ == '__main__':
    asyncio.run(main())
