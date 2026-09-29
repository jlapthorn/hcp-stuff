#!/usr/bin/env python3
"""Generate Excalidraw architecture diagram for OpenShift HCP bare metal deployment."""

import json
import random

random.seed(42)

elements = []
_id_counter = [0]

def make_id():
    _id_counter[0] += 1
    return f"elem_{_id_counter[0]}"

def rect(x, y, w, h, bg="#ffffff", stroke="#1e1e1e", stroke_w=2, opacity=100, group=None, roundness=3):
    eid = make_id()
    el = {
        "type": "rectangle",
        "version": 1,
        "versionNonce": random.randint(1, 2**31),
        "isDeleted": False,
        "id": eid,
        "fillStyle": "solid",
        "strokeWidth": stroke_w,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": opacity,
        "angle": 0,
        "x": x,
        "y": y,
        "strokeColor": stroke,
        "backgroundColor": bg,
        "width": w,
        "height": h,
        "seed": random.randint(1, 2**31),
        "groupIds": [group] if group else [],
        "frameId": None,
        "roundness": {"type": roundness},
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
    }
    elements.append(el)
    return eid

def text(x, y, txt, size=16, color="#1e1e1e", align="left", bold=False, group=None, family=1):
    eid = make_id()
    lines = txt.split("\n")
    h = len(lines) * size * 1.25
    max_w = max(len(line) for line in lines) * size * 0.6
    el = {
        "type": "text",
        "version": 1,
        "versionNonce": random.randint(1, 2**31),
        "isDeleted": False,
        "id": eid,
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "x": x,
        "y": y,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "width": max_w,
        "height": h,
        "seed": random.randint(1, 2**31),
        "groupIds": [group] if group else [],
        "frameId": None,
        "roundness": None,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "fontSize": size,
        "fontFamily": family,
        "text": txt,
        "textAlign": align,
        "verticalAlign": "top",
        "containerId": None,
        "originalText": txt,
        "autoResize": True,
        "lineHeight": 1.25,
    }
    elements.append(el)
    return eid

def arrow(x1, y1, x2, y2, color="#868e96", width=2, style="solid"):
    eid = make_id()
    el = {
        "type": "arrow",
        "version": 1,
        "versionNonce": random.randint(1, 2**31),
        "isDeleted": False,
        "id": eid,
        "fillStyle": "solid",
        "strokeWidth": width,
        "strokeStyle": style,
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "x": x1,
        "y": y1,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "width": x2 - x1,
        "height": y2 - y1,
        "seed": random.randint(1, 2**31),
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 2},
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "startBinding": None,
        "endBinding": None,
        "lastCommittedPoint": None,
        "startArrowhead": None,
        "endArrowhead": "arrow",
        "points": [[0, 0], [x2 - x1, y2 - y1]],
    }
    elements.append(el)
    return eid

def line(x1, y1, x2, y2, color="#868e96", width=1, style="dashed"):
    eid = make_id()
    el = {
        "type": "line",
        "version": 1,
        "versionNonce": random.randint(1, 2**31),
        "isDeleted": False,
        "id": eid,
        "fillStyle": "solid",
        "strokeWidth": width,
        "strokeStyle": style,
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "x": x1,
        "y": y1,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "width": x2 - x1,
        "height": y2 - y1,
        "seed": random.randint(1, 2**31),
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 2},
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
        "startBinding": None,
        "endBinding": None,
        "lastCommittedPoint": None,
        "startArrowhead": None,
        "endArrowhead": None,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
    }
    elements.append(el)
    return eid


# ═══════════════════════════════════════════════════════════════
# LAYOUT CONSTANTS
# ═══════════════════════════════════════════════════════════════

CANVAS_W = 3400
LEFT = 40
RIGHT = CANVAS_W - 40

# Cluster colors
COLORS = {
    "x_prod":  {"bg": "#ffc9c9", "stroke": "#c92a2a", "dark": "#e03131"},
    "x_np1":   {"bg": "#ffd8a8", "stroke": "#e8590c", "dark": "#e8590c"},
    "y_prod":  {"bg": "#b2f2bb", "stroke": "#2b8a3e", "dark": "#2f9e44"},
    "y_np1":   {"bg": "#d0bfff", "stroke": "#6741d9", "dark": "#7048e8"},
    "max_np1": {"bg": "#96f2d7", "stroke": "#087f5b", "dark": "#0ca678"},
}

MGMT_BG = "#a5d8ff"
MGMT_STROKE = "#1971c2"
PHYS_BG = "#e9ecef"
PHYS_STROKE = "#495057"
SUMMARY_BG = "#fff3bf"
SUMMARY_STROKE = "#e67700"

# ═══════════════════════════════════════════════════════════════
# TITLE
# ═══════════════════════════════════════════════════════════════

text(LEFT, 20, "OpenShift HCP Bare Metal Architecture", size=32, color="#1e1e1e")
text(LEFT, 62, "5 Hosted Clusters on a Single Combined Pool of 44 Dell Bare Metal Nodes with OpenShift Virtualization (KubeVirt)", size=16, color="#495057")

# ═══════════════════════════════════════════════════════════════
# LAYER 1: HOSTED CLUSTERS (TOP)
# ═══════════════════════════════════════════════════════════════

HC_TOP = 110
HC_H = 520

# Outer container
rect(LEFT, HC_TOP, RIGHT - LEFT, HC_H, bg="#f8f9fa", stroke="#868e96", stroke_w=2)
text(LEFT + 20, HC_TOP + 10, "HOSTED CLUSTERS (KubeVirt Virtual Machines)", size=18, color="#495057")

clusters = [
    {
        "name": "X-PROD", "key": "x_prod", "vlan": "VLAN 100",
        "workers": (64, 32, 66), "infra": (94, 32, 6), "master": (188, 32, 3),
    },
    {
        "name": "X-NP1", "key": "x_np1", "vlan": "VLAN 200",
        "workers": (32, 16, 107), "infra": (94, 32, 6), "master": (255, 16, 3),
    },
    {
        "name": "Y-PROD", "key": "y_prod", "vlan": "VLAN 300",
        "workers": (32, 16, 25), "infra": (94, 32, 6), "master": (94, 16, 3),
    },
    {
        "name": "Y-NP1", "key": "y_np1", "vlan": "VLAN 400",
        "workers": (32, 16, 33), "infra": (94, 32, 6), "master": (94, 16, 3),
    },
    {
        "name": "Max-NP1", "key": "max_np1", "vlan": "VLAN 500",
        "workers": (32, 8, 3), "infra": None, "master": (32, 8, 3),
    },
]

cluster_w = 620
cluster_gap = 20
cluster_start_x = LEFT + 30
cluster_y = HC_TOP + 45

for i, c in enumerate(clusters):
    cx = cluster_start_x + i * (cluster_w + cluster_gap)
    col = COLORS[c["key"]]

    # Cluster box
    rect(cx, cluster_y, cluster_w, HC_H - 60, bg=col["bg"], stroke=col["stroke"], stroke_w=2, opacity=60)

    # Cluster name + VLAN
    text(cx + 15, cluster_y + 10, c["name"], size=22, color=col["dark"])
    text(cx + 15, cluster_y + 38, c["vlan"], size=14, color=col["stroke"])

    # Calculate totals
    w_ram, w_cpu, w_cnt = c["workers"]
    w_total_ram = w_ram * w_cnt
    w_total_cpu = w_cpu * w_cnt

    if c["infra"]:
        i_ram, i_cpu, i_cnt = c["infra"]
        i_total_ram = i_ram * i_cnt
        i_total_cpu = i_cpu * i_cnt
    else:
        i_cnt = 0
        i_total_ram = 0
        i_total_cpu = 0

    m_ram, m_cpu, m_cnt = c["master"]
    m_total_ram = m_ram * m_cnt
    m_total_cpu = m_cpu * m_cnt

    total_vms = w_cnt + i_cnt + m_cnt
    total_ram = w_total_ram + i_total_ram + m_total_ram
    total_cpu = w_total_cpu + i_total_cpu + m_total_cpu

    # Worker details
    inner_y = cluster_y + 65
    rect(cx + 10, inner_y, cluster_w - 20, 90, bg="#ffffff", stroke=col["stroke"], stroke_w=1, opacity=80)
    text(cx + 20, inner_y + 8, "Workers", size=16, color=col["dark"])
    text(cx + 20, inner_y + 30, f"{w_cnt}x VMs  |  {w_ram}GB RAM  |  {w_cpu} vCPU each", size=13, color="#495057")
    text(cx + 20, inner_y + 52, f"Total: {w_total_ram:,}GB RAM  |  {w_total_cpu:,} vCPU", size=13, color="#1e1e1e")

    # Infra details
    inner_y += 100
    if c["infra"]:
        rect(cx + 10, inner_y, cluster_w - 20, 90, bg="#ffffff", stroke=col["stroke"], stroke_w=1, opacity=80)
        text(cx + 20, inner_y + 8, "Infrastructure", size=16, color=col["dark"])
        text(cx + 20, inner_y + 30, f"{i_cnt}x VMs  |  {i_ram}GB RAM  |  {i_cpu} vCPU each", size=13, color="#495057")
        text(cx + 20, inner_y + 52, f"Total: {i_total_ram:,}GB RAM  |  {i_total_cpu:,} vCPU", size=13, color="#1e1e1e")
    else:
        rect(cx + 10, inner_y, cluster_w - 20, 90, bg="#ffffff", stroke=col["stroke"], stroke_w=1, opacity=40)
        text(cx + 20, inner_y + 8, "Infrastructure", size=16, color="#adb5bd")
        text(cx + 20, inner_y + 35, "N/A", size=13, color="#adb5bd")

    # Master / Control Plane
    inner_y += 100
    rect(cx + 10, inner_y, cluster_w - 20, 90, bg="#ffffff", stroke=col["stroke"], stroke_w=1, opacity=80)
    text(cx + 20, inner_y + 8, "Control Plane (HCP Pods)", size=16, color=col["dark"])
    text(cx + 20, inner_y + 30, f"{m_cnt}x Pods  |  {m_ram}GB RAM  |  {m_cpu} vCPU each", size=13, color="#495057")
    text(cx + 20, inner_y + 52, f"Total: {m_total_ram:,}GB RAM  |  {m_total_cpu:,} vCPU", size=13, color="#1e1e1e")

    # ODF + totals
    inner_y += 100
    rect(cx + 10, inner_y, (cluster_w - 20) // 2 - 5, 55, bg="#e7f5ff", stroke=col["stroke"], stroke_w=1)
    text(cx + 20, inner_y + 8, "ODF Storage", size=14, color=MGMT_STROKE)
    text(cx + 20, inner_y + 28, "Runs on Infra nodes", size=11, color="#495057")

    rect(cx + 10 + (cluster_w - 20) // 2 + 5, inner_y, (cluster_w - 20) // 2 - 5, 55, bg="#fff9db", stroke=col["stroke"], stroke_w=1)
    text(cx + 10 + (cluster_w - 20) // 2 + 15, inner_y + 5, f"Cluster Total", size=14, color="#e67700")
    text(cx + 10 + (cluster_w - 20) // 2 + 15, inner_y + 22, f"{total_vms} VMs | {total_ram:,}GB", size=12, color="#495057")
    text(cx + 10 + (cluster_w - 20) // 2 + 15, inner_y + 38, f"{total_cpu:,} vCPU", size=12, color="#495057")


# ═══════════════════════════════════════════════════════════════
# LAYER 2: MANAGEMENT CLUSTER (MIDDLE)
# ═══════════════════════════════════════════════════════════════

MC_TOP = HC_TOP + HC_H + 30
MC_H = 280

rect(LEFT, MC_TOP, RIGHT - LEFT, MC_H, bg="#d0ebff", stroke=MGMT_STROKE, stroke_w=3)
text(LEFT + 20, MC_TOP + 10, "MANAGEMENT CLUSTER  (OpenShift 4.x Bare Metal)", size=20, color=MGMT_STROKE)

# Management components row
comp_y = MC_TOP + 50
comp_h = 80
comp_gap = 20

mgmt_components = [
    ("HCP Operator", "Manages hosted\ncontrol planes", "#e7f5ff"),
    ("OpenShift Virtualization", "KubeVirt - runs\nguest VMs", "#e7f5ff"),
    ("ODF Storage", "Mgmt cluster\npersistent storage", "#e7f5ff"),
    ("Monitoring & Logging", "Prometheus, Alertmanager\nLoki / EFK", "#e7f5ff"),
    ("Image Registry", "Internal container\nregistry", "#e7f5ff"),
    ("MetalLB / VLAN", "L2 network isolation\nper hosted cluster", "#e7f5ff"),
]

comp_w = (RIGHT - LEFT - 60 - (len(mgmt_components) - 1) * comp_gap) // len(mgmt_components)
for i, (name, desc, bg) in enumerate(mgmt_components):
    cx = LEFT + 30 + i * (comp_w + comp_gap)
    rect(cx, comp_y, comp_w, comp_h, bg=bg, stroke=MGMT_STROKE, stroke_w=1)
    text(cx + 10, comp_y + 8, name, size=14, color=MGMT_STROKE)
    text(cx + 10, comp_y + 30, desc, size=11, color="#495057")

# Hosted control plane pods row
cp_y = comp_y + comp_h + 20
text(LEFT + 30, cp_y, "Hosted Control Plane Pods:", size=14, color="#1e1e1e")
cp_y += 22

cp_w = 580
for i, c in enumerate(clusters):
    cx = LEFT + 30 + i * (cp_w + cluster_gap)
    col = COLORS[c["key"]]
    m_ram, m_cpu, m_cnt = c["master"]
    m_total_ram = m_ram * m_cnt
    m_total_cpu = m_cpu * m_cnt
    rect(cx, cp_y, cp_w, 50, bg=col["bg"], stroke=col["stroke"], stroke_w=1, opacity=60)
    text(cx + 10, cp_y + 5, f"{c['name']} CP", size=14, color=col["dark"])
    text(cx + 10, cp_y + 25, f"API + etcd + Controllers  |  {m_total_ram}GB RAM  |  {m_total_cpu} vCPU", size=12, color="#495057")

# Management overhead note
text(LEFT + 30, cp_y + 60, "Management overhead: ~656 GB RAM, ~200 vCPU (OS, kubelet, operators, monitoring, ODF)", size=13, color="#495057")

# ═══════════════════════════════════════════════════════════════
# LAYER 3: PHYSICAL INFRASTRUCTURE (BOTTOM)
# ═══════════════════════════════════════════════════════════════

PI_TOP = MC_TOP + MC_H + 30
PI_H = 250

rect(LEFT, PI_TOP, RIGHT - LEFT, PI_H, bg=PHYS_BG, stroke=PHYS_STROKE, stroke_w=3)
text(LEFT + 20, PI_TOP + 10, "PHYSICAL INFRASTRUCTURE  —  44 Dell Bare Metal Nodes (Single Combined Pool)", size=20, color=PHYS_STROKE)

# Single unified pool
srv_y = PI_TOP + 45

# Large summary box for the combined pool
pool_w = RIGHT - LEFT - 60
rect(LEFT + 30, srv_y, pool_w, 145, bg="#ffffff", stroke=PHYS_STROKE, stroke_w=2)

text(LEFT + 50, srv_y + 10, "Combined Management Cluster Node Pool  —  44 Nodes", size=18, color=PHYS_STROKE)

# Node specs breakdown (informational, not separate tiers)
text(LEFT + 50, srv_y + 42, "Node Specs (mixed hardware, single scheduling pool):", size=14, color="#1e1e1e")
text(LEFT + 70, srv_y + 64, "16 nodes  @  515 GB RAM / 48 cores    |    16 nodes  @  768 GB RAM / 96 cores    |    12 nodes  @  768 GB RAM / 192 cores", size=13, color="#495057")

# Totals line
line(LEFT + 50, srv_y + 90, LEFT + pool_w - 20, srv_y + 90, color=PHYS_STROKE, width=1, style="solid")
text(LEFT + 50, srv_y + 98, "TOTAL POOL:  44 Nodes  |  29,744 GB RAM  |  4,608 Physical Cores  (9,216 vCPU with Hyperthreading)", size=16, color="#1e1e1e")
text(LEFT + 50, srv_y + 120, "All nodes join a single OCP bare metal cluster — Kubernetes scheduler distributes workloads across the full pool", size=12, color="#868e96")

# ═══════════════════════════════════════════════════════════════
# CAPACITY SUMMARY BOX (RIGHT SIDE)
# ═══════════════════════════════════════════════════════════════

SUM_TOP = PI_TOP + PI_H + 30
SUM_H = 420

rect(LEFT, SUM_TOP, (RIGHT - LEFT) // 2 - 10, SUM_H, bg=SUMMARY_BG, stroke=SUMMARY_STROKE, stroke_w=2)
text(LEFT + 20, SUM_TOP + 10, "CAPACITY ANALYSIS", size=20, color=SUMMARY_STROKE)

summary_lines = [
    ("VM Workload Requirements", True, "#1e1e1e"),
    ("  X-PROD:     5,352 GB RAM  |  2,400 vCPU  |  75 VMs", False, "#495057"),
    ("  X-NP1:      4,753 GB RAM  |  1,952 vCPU  |  116 VMs", False, "#495057"),
    ("  Y-PROD:     1,646 GB RAM  |    640 vCPU  |  34 VMs", False, "#495057"),
    ("  Y-NP1:      1,902 GB RAM  |    768 vCPU  |  42 VMs", False, "#495057"),
    ("  Max-NP1:      192 GB RAM  |     48 vCPU  |   6 VMs", False, "#495057"),
    ("", False, "#495057"),
    ("  TOTAL:     13,845 GB RAM  |  5,808 vCPU  |  273 VMs", True, "#c92a2a"),
    ("  + Mgmt:      ~656 GB RAM  |   ~200 vCPU", False, "#495057"),
    ("  GRAND:    ~14,501 GB RAM  | ~6,008 vCPU", True, "#1e1e1e"),
    ("", False, "#495057"),
    ("Available Capacity", True, "#1e1e1e"),
    ("  Physical Cores:     4,608", False, "#495057"),
    ("  With Hyperthreading: 9,216", False, "#495057"),
    ("  Total RAM:         29,744 GB", False, "#495057"),
    ("", False, "#495057"),
    ("Utilization", True, "#1e1e1e"),
    ("  RAM:  48.8%  (15,243 GB headroom)", False, "#2f9e44"),
    ("  CPU:  65.2%  (with HT, 3,208 headroom)", False, "#2f9e44"),
    ("  CPU: 130.4%  (NO HT - WILL NOT FIT)", False, "#c92a2a"),
]

sy = SUM_TOP + 40
for line_text, is_bold, color in summary_lines:
    if line_text:
        text(LEFT + 30, sy, line_text, size=14 if is_bold else 13, color=color)
    sy += 18

# ═══════════════════════════════════════════════════════════════
# NETWORK / VLAN DIAGRAM (RIGHT SIDE)
# ═══════════════════════════════════════════════════════════════

NET_LEFT = LEFT + (RIGHT - LEFT) // 2 + 10
NET_W = (RIGHT - LEFT) // 2 - 10

rect(NET_LEFT, SUM_TOP, NET_W, SUM_H, bg="#f3f0ff", stroke="#6741d9", stroke_w=2)
text(NET_LEFT + 20, SUM_TOP + 10, "NETWORK ISOLATION (L2 VLANs)", size=20, color="#6741d9")

# VLAN diagram
vlan_data = [
    ("VLAN 100", "X-PROD", COLORS["x_prod"]),
    ("VLAN 200", "X-NP1", COLORS["x_np1"]),
    ("VLAN 300", "Y-PROD", COLORS["y_prod"]),
    ("VLAN 400", "Y-NP1", COLORS["y_np1"]),
    ("VLAN 500", "Max-NP1", COLORS["max_np1"]),
]

# Trunk line
trunk_x = NET_LEFT + 80
trunk_top = SUM_TOP + 55
trunk_bottom = SUM_TOP + SUM_H - 30
line(trunk_x, trunk_top, trunk_x, trunk_bottom, color="#6741d9", width=3, style="solid")
text(NET_LEFT + 20, trunk_top - 20, "802.1Q Trunk", size=13, color="#6741d9")

vlan_spacing = (trunk_bottom - trunk_top - 20) // (len(vlan_data))
for i, (vlan, cluster, col) in enumerate(vlan_data):
    vy = trunk_top + 20 + i * vlan_spacing

    # Branch line from trunk
    line(trunk_x, vy, trunk_x + 60, vy, color=col["stroke"], width=2, style="solid")

    # VLAN box
    rect(trunk_x + 65, vy - 20, 200, 45, bg=col["bg"], stroke=col["stroke"], stroke_w=1, opacity=80)
    text(trunk_x + 75, vy - 15, f"{vlan} → {cluster}", size=14, color=col["dark"])
    text(trunk_x + 75, vy + 5, "Isolated L2 broadcast domain", size=11, color="#495057")

# Additional notes
notes_y = SUM_TOP + 55
notes_x = trunk_x + 310
text(notes_x, notes_y, "Key Design Decisions:", size=16, color="#6741d9")
notes = [
    "• Each hosted cluster gets a",
    "  dedicated L2 VLAN for full",
    "  network isolation",
    "",
    "• Management cluster uses a",
    "  separate management VLAN",
    "",
    "• OVN-Kubernetes or Multus",
    "  maps VMs to correct VLANs",
    "",
    "• Control plane traffic stays",
    "  on management network",
    "",
    "• ODF traffic can use a",
    "  dedicated storage VLAN",
    "  (recommended for perf)",
    "",
    "• MetalLB provides LoadBalancer",
    "  services per VLAN",
]
ny = notes_y + 25
for n in notes:
    if n:
        text(notes_x, ny, n, size=12, color="#495057")
    ny += 17


# ═══════════════════════════════════════════════════════════════
# ARROWS between layers
# ═══════════════════════════════════════════════════════════════

# Arrows from hosted clusters to management cluster
for i in range(5):
    ax = LEFT + 30 + i * (cluster_w + cluster_gap) + cluster_w // 2
    arrow(ax, HC_TOP + HC_H, ax, MC_TOP, color="#868e96", width=1, style="dashed")

# Arrow from management to physical (single pool)
arrow(CANVAS_W // 2, MC_TOP + MC_H, CANVAS_W // 2, PI_TOP, color=PHYS_STROKE, width=3)


# ═══════════════════════════════════════════════════════════════
# BUILD OUTPUT
# ═══════════════════════════════════════════════════════════════

excalidraw = {
    "type": "excalidraw",
    "version": 2,
    "source": "claude-code",
    "elements": elements,
    "appState": {
        "gridSize": None,
        "viewBackgroundColor": "#ffffff",
    },
    "files": {},
}

with open("/home/jlapthor/tmp/hcp-stuff/hcp-architecture.excalidraw", "w") as f:
    json.dump(excalidraw, f, indent=2)

print(f"Generated {len(elements)} elements")
print(f"File written to hcp-architecture.excalidraw")
