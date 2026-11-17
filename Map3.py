import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

# =========================================================
# 1. VERIFIED PARAMETERS (100% CONSERVED)
# =========================================================
PCT_RT12_EAST = 0.92   # 88.80% confirmed (Utica/Deerfield/Herkimer/Schuyler/Frankfort) + 3.20% minor towns
PCT_NORTH_WEST = 0.08  # 4.79% confirmed (Marcy/Rome/Kirkland) + 3.21% minor towns

# Site Trips (AM_In, AM_Out, PM_In, PM_Out) + Proportioned 2029 No-Build Driveway Totals
# Acc 1: 0 NB | Acc 2: 11 AM (10 In/1 Out), 20 PM (3 In/17 Out) | Acc 3: 32 AM (21 In/11 Out), 68 PM (15 In/53 Out)
TOTAL_DWY = {
    "acc1": (68, 39, 306, 155),
    "acc2": (1092, 144, 194, 950),
    "acc3": (154, 83, 91, 321),
}

def turns(in_v, out_v):
    m_in = round(in_v * PCT_RT12_EAST)
    m_out = round(out_v * PCT_RT12_EAST)
    return m_in, in_v - m_in, m_out, out_v - m_out

a1_am, a1_pm = turns(*TOTAL_DWY["acc1"][:2]), turns(*TOTAL_DWY["acc1"][2:])
a2_am, a2_pm = turns(*TOTAL_DWY["acc2"][:2]), turns(*TOTAL_DWY["acc2"][2:])
a3_am, a3_pm = turns(*TOTAL_DWY["acc3"][:2]), turns(*TOTAL_DWY["acc3"][2:])

# External Link 2029 Total Build Volumes (2029 No-Build + Distributed Site Trips)
mulaney_eb_am = 229 + a1_am[2] + a2_am[2] + a3_am[2]  # 473
mulaney_eb_pm = 328 + a1_pm[2] + a2_pm[2] + a3_pm[2]  # 1,640
mulaney_wb_am = 170 + a3_am[0] + a2_am[0] + a1_am[0]  # 1,380
mulaney_wb_pm = 70  + a3_pm[0] + a2_pm[0] + a1_pm[0]  # 614
edic_nb_am = 220 + a2_am[0] + a1_am[0]                # 1,288
edic_nb_pm = 268 + a2_pm[0] + a1_pm[0]                # 728

# =========================================================
# 2. FIGURE & BASE GEOMETRY
# =========================================================
fig, ax = plt.subplots(figsize=(11.5, 15.5), dpi=300)
ax.set_xlim(0, 108)
ax.set_ylim(0, 152)
ax.axis("off")
ax.set_facecolor("#F7F7F2")
fig.patch.set_facecolor("#F7F7F2")

ax.text(54, 148.5, "MAP 3: 2029 TOTAL BUILD PEAK HOUR TRAFFIC VOLUMES (AM / PM)",
        ha="center", va="center", fontsize=12.5, fontweight="bold", color="#111",
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#333", lw=1.2))

# Stream
ax.plot([17, 15, 11, 8, 5, 0], [145, 115, 96, 88, 72, 68], color="#6BAED6", lw=2.3, zorder=1)
ax.plot([14, 10, 6, 6], [62, 48, 36, 0], color="#6BAED6", lw=2.0, zorder=1)

# External Roads
road_c, edge_c = "#D9D9D9", "#666666"
ax.add_patch(patches.Rectangle((17, 0), 5, 145, fc=road_c, ec=edge_c, lw=1.2, zorder=2))
ax.add_patch(patches.Rectangle((0, 24), 108, 5, fc=road_c, ec=edge_c, lw=1.2, zorder=2))
ax.plot([22, 52, 74], [133, 133, 141], color=edge_c, lw=8, solid_capstyle="butt", zorder=2)
ax.plot([22, 52, 74], [133, 133, 141], color=road_c, lw=6, solid_capstyle="butt", zorder=3)

ax.text(13.5, 78, "EDIC RD", rotation=90, va="center", ha="center", fontsize=12.5, fontweight="bold", color="#222")
ax.text(52, 20.5, "MULANEY RD", va="center", ha="center", fontsize=12.5, fontweight="bold", color="#222")
ax.text(40, 133, "GLASS FACTORY RD", va="center", ha="center", fontsize=9.5, fontweight="bold", color="#222", zorder=5)

# Internal Loop Roadway
for px, py in [([22, 54, 58, 58], [107, 107, 103, 66]),
               ([22, 84, 87, 87, 79, 79], [66, 66, 62, 38, 34, 29])]:
    ax.plot(px, py, color=edge_c, lw=7, solid_joinstyle="round", zorder=2)
    ax.plot(px, py, color=road_c, lw=5, solid_joinstyle="round", zorder=3)

# Buildings
def draw_box(x, y, w, h, label, fs=8):
    ax.add_patch(patches.Rectangle((x, y), w, h, fc="#BDBDBD", ec="#525252", lw=1.2, zorder=4))
    ax.text(x + w/2, y + h/2, label, va="center", ha="center", fontsize=fs, fontweight="bold", color="#111", zorder=5)

draw_box(28, 115, 16, 12, "NORTH-WEST\n10,000 SF Sports Bar\n(ITE LUC 975)", fs=7.5)
draw_box(65, 84, 30, 44, "NORTH-EAST WAREHOUSE\n640,000 SF Warehouse\n(ITE LUC 150)", fs=8.5)
draw_box(24, 69, 30, 14, "MIDDLE-LEFT (3 STORY)\n240,000 SF General Office\n(ITE LUC 710)", fs=8)
draw_box(36, 44, 42, 16, "OFFICE 2 / CENTER-BOTTOM\n540,000 SF Office / Light Ind.\n(ITE LUC 110)", fs=8)

# =========================================================
# 3. ACCESS PINS & FLOW ARROWS
# =========================================================
for x, y, n in [(24.5, 107, 1), (24.5, 66, 2), (77.5, 31, 3)]:
    ax.add_patch(patches.Circle((x, y), 1.9, fc="#1F5A9E", ec="white", lw=1.2, zorder=8))
    ax.text(x, y, str(n), color="white", ha="center", va="center", fontsize=9, fontweight="bold", zorder=9)

def arrow(x1, y1, x2, y2, color):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.0, mutation_scale=11), zorder=6)

arrow(19.5, 96, 19.5, 107, "#2CA02C"); arrow(20, 107.6, 33, 107.6, "#2CA02C"); arrow(33, 106.0, 21, 106.0, "#D62728")
arrow(19.5, 42, 19.5, 66, "#2CA02C");  arrow(20, 66.8, 48, 66.8, "#2CA02C");  arrow(48, 65.2, 20.5, 65.2, "#D62728")
arrow(102, 27.2, 79.6, 27.2, "#2CA02C"); arrow(79.6, 27.2, 79.6, 36, "#2CA02C")
arrow(78.0, 36, 78.0, 25.5, "#D62728");  arrow(78.0, 25.5, 102, 25.5, "#D62728")

# =========================================================
# 4. TURNING MOVEMENT & LINK VOLUME CALLOUTS
# =========================================================
tm_style = dict(boxstyle="round,pad=0.35", fc="white", ec="#1F5A9E", lw=1.2, alpha=0.96)
link_style = dict(boxstyle="round,pad=0.3", fc="#FFFDE7", ec="#795548", lw=0.95, alpha=0.96)

# Access 1 Turning Box
ax.text(28, 102.5,
        "ACCESS 1 (2029 Total Build)\n"
        f"AM: NB R-In {a1_am[0]} | SB L-In {a1_am[1]} | WB L-Out {a1_am[2]} | WB R-Out {a1_am[3]}\n"
        f"PM: NB R-In {a1_pm[0]} | SB L-In {a1_pm[1]} | WB L-Out {a1_pm[2]} | WB R-Out {a1_pm[3]}",
        fontsize=6.8, va="top", ha="left", bbox=tm_style, zorder=7)

# Access 2 Turning Box
ax.text(42, 62.2,
        "ACCESS 2 (2029 Total Build | Incl. 11 AM / 20 PM NB)\n"
        f"AM: NB R-In {a2_am[0]:,} | SB L-In {a2_am[1]} | WB L-Out {a2_am[2]} | WB R-Out {a2_am[3]}\n"
        f"PM: NB R-In {a2_pm[0]} | SB L-In {a2_pm[1]} | WB L-Out {a2_pm[2]} | WB R-Out {a2_pm[3]}",
        fontsize=6.8, va="top", ha="center", bbox=tm_style, zorder=7)

# Access 3 Turning Box
ax.text(59, 34.5,
        "ACCESS 3 (2029 Total Build | Incl. 32 AM / 68 PM NB)\n"
        f"AM: WB R-In {a3_am[0]} | EB L-In {a3_am[1]} | SB L-Out {a3_am[2]} | SB R-Out {a3_am[3]}\n"
        f"PM: WB R-In {a3_pm[0]} | EB L-In {a3_pm[1]} | SB L-Out {a3_pm[2]} | SB R-Out {a3_pm[3]}",
        fontsize=6.8, va="center", ha="center", bbox=tm_style, zorder=7)

# External Link Totals
ax.text(2, 126,
        "INT 1 (Edic / Glass Factory)\n"
        "2029 NB: NB 172/145 | SB 73/166\n"
        "Glass Factory: 73 AM / 70 PM",
        fontsize=6.8, bbox=link_style, zorder=7)

ax.text(2, 44,
        "Edic Rd NB (N of Mulaney)\n"
        f"2029 NB: 220 AM / 268 PM\n"
        f"2029 TB: {edic_nb_am:,} AM / {edic_nb_pm:,} PM",
        fontsize=7.0, bbox=link_style, zorder=7)

ax.text(92, 14,
        "Mulaney Rd East (to/from NY-12)\n"
        f"EB (to Rt-12): {mulaney_eb_am:,} AM / {mulaney_eb_pm:,} PM\n"
        f"WB (from Rt-12): {mulaney_wb_am:,} AM / {mulaney_wb_pm:,} PM",
        fontsize=7.0, ha="center", bbox=link_style, zorder=7)

# =========================================================
# 5. HCM 7th EDITION CAPACITY & MITIGATION CALLOUTS
# =========================================================
ax.annotate(
    "HCM 7th Ed. Mitigation (Edic / Glass Factory):\n"
    "• Dual Left-Turn Lanes + Channelized Right-Turn Bay\n"
    "• Prevents Capacity Breakdown (V/C > 1.0 under 2029 Build)",
    xy=(20, 133), xytext=(50, 135),
    arrowprops=dict(arrowstyle="->", color="#C62828", lw=1.4),
    fontsize=7.3, fontweight="bold", color="#7F0000",
    bbox=dict(boxstyle="round,pad=0.4", fc="#FFEBEE", ec="#C62828", lw=1.2), va="center", zorder=8
)

ax.annotate(
    "HCM 7th Ed. Check (Main Interior Collector):\n"
    "• 573 veh/hr (PM Outbound Segment) | 2-Lane Section\n"
    "• V/C = 0.819 | LOS D (Consistent with Sec. 7)",
    xy=(58, 76), xytext=(74, 70),
    arrowprops=dict(arrowstyle="->", color="#2E7D32", lw=1.4),
    fontsize=7.3, color="#1B5E20",
    bbox=dict(boxstyle="round,pad=0.4", fc="#E8F5E9", ec="#2E7D32", lw=1.2), va="center", zorder=8
)

# =========================================================
# 6. NORTH ARROW & LEGEND
# =========================================================
ax.annotate("N", xy=(7, 17), xytext=(7, 10), ha="center", va="center", fontsize=11, fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color="#111", lw=2, mutation_scale=16), zorder=7)

legend_elements = [
    Line2D([0], [0], color="#2CA02C", lw=2.5, marker=">", markersize=6, label="Entering 2029 Build Flow (AM / PM)"),
    Line2D([0], [0], color="#D62728", lw=2.5, marker=">", markersize=6, label="Exiting 2029 Build Flow (AM / PM)"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor="#1F5A9E", markersize=9, label="Site Access Node (1, 2, 3)"),
    patches.Patch(fc="#FFFDE7", ec="#795548", label="2029 No-Build & Total Build Corridor Volumes"),
    patches.Patch(fc="#FFEBEE", ec="#C62828", label="HCM 7th Ed. Mitigation (V/C > 1.0)"),
]
ax.legend(handles=legend_elements, loc="lower left", bbox_to_anchor=(0.02, 0.01),
          frameon=True, facecolor="white", edgecolor="#555", fontsize=7.8,
          title="MAP 3: 2029 TOTAL BUILD (92% Rt-12 / 8% N-W)", title_fontsize=8.2)

plt.tight_layout()
plt.savefig("map3_2029_total_build_final.png", dpi=300, bbox_inches="tight")
plt.show()