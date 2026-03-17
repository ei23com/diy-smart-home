# Node-RED

[Node-RED](https://nodered.org/) is a visual programming environment for wiring together hardware devices, APIs, and online services. It's the Swiss Army knife of automation.

## Installation

Node-RED is installed **natively** with the ei23 script (not as a Docker container). This offers advantages for GPIO usage and performance.

!!!note "Pre-installed"
    Node-RED is automatically installed with the ei23 script. You don't need to do anything else!

## Access

Node-RED is accessible at `http://[IP]:1880`

## Nodes

Nodes are the central components of Node-RED. They are dragged onto the workspace and connected together.

### Pre-installed Nodes

The ei23 script automatically installs the following nodes:

| Node | Description |
|------|-------------|
| **node-red-dashboard** | Web dashboard for UI elements |
| **node-red-contrib-home-assistant-websocket** | Home Assistant integration |
| **node-red-contrib-boolean-logic** | Logical operations |
| **node-red-contrib-config** | Configuration nodes |
| **node-red-contrib-counter** | Counter |
| **node-red-contrib-dwd-local-weather** | German Weather Service |
| **node-red-contrib-eztimer** | Time control |
| **node-red-contrib-influxdb** | InfluxDB integration |
| **node-red-contrib-looptimer2** | Loop timer |
| **node-red-contrib-sunpos** | Sun position |
| **node-red-contrib-telegrambot** | Telegram Bot |
| **node-red-contrib-time-range-switch** | Time range switch |
| **node-red-contrib-timerswitch** | Timer switch |
| **node-red-node-email** | Send emails |
| **node-red-node-ping** | Ping test |
| **node-red-node-serialport** | Serial interface |
| **node-red-node-smooth** | Smooth data |
| **node-red-contrib-postgresql** | PostgreSQL integration |

### Installing Additional Nodes

Additional nodes can be installed via the Palette (Hamburger menu → Manage Palette).

## Setup

### MQTT Node Configuration

1. Drag an **mqtt in** node onto the workspace
2. Double-click the node
3. Click the pencil ✏️ next to **Server**
4. Configure:
    - **Server**: `localhost` or IP of the MQTT broker
    - **Port**: `1883`
    - **Username/Password**: If configured
5. Click **Connect** → **Done**
6. Enter a **Topic** (e.g. `home/temperature/#`)

### Home Assistant Node Configuration

1. Drag a **server** Config node onto the workspace
2. Or create it via an HA node
3. Configure:
    - **Base URL**: `http://localhost:8123` (or IP)
    - **Access Token**: Create in HA under Profile → Long-lived tokens

### Inject Node

The **Inject** node triggers flows manually or on schedule:

- **Once**: Click the button
- **Scheduled**: Configure repeat interval
- **Timed**: At specific times

### Debug Node

The **Debug** node displays data in the debug panel:

- The sidebar "Debug" tab shows all outputs
- Useful for testing and finding errors

## Flows

### Pages (Tabs)

Flows can be organized in pages:

1. Click **+** next to the tab name
2. Name the page (e.g. "Heating", "Lights", "Sensors")
3. Organize your nodes thematically

### Subflows

Subflows are reusable groups of nodes:

1. Select nodes
2. Right-click → **Selection to Subflow**
3. The subflow appears as a single node in the panel

!!!tip "Subflows are powerful"
    Subflows can have parameters and are displayed as a single node. Ideal for repeating logic.

### Flow Library

Flows can be saved in the library:

1. Select nodes
2. Right-click → **Save selection to library**
3. Reuse via library

## Variables and Context

Node-RED offers three context levels:

| Level | Scope | Example |
|-------|-------|---------|
| **Flow** | Within a tab | `flow.get("counter")` |
| **Global** | Everywhere | `global.get("lastUpdate")` |
| **Node** | Only this node | `node.get("state")` |

### Example: Counter

```javascript
// Increment counter
let count = flow.get("counter") || 0;
count++;
flow.set("counter", count);
msg.payload = count;
return msg;
```

## Dashboard

The pre-installed **node-red-dashboard** provides a web interface for UI elements:

### Access

The dashboard is accessible at `http://[IP]:1880/ui`

### Available UI Elements

| Element | Description |
|---------|-------------|
| **ui_button** | Button |
| **ui_slider** | Slider |
| **ui_switch** | Switch |
| **ui_text** | Text display |
| **ui_gauge** | Gauge |
| **ui_chart** | Chart |
| **ui_dropdown** | Dropdown menu |
| **ui_text_input** | Text input |

### Configuration

1. Double-click a UI element
2. Select the **Group** and **Tab**
3. Configure size and position

## Password Protection

### Via the ei23 Script

```bash
ei23
# Select "Set new passwords"
```

### Manually

Edit `/home/[user]/.node-red/settings.js`:

```javascript
adminAuth: {
    type: "credentials",
    users: [{
        username: "admin",
        password: "$2a$08$...", // bcrypt hash
        permissions: "*"
    }]
}
```

!!!tip "Generate hash"
    ```bash
    cd ~/.node-red/
    node -e "console.log(require('bcryptjs').hashSync('YOUR_PASSWORD', 8));"
    ```

## Backup

Node-RED data is backed up with the ei23 backup. Manually:

```bash
# Backup
sudo tar -czf ~/nodered_backup.tar.gz ~/.node-red/

# Restore
sudo tar -xzf ~/nodered_backup.tar.gz -C ~/
sudo service nodered restart
```

## Updates

Node-RED is updated with the ei23 update:

```bash
ei23 update
```

Or manually:

```bash
# Update Node-RED and nodes
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered) --confirm-install --update-nodes
```

## Home Assistant Integration

The pre-installed **hass-node-red** addon enables integration with Home Assistant:

1. In Node-RED: Configure Home Assistant server
2. In Home Assistant: Create long-lived token
3. URL: `http://localhost:8123` (if HA is in Docker)

### Example: Light on Motion

```
[HA: Motion Sensor] → [Switch] → [HA: Light on]
                        ↓
                   [Delay 5min] → [HA: Light off]
```

## Notes

- Node-RED runs on port **1880**
- Configuration: `/home/[user]/.node-red/settings.js`
- Flows: `/home/[user]/.node-red/flows.json`
- Service: `sudo systemctl status nodered`
- Logs: `journalctl -u nodered -f`

## Further Information

- [Official Documentation](https://nodered.org/docs/)
- [Flow Library](https://flows.nodered.org/)
- [Node-RED Forum](https://discourse.nodered.org/)
- [YouTube Tutorials](https://www.youtube.com/c/NodeRED)
