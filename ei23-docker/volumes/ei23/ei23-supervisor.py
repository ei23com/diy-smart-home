from datetime import datetime
from flask import Flask, render_template, redirect, url_for, send_from_directory, request, jsonify
from ruamel.yaml import YAML
from waitress import serve
import json, socket, subprocess, os


app = Flask(__name__, template_folder='web', static_folder='web/static')


@app.route('/')
def index():
    header = render_template('dashboard-head.html')
    navbar = render_template('navbar.html').replace("dashboard-placeholder\"", "active\" aria-current=\"page\"")
    items = create_items()
    bottom_logo = render_template('bottom-logo.html')
    return render_template('index.html', header=header, navbar=navbar, items=items, bottom_logo=bottom_logo)

@app.route('/localnet')
def localnet():
    header = render_template('dashboard-head.html')
    navbar = render_template('navbar.html').replace("localnet-placeholder\"", "active\" aria-current=\"page\"")
    bottom_logo = render_template('bottom-logo.html')
    json_path = 'web/static/ipscan.json'
    scan_result = ""
    if os.path.exists(json_path):
        with open(json_path, 'r') as file:
            data = json.load(file)
        # Daten für die Tabelle aufbauen und nach dem Host (ignorieren der Groß- und Kleinschreibung) sortieren
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

mkdocs_directory = 'docs/site/'
@app.route('/docs/')
@app.route('/docs/<path:filename>')
def serve_docs(filename='index.html'):
    # build docs wenn nicht vorhanden
    if not os.path.exists(mkdocs_directory):
        # pfad fuer root command holen
        docs_path = subprocess.check_output(['pwd']).decode('utf-8')
        # build docs
        command = 'bash -c \'cd '+docs_path+'/; source .venv/bin/activate; cd docs/; mkdocs build; deactivate\''
        subprocess.run(command, shell=True)

    full_path = os.path.join(mkdocs_directory, filename)
    # Überprüfe, ob der angegebene Dateiname ein Verzeichnis ist
    if os.path.isdir(full_path):
        # Wenn es sich um ein Verzeichnis handelt, füge 'index.html' hinzu
        filename = os.path.join(filename, 'index.html')
    return send_from_directory(mkdocs_directory, filename)

# Routen für die Anzeige der Tabelle und Aktualisierung der JSON-Daten
@app.route('/server')
def server():
    header = render_template('dashboard-head.html')
    navbar = render_template('navbar.html').replace("server-placeholder\"", "active\" aria-current=\"page\"")
    bottom_logo = render_template('bottom-logo.html')
    json_path = 'web/static/programs.json'
    table = ""
    external_ports = get_external_ports()
    ignore = ["1880", "/", "8123"]
    if os.path.exists(json_path):
        with open(json_path, 'r') as file:
            data = json.load(file)
        for program in data['programs']:
            port = program['port']
            # ignoriere ports mit 1880 oder /
            if not any(substr in port for substr in ignore) and program['custom_url'] == "":
                no_entry = not program['port'] in external_ports and program['active']
                color = "<tr style=\"background-color: #ff000050\">" if no_entry else "<tr>"
                table += f"{color}<td>{'&#x2705;' if program['port'] in external_ports else '&#x274C;'}</td><td>{'&#x2705;' if program['active'] else '&#x274C;'}</td><td>{program['port']}</td><td>{program['name']}</td></tr>\n"
            else:
                table += f"<tr><td>{'&#x2705;' if program['port'] in external_ports else '&#x274C;'}</td><td>{'&#x2705;' if program['active'] else '&#x274C;'}</td><td>{program['port']}</td><td>{program['name']}</td></tr>\n"

    return render_template('server.html', header=header, navbar=navbar, table=table, bottom_logo=bottom_logo)

@app.route('/addprograms')
def add_programs():
    merge_json_files('web/static/programs.json', 'web/static/programs_templates.json')
    return redirect(url_for('server'))

def merge_json_files(target_filename, template_filename):
    # Öffne die JSON-Dateien
    with open(target_filename, 'r') as target_file:
        target_data = json.load(target_file)

    with open(template_filename, 'r') as template_file:
        template_data = json.load(template_file)

    # Iteriere durch die Einträge der Vorlagendatei
    for template_entry in template_data['programs']:
        template_port = template_entry['port']

        # Überprüfe, ob der Eintrag bereits in der Zieldatei vorhanden ist
        existing_entry = next((entry for entry in target_data['programs'] if entry['port'] == template_port), None)

        # Füge den Eintrag hinzu, falls er nicht vorhanden ist
        if existing_entry is None:
            target_data['programs'].append(template_entry)

    # Schreibe die aktualisierten Daten zurück in die Zieldatei
    with open(target_filename, 'w') as updated_file:
        json.dump(target_data, updated_file, indent=None)

    # Füge manuell Zeilenumbrüche nach "},{" hinzu
    with open(target_filename, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace('}, {', '},\n{').replace('[{', '[\n{').replace(']}', '\n]}'))




def ip_scan():
    target_data = {'devices': []}
    try:
        # arp-scan --plain --ignoredups -l --format='${ip}\t${Name}\t${mac}\t${vendor}'
        arp_scan_output = subprocess.check_output(['arp-scan', '--plain', '--ignoredups', '-l', '--resolve', '--format=${ip}\t${Name}\t${mac}\t${vendor}']).decode('utf-8')
        for line in arp_scan_output.splitlines():
            parts = line.split('\t')
            if len(parts) == 4:
                ip, host, mac, vendor = parts
                http_status = check_http(ip)
                print(host+" "+ip)
                target_data['devices'].append({'ip': ip, 'host': host, 'mac': mac, 'vendor': vendor, 'http': http_status})
    except subprocess.CalledProcessError:
        # Fehler beim arp-scan Aufruf - alternativen Aufruf hier einfügen
        # Zum Beispiel: arp_scan_output = subprocess.check_output(['alternative_command', ...]).decode('utf-8')
        arp_scan_output = subprocess.check_output(['arp-scan', '--plain', '--ignoredups', '-l']).decode('utf-8')
        for line in arp_scan_output.splitlines():
            parts = line.split('\t')
            if len(parts) == 3:
                ip, mac, vendor = parts
                http_status = check_http(ip)
                target_data['devices'].append({'ip': ip, 'host': ip, 'mac': mac, 'vendor': vendor, 'http': http_status})



    # Füge einen aktuellen Zeitstempel hinzu
    target_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("web/static/ipscan.json", 'w') as updated_file:
        json.dump(target_data, updated_file, indent=2)

def check_http(ip):
    try:
        sock = socket.create_connection((ip, 80), timeout=2)
        sock.close()
        return True
    # except (socket.timeout, ConnectionRefusedError):
    except:
        return False


def get_external_ports():
    yaml = YAML(typ='safe', pure=True)
    with open('../../docker-compose.yml', 'r') as yaml_file:
        data = yaml.load(yaml_file)

    external_ports = []

    for service_name, service_config in data.get('services', {}).items():
        ports = service_config.get('ports', [])
        for port in ports:
            if isinstance(port, str):
                external_port = port.split(":")[0]
                external_ports.append(external_port)

    return external_ports

    
def create_items():
    with open('web/static/programs.json', 'r') as json_file:
        programs = json.load(json_file)['programs']

    items = []
    for program in programs:
        if program['active']:
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


if __name__ == '__main__':
    # Starte den Webserver mit Waitress
    serve(app, host='0.0.0.0', port=80)
