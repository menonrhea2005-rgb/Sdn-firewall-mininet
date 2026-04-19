# Sdn-firewall-mininet


# SDN-Based Firewall using Mininet and POX Controller

## Problem Statement
Develop a controller-based firewall to block or allow traffic between hosts using 
Software Defined Networking (SDN) principles with OpenFlow.

## Overview
This project implements an SDN firewall using:
- **Mininet** - Network emulator
- **POX Controller** - OpenFlow controller
- **OpenFlow** - Flow rule protocol

## Topology
- 1 Switch (s1)
- 4 Hosts (h1, h2, h3, h4)
- 1 Remote Controller (POX)

## Firewall Rules
| Rule | Source | Destination | Port | Action |
|------|--------|-------------|------|--------|
| 1 | h1 (10.0.0.1) | h2 (10.0.0.2) | Any | ALLOW |
| 2 | h2 (10.0.0.2) | h1 (10.0.0.1) | Any | ALLOW |
| 3 | h3 (10.0.0.3) | Any | Any | BLOCK |
| 4 | Any | h3 (10.0.0.3) | Any | BLOCK |
| 5 | Any | h4 (10.0.0.4) | 80 | BLOCK |

## Setup and Execution

### Prerequisites
- Ubuntu 20.04/22.04
- Mininet
- POX Controller
- Python 3

### Installation
```bash
# Install Mininet
sudo apt install mininet -y

# Install POX
git clone https://github.com/noxrepo/pox.git

# Clone this repo
git clone https://github.com/menonrhea2005-rgb/Sdn-firewall-mininet.git
```

### Running the Project

**Terminal 1 - Start POX Firewall Controller:**
```bash
cp firewall.py ~/pox/pox/forwarding/
cd ~/pox
python3 pox.py forwarding.firewall
```

**Terminal 2 - Start Mininet Topology:**
```bash
sudo python3 topology.py
```

### Testing

**Test 1 - Allowed traffic (h1 to h2):**

#screenshots 

<img width="1317" height="981" alt="WhatsApp Image 2026-04-19 at 12 06 12" src="https://github.com/user-attachments/assets/a3077505-282d-4f85-a37a-83674cdc4f42" />



<img width="1317" height="981" alt="WhatsApp Image 2026-04-19 at 12 06 12" src="https://github.com/user-attachments/assets/a31208a7-1246-4a5b-86bf-ee988fb6807e" />



<img width="1317" height="981" alt="WhatsApp Image 2026-04-19 at 12 06 12" src="https://github.com/user-attachments/assets/2d48202b-3cf2-41e9-970a-4a712733a920" />





