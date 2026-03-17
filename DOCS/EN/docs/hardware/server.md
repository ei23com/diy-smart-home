# Server / Mini-PC Hardware

Choosing the right hardware is crucial for your Smart Home Server. Here you'll learn about the available options and which one is best suited for you.

!!!tip "Mini-PCs / ThinClients Recommended"
    Although the Raspberry Pi has very low power consumption, the **performance per watt** of used Mini-PCs and ThinClients is often significantly better. For around €50-100, you can get used x86 systems that offer more performance and better Docker support.

## Hardware Comparison

| Hardware | Price | Power Consumption | Performance | Docker Support | Recommendation |
|----------|-------|-------------------|-------------|----------------|----------------|
| **Raspberry Pi 4** | ~€50 | 3-5W | Good | Limited (ARM) | ✅ For beginners |
| **Raspberry Pi 5** | ~€80 | 5-8W | Very Good | Limited (ARM) | ✅ For light use |
| **Intel N100 Mini-PC** | ~€150 | 6-10W | Very Good | ✅ Perfect | ✅ **Recommended** |
| **HP/Lenovo/Dell ThinClient** | €50-100 | 10-25W | Excellent | ✅ Perfect | ✅ **Best Value** |
| **Intel NUC (i3/i5)** | €200-400 | 15-35W | Superior | ✅ Perfect | For high requirements |
| **Old PC** | ~€0 | 30-80W | Variable | ✅ Perfect | For testing |

## Recommended Hardware

### Beginners: Raspberry Pi 4/5

**Advantages:**
- Very low power consumption (3-8W)
- Compact form factor
- Low purchase cost

**Disadvantages:**
- Limited Docker support (not all images available for ARM)
- Limited RAM (max. 8GB)
- SD card as primary storage (slow, less reliable)

**Ideal for:**
- Home Assistant + NodeRED only
- Up to 5-8 Docker containers
- Light use without media server

!!!tip "Recommendation"
    At least **4GB RAM**, preferably **8GB**. Use an SSD instead of an SD card (via USB).

---

### Recommended: Mini-PCs / ThinClients

!!!success "Best Recommendation"
    Used ThinClients offer the **best price-performance ratio** for Smart Home servers.

**Examples:**

| Model | Price (used) | CPU | RAM | Advantages |
|-------|-------------|-----|-----|------------|
| **HP T620** | ~€40 | AMD GX-415GA | 4-8GB | Very affordable, quiet |
| **HP T630** | ~€60 | AMD GX-420GI | 4-8GB | More performance |
| **Lenovo ThinkCentre M700** | ~€80 | i3-6100T | 8GB | Intel QuickSync |
| **Dell Wyse 5070** | ~€50 | J5005 | 4-8GB | Low consumption |
| **Intel N100 Mini-PC** | ~€150 | N100 | 8-16GB | Current, efficient |
| **HP ProDesk 400 G6** | ~€150 | i3-10100T | 8-16GB | Very powerful |

**Advantages of Mini-PCs:**
- ✅ x86 architecture - All Docker images work
- ✅ More performance per watt
- ✅ SSD support (SATA/NVMe)
- ✅ More expandable RAM
- ✅ Intel QuickSync for hardware transcoding (Jellyfin, Plex)
- ✅ More durable than SD cards

**Ideal for:**
- All Docker containers from the ei23 script
- Media servers (Jellyfin, Plex)
- Nextcloud with many users
- AI/LLM (with dedicated GPU)
- Frigate with multiple cameras

---

### Advanced: Own PC / Server

For very high requirements:

- **Proxmox** as hypervisor
- **Multiple VMs** for different services
- **Dedicated GPU** for AI/LLM
- **RAID storage** for data security
- Power consumption: 30-100W

## Power Consumption Comparison

| System | Idle | Load | Cost/Year* |
|--------|------|------|------------|
| Raspberry Pi 4 | 3W | 6W | ~€10 |
| Intel N100 Mini-PC | 6W | 15W | ~€20 |
| HP ThinClient i3 | 12W | 35W | ~€40 |
| Old Desktop PC | 40W | 120W | ~€140 |

*At €0.30/kWh, 24/7 operation

!!!note "Performance per Watt"
    While the Raspberry Pi consumes the least power, an Intel N100 offers **5-10x the performance** at double the power consumption. For Docker workloads, a Mini-PC is often the more efficient choice.

## Storage Recommendations

| Type | Price | Advantages | Disadvantages |
|------|-------|------------|---------------|
| **SD Card** | ~€15 | Affordable | Slow, less durable |
| **USB SSD** | ~€30 | Faster, more durable | USB bandwidth limitation |
| **SATA SSD** | ~€40 | Fast, reliable | Only on Mini-PCs |
| **NVMe SSD** | ~€50 | Fastest | Only on newer systems |

!!!warning "SD Cards"
    SD cards have a limited lifespan with frequent write operations. Use **Log2RAM** (available in the ei23 script) or better yet, an SSD.

## My Recommendations

| Use Case | Recommendation | Budget |
|----------|----------------|--------|
| **Home Assistant + NodeRED only** | Raspberry Pi 4 4GB | ~€70 |
| **Home Assistant + 5-10 containers** | HP T630 or Dell Wyse 5070 | ~€60-80 |
| **Everything + Media Server** | Intel N100 Mini-PC | ~€150 |
| **AI/LLM + many containers** | i5/i7 Mini-PC with GPU | ~€300+ |

## Where to Buy?

- **eBay Kleinanzeigen / eBay** - Used ThinClients
- **refurbed.de** - Refurbished Mini-PCs with warranty
- **Amazon** - New Intel N100 systems
- **Raspberry Pi Shops** - For RPis and accessories
