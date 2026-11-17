import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

# ==========================================
# CONFIG: Update with exact Appendix C values
# ==========================================
CORRIDOR_SPLITS = {
    "utica_south": "82.6% (to/from Utica via Rt-12 / Mulaney Rd)",
    "marcy": "2.9% (Marcy)",
    "rome_north": "1.2% (Rome via Rt-12N / Glass Factory Rd)",
    "other_east": "13.3% (Other / East Corridor - Verify App. C)",
}

DRIVEWAY_VOLUMES = {
    "access_1": "Access 1\n[Insert Entering/Exiting %]",
    "access_2": "Access 2\nAM: 161 | PM: 105",
    "access_3": "Access 3\nAM: [Verify] | PM: [Verify]",
    "mulaney_split": "[Verify]% Entering\n[Verify]% Exiting",
}

# ==========================================
# FIGURE SETUP
# ==========================================
fig, ax = plt.subplots(figsize=(10, 14), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 145)
ax.axis("off")
ax.set_facecolor("#F7F7F2")
fig.patch.set_facecolor("#F7F7F2")

# --- 1. Creek / Stream (West of Edic Rd) ---
stream_x = [17, 15, 11, 8, 5, 0]
stream_y = [145, 115, 96, 88, 72, 68]
ax.plot(stream_x, stream_y, color="#6BAED6", linewidth=2.5, zorder=1)
ax.plot([8, 4, 0], [88, 92, 93], color="#6BAED6", linewidth=1.8, zorder=1)
ax.plot([14, 10, 6, 6], [62, 48, 36, 0], color="#6BAED6", linewidth=2.2, zorder=1)

# --- 2. External Roadways ---
road_color = "#D9D9D9"
edge_color = "#737373"

# Edic Rd (N-S)
ax.add_patch(patches.Rectangle((17, 0), 5, 145, fc=road_color, ec=edge_color, lw=1.2, zorder=2))
# Mulaney Rd (E-W)
ax.add_patch(patches.Rectangle((0, 24), 100, 5, fc=road_color, ec=edge_color, lw=1.2, zorder=2))
# Glass Factory Rd (NE)
ax.plot([22, 52, 70], [134, 134, 142], color=edge_color, lw=8, solid_capstyle="butt", zorder=2)
ax.plot([22, 52, 70], [134, 134, 142], color=road_color, lw=6, solid_capstyle="butt", zorder=3)

# Road Labels
ax.text(13.5, 73, "EDIC RD", rotation=90, va="center", ha="center", fontsize=13, fontweight="bold", color="#222")
ax.text(52, 20.5, "MULANEY RD", va="center", ha="center", fontsize=13, fontweight="bold", color="#222")
ax.text(38, 134, "GLASS FACTORY RD", va="center", ha="center", fontsize=10, fontweight="bold", color="#222", zorder=5)

# --- 3. Internal Loop Roadway ---
# North leg (Access 1) -> Center N-S Spine -> Middle leg (Access 2) -> East leg -> South leg (Access 3)
internal_paths = [
    ([22, 54, 58, 58], [107, 107, 103, 66]),   # Access 1 & North-South Spine
    ([22, 82, 85, 85, 78, 78], [66, 66, 62, 38, 34, 29]),  # Access 2 to Access 3
]
for px, py in internal_paths:
    ax.plot(px, py, color=edge_color, lw=7, solid_joinstyle="round", zorder=2)
    ax.plot(px, py, color=road_color, lw=5, solid_joinstyle="round", zorder=3)

# --- 4. Parking Zones & Buildings ---
def draw_box(x, y, w, h, label, fc="#BDBDBD", ec="#525252", fs=8.5, zorder=4):
    rect = patches.Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.2, zorder=zorder)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, label, va="center", ha="center",
            fontsize=fs, fontweight="bold", color="#111", zorder=zorder + 1)

# Parking background shading
ax.add_patch(patches.Rectangle((27, 110), 16, 6, fc="#E8E8E4", ec="none", zorder=1))
ax.add_patch(patches.Rectangle((24, 83), 30, 20, fc="#E8E8E4", ec="none", zorder=1))
ax.add_patch(patches.Rectangle((63, 72), 29, 12, fc="#E8E8E4", ec="none", zorder=1))
ax.add_patch(patches.Rectangle((36, 33), 38, 11, fc="#E8E8E4", ec="none", zorder=1))

ax.text(35, 113, "PARKING", ha="center", va="center", fontsize=8, color="#555")
ax.text(39, 93, "PARKING", ha="center", va="center", fontsize=9, color="#555")
ax.text(77.5, 78, "PARKING", ha="center", va="center", fontsize=9, color="#555")
ax.text(55, 38.5, "PARKING", ha="center", va="center", fontsize=9, color="#555")

# Buildings (Updated Zoning & ITE LUC Labels)
draw_box(27, 116, 16, 13,
         "NORTH-WEST\n10,000 SF Sports Bar\n(Drinking Place - ITE LUC 975)", fs=7.5)
draw_box(63, 84, 29, 46,
         "NORTH-EAST WAREHOUSE\n640,000 SF Warehouse\n(Distribution Center - ITE LUC 150)", fs=9)
draw_box(24, 69, 30, 14,
         "MIDDLE-LEFT (3 STORY)\n240,000 SF General Office Bldg\n(ITE LUC 710)", fs=8)
draw_box(36, 44, 42, 16,
         "OFFICE 2 / CENTER-BOTTOM\n540,000 SF Office / Light Industrial Park\n(ITE LUC 110)", fs=8.5)

# --- 5. Access Markers (1, 2, 3) ---
def draw_access_pin(x, y, num):
    circ = patches.Circle((x, y), 1.9, fc="#1F5A9E", ec="white", lw=1.2, zorder=8)
    ax.add_patch(circ)
    ax.text(x, y, str(num), color="white", ha="center", va="center",
            fontsize=9, fontweight="bold", zorder=9)

draw_access_pin(24.5, 107, 1)
draw_access_pin(24.5, 66, 2)   # Corrected position at middle driveway
draw_access_pin(76.5, 31, 3)

# --- 6. Directional Flow Arrows (Green = Entering, Red = Exiting) ---
def flow_arrow(x1, y1, x2, y2, color, lw=2.0):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=12),
                zorder=6)

# Access 1 arrows
flow_arrow(19.5, 95, 19.5, 107, "#2CA02C")
flow_arrow(20, 107, 32, 107, "#2CA02C")
flow_arrow(32, 105.5, 21, 105.5, "#D62728")

# Access 2 arrows
flow_arrow(19.5, 42, 19.5, 66, "#2CA02C")
flow_arrow(20, 66.5, 48, 66.5, "#2CA02C")
flow_arrow(48, 65, 20.5, 65, "#D62728")

# Access 3 arrows
flow_arrow(95, 27, 78.5, 27, "#2CA02C")
flow_arrow(78.5, 27, 78.5, 36, "#2CA02C")
flow_arrow(77.2, 36, 77.2, 25.5, "#D62728")
flow_arrow(77.2, 25.5, 95, 25.5, "#D62728")

# --- 7. Clean Callout Boxes ---
bbox_info = dict(boxstyle="round,pad=0.35", fc="white", ec="#444", lw=0.9, alpha=0.95)
ax.text(28, 101.5, DRIVEWAY_VOLUMES["access_1"], fontsize=7.5, ha="left", va="top", bbox=bbox_info, zorder=7)
ax.text(58, 66, DRIVEWAY_VOLUMES["access_2"], fontsize=8, ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.35", fc="#E8F5E9", ec="#2CA02C", lw=1), zorder=7)
ax.text(65, 31.5, DRIVEWAY_VOLUMES["access_3"], fontsize=8, ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.35", fc="#FFF3E0", ec="#E65100", lw=1), zorder=7)

# Regional Corridor Labels
ax.text(24, 138, CORRIDOR_SPLITS["rome_north"], fontsize=8, bbox=bbox_info, zorder=7)
ax.text(24, 131, CORRIDOR_SPLITS["marcy"], fontsize=8, bbox=bbox_info, zorder=7)
ax.text(24, 52, CORRIDOR_SPLITS["utica_south"], fontsize=8.5, fontweight="bold", bbox=bbox_info, zorder=7)
ax.text(87, 19, CORRIDOR_SPLITS["other_east"], fontsize=8, ha="center", bbox=bbox_info, zorder=7)
ax.text(88, 33, DRIVEWAY_VOLUMES["mulaney_split"], fontsize=7.5, ha="center", bbox=bbox_info, zorder=7)

# --- 8. North Arrow & Clean Legend ---
ax.annotate("N", xy=(7, 17), xytext=(7, 10),
            ha="center", va="center", fontsize=11, fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color="#111", lw=2, mutation_scale=16), zorder=7)

legend_elements = [
    Line2D([0], [0], color="#2CA02C", lw=2.5, marker=">", markersize=6, label="Entering Trip Flow"),
    Line2D([0], [0], color="#D62728", lw=2.5, marker=">", markersize=6, label="Exiting Trip Flow"),
    Line2D([0], [0], color=road_color, lw=6, label="Roadway / Site Circulation"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor="#1F5A9E", markersize=9, label="Site Access (1, 2, 3)"),
]
ax.legend(handles=legend_elements, loc="lower left", bbox_to_anchor=(0.02, 0.01),
          frameon=True, facecolor="white", edgecolor="#555", fontsize=8.5,
          title="MAP 2: CALIBRATED TRIP DISTRIBUTION", title_fontsize=9)

plt.tight_layout()
plt.savefig("map2_calibrated.png", dpi=300, bbox_inches="tight")
plt.show()