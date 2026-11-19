#!/usr/bin/env python3
"""Generates all Master's Thesis Publication Figures based on empirical data.

Replaces ALL ASCII/text diagrams with high-resolution 300 DPI charts:
1. fig_cold_start_comparison.png (Cold-Start & VRAM Bottleneck vs AST Grounding)
2. fig_council_sota_architecture.png (5 Pillars Architecture Diagram)
3. fig_critic_repair_attribution.png (Round 1 vs Round 2 Sửa lỗi & Bảo toàn Mutation)
4. fig_case_studies_comparison.png (Case Studies: Numpydoc & Genty Grounding Leap)
5. fig_pareto_frontier_ci_cd.png (Pareto Trade-off: Quality vs Latency/Cost)
6. fig_tco_breakeven_analysis.png (TCO Annual Economics: Cloud LPU vs On-premise GPU)
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "monograph_final_deliverables" / "figures"
DATA_DIR = BASE_DIR / "monograph_final_deliverables" / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Set global styles - Clean Publication Standards
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 11.5
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['figure.dpi'] = 300

# Color palette
C_NAVY = '#1A237E'
C_BLUE = '#1976D2'
C_CYAN = '#0288D1'
C_GREEN = '#2E7D32'
C_LIGHT_GREEN = '#4CAF50'
C_AMBER = '#F57C00'
C_RED = '#D32F2F'
C_PURPLE = '#7B1FA2'
C_GREY_LIGHT = '#F5F7FA'
C_GREY_BORDER = '#CFD8DC'
C_TEXT_DARK = '#263238'


def plot_cold_start_comparison():
    """Figure: Cold-Start Latency & VRAM Footprint comparison."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2), gridspec_kw={'width_ratios': [1.2, 1]})
    
    # Panel 1: Latency (Log Scale)
    methods = ['Upstream Call-Graph RAG\n(95 LLM Calls)', 'Standard Council\n(Single-Turn)', 'Council-SOTA\n(Static AST Grounding)']
    latencies = [2627.0, 7.4, 0.045]  # seconds
    colors = [C_RED, C_AMBER, C_GREEN]
    
    y_pos = np.arange(len(methods))
    bars = ax1.barh(y_pos, latencies, color=colors, height=0.52, edgecolor=C_TEXT_DARK, linewidth=0.8)
    ax1.set_xscale('log')
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(methods, fontsize=9.5, fontweight='bold', color=C_TEXT_DARK)
    ax1.set_xlabel('Thời Gian Khởi Động (Giây - Log Scale)', fontsize=10, fontweight='bold')
    ax1.set_title('(a) Thời Gian Khởi Động (Cold-Start Latency)', pad=10, color=C_NAVY)
    ax1.grid(axis='x', linestyle='--', alpha=0.5)
    
    # Add data labels
    ax1.text(2627.0 * 1.2, 0, '2.627 s', va='center', fontweight='bold', color=C_RED, fontsize=9)
    ax1.text(7.4 * 1.2, 1, '7.4 s', va='center', fontweight='bold', color=C_AMBER, fontsize=9)
    ax1.text(0.045 * 1.3, 2, '0.045 s (58.377x)', va='center', fontweight='bold', color=C_GREEN, fontsize=9)
    ax1.set_xlim(0.01, 20000)

    # Panel 2: VRAM Consumption
    vram_methods = ['Upstream RAG\n(NF4 Quant)', 'Council-SOTA\n(AST Grounding)']
    vram_usage = [15.2, 0.012]  # GB
    vram_capacity = 16.0  # Dual T4 16GB limit
    
    x = np.arange(len(vram_methods))
    bars2 = ax2.bar(x, vram_usage, color=[C_RED, C_GREEN], width=0.42, edgecolor=C_TEXT_DARK, linewidth=0.8)
    ax2.axhline(vram_capacity, color='black', linestyle=':', linewidth=1.4, label='Giới Hạn VRAM T4 (16 GB)')
    
    ax2.set_xticks(x)
    ax2.set_xticklabels(vram_methods, fontsize=9.5, fontweight='bold', color=C_TEXT_DARK)
    ax2.set_ylabel('Chiếm Dụng Bộ Nhớ VRAM (GB)', fontsize=10, fontweight='bold')
    ax2.set_title('(b) Chiếm Dụng VRAM GPU', pad=10, color=C_NAVY)
    ax2.set_ylim(0, 18.5)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    ax2.legend(loc='upper right', frameon=True, fontsize=8.5)
    
    ax2.text(0, 15.2 + 0.5, '15.2 GB (95%)', ha='center', fontweight='bold', color=C_RED, fontsize=9)
    ax2.text(1, 0.012 + 0.5, '0.012 GB (RAM)', ha='center', fontweight='bold', color=C_GREEN, fontsize=9)

    plt.tight_layout()
    plt.savefig(OUT_DIR / "fig_cold_start_comparison.png", dpi=300)
    plt.savefig(OUT_DIR / "fig_cold_start_comparison.svg")
    plt.close()
    print("[+] Saved fig_cold_start_comparison.png and .svg")


def plot_council_sota_architecture():
    """Figure: Publication-grade Architecture diagram for Council-SOTA 5 Pillars."""
    fig, ax = plt.subplots(figsize=(11.5, 6.8))
    ax.axis('off')
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # Title Box
    title_box = patches.FancyBboxPatch((6, 91), 88, 7, boxstyle="round,pad=0.5", fc=C_NAVY, ec="none")
    ax.add_patch(title_box)
    ax.text(50, 94.5, "KIẾN TRÚC 5 TRỤ CỘT: COUNCIL-SOTA", 
            ha='center', va='center', color='white', fontsize=12.5, fontweight='bold')

    # Pillar 1: AST Grounding
    p1 = patches.FancyBboxPatch((4, 46), 24, 40, boxstyle="round,pad=0.6", fc='#E8EAF6', ec=C_NAVY, lw=1.4)
    ax.add_patch(p1)
    ax.text(16, 81, "TRỤ CỘT 1:\nAST GROUNDING", ha='center', va='center', color=C_NAVY, fontweight='bold', fontsize=9.5)
    ax.text(16, 63, "• Trích xuất AST tĩnh\n• Bảng định danh Γ_scope\n• Khắc phục 100% import\n• Chi phí: 0 Token, <50ms", 
            ha='center', va='center', color=C_TEXT_DARK, fontsize=8.5, linespacing=1.5)
    
    # Pillar 2: Coder & Two-Round Critic Loop
    p2 = patches.FancyBboxPatch((31, 30), 38, 56, boxstyle="round,pad=0.6", fc='#E3F2FD', ec=C_BLUE, lw=1.6)
    ax.add_patch(p2)
    ax.text(50, 81, "TRỤ CỘT 2: TWO-ROUND ADAPTIVE CRITIC", ha='center', va='center', color=C_BLUE, fontweight='bold', fontsize=10)
    
    coder_box = patches.FancyBboxPatch((33, 67), 34, 9, boxstyle="round,pad=0.3", fc='white', ec=C_BLUE, lw=1)
    ax.add_patch(coder_box)
    ax.text(50, 71.5, "Coder SLM (gpt-oss-20b)\nSinh bộ kiểm thử ban đầu T_init", ha='center', va='center', color=C_TEXT_DARK, fontsize=8.0, fontweight='bold')
    
    pytest_box = patches.FancyBboxPatch((33, 53), 34, 9, boxstyle="round,pad=0.3", fc='#FFF3E0', ec=C_AMBER, lw=1)
    ax.add_patch(pytest_box)
    ax.text(50, 57.5, "Runner Sandbox (pytest)\nThực thi cô lập & Traceback", ha='center', va='center', color=C_TEXT_DARK, fontsize=8.0, fontweight='bold')
    
    critic_box = patches.FancyBboxPatch((33, 36), 34, 12, boxstyle="round,pad=0.3", fc='white', ec=C_GREEN, lw=1)
    ax.add_patch(critic_box)
    ax.text(50, 42, "Two-Round Critic Loop:\n• Vòng 1: Cú pháp / Import (24 ca)\n• Vòng 2: Vi sai Assertion (5 ca)", ha='center', va='center', color=C_GREEN, fontsize=8.0, fontweight='bold')

    # Pillar 3 & 4: Safe Normalizer & Quality Auditor
    p34 = patches.FancyBboxPatch((72, 46), 24, 40, boxstyle="round,pad=0.6", fc='#F1F8E9', ec=C_GREEN, lw=1.4)
    ax.add_patch(p34)
    ax.text(84, 81, "TRỤ CỘT 3 & 4:\nQUALITY GATE", ha='center', va='center', color=C_GREEN, fontweight='bold', fontsize=9.5)
    ax.text(84, 63, "• Preflight Normalizer\n• Quality Auditor Gate\n• Khử assert hiển nhiên\n• Flake-rate: 0.00%", 
            ha='center', va='center', color=C_TEXT_DARK, fontsize=8.5, linespacing=1.5)

    # Pillar 5: Circuit Breaker & Economics (Bottom Banner)
    p5 = patches.FancyBboxPatch((4, 6), 92, 19, boxstyle="round,pad=0.6", fc='#FFFDE7', ec=C_AMBER, lw=1.4)
    ax.add_patch(p5)
    ax.text(50, 20.5, "TRỤ CỘT 5: RÀO CHẮN TÀI CHÍNH & TỐI ƯU HÓA CI/CD", ha='center', va='center', color='#E65100', fontweight='bold', fontsize=10)
    ax.text(26, 11.5, "• Hạn mức an toàn: Max $1.00 USD\n• Tiêu thụ thực tế: $0.5166 USD", ha='center', va='center', color=C_TEXT_DARK, fontsize=8.5)
    ax.text(74, 11.5, "• Đơn giá: $0.0013 USD / Suite\n• Giảm 76.5% TCO so với GPU tại chỗ", ha='center', va='center', color=C_TEXT_DARK, fontsize=8.5)

    # Arrows
    arrow_style = dict(arrowstyle="->", lw=1.8, color=C_NAVY)
    ax.annotate("", xy=(31, 67), xytext=(28, 67), arrowprops=arrow_style)
    ax.annotate("", xy=(72, 67), xytext=(69, 67), arrowprops=arrow_style)
    
    # Critic loop arrows
    ax.annotate("", xy=(33, 42), xytext=(33, 53), arrowprops=dict(arrowstyle="->", lw=1.5, color=C_AMBER, connectionstyle="arc3,rad=-0.35"))
    ax.annotate("", xy=(67, 71.5), xytext=(67, 45), arrowprops=dict(arrowstyle="->", lw=1.5, color=C_GREEN, connectionstyle="arc3,rad=-0.35"))

    plt.tight_layout()
    plt.savefig(OUT_DIR / "fig_council_sota_architecture.png", dpi=300)
    plt.savefig(OUT_DIR / "fig_council_sota_architecture.svg")
    plt.close()
    print("[+] Saved fig_council_sota_architecture.png and .svg")


def plot_critic_repair_attribution():
    """Figure: Round 1 vs Round 2 Critic Attribution and Mutation Preservation."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.4))
    
    # Panel 1: Number of repairs in 105 trials
    rounds = ['Vòng 1 (Round 1)\nCú pháp & Import', 'Vòng 2 (Round 2)\nVi Sai Assertion']
    counts = [24, 5]
    total_repairs = 29
    colors = [C_BLUE, C_GREEN]
    
    bars = ax1.bar(rounds, counts, color=colors, width=0.42, edgecolor=C_TEXT_DARK, linewidth=0.8)
    ax1.set_ylabel('Số Ca Sửa Lỗi (Trials)', fontsize=10, fontweight='bold')
    ax1.set_title('(a) Phân Bổ 29 Ca Sửa Lỗi', pad=10, color=C_NAVY)
    ax1.set_ylim(0, 32)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar, count in zip(bars, counts):
        pct = (count / total_repairs) * 100
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                 f'{count} ca\n({pct:.1f}%)', ha='center', va='bottom', fontweight='bold', fontsize=9.0)
        
    ax1.text(0.5, 29.2, 'Tổng: 29 ca / 105 trials SOTA (27.6%)', 
             ha='center', va='center', bbox=dict(boxstyle='round,pad=0.35', fc='#E8EAF6', ec=C_NAVY, lw=0.9),
             fontsize=9.0, fontweight='bold', color=C_NAVY)

    # Panel 2: Target specifics of Round 2
    r2_targets = ['typesystem_oneof', 'docstring_parser_google', 'genty_args', 'pycg_imports']
    r2_cases = [2, 1, 1, 1]
    r2_colors = [C_PURPLE, C_CYAN, C_AMBER, C_GREEN]
    
    y_pos = np.arange(len(r2_targets))
    ax2.barh(y_pos, r2_cases, color=r2_colors, height=0.48, edgecolor=C_TEXT_DARK, linewidth=0.8)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(r2_targets, fontsize=9.0, fontweight='bold', color=C_TEXT_DARK)
    ax2.invert_yaxis()  # Top-down natural reading hierarchy
    ax2.set_xlabel('Số Ca Cứu Vãn Riêng Biệt', fontsize=10, fontweight='bold')
    ax2.set_title('(b) 5 Ca Cứu Vãn Tại Vòng 2', pad=10, color=C_NAVY)
    ax2.set_xlim(0, 3.8)  # Generous headroom to prevent any text clipping
    ax2.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax2.grid(axis='x', linestyle='--', alpha=0.5)
    
    callouts = [
        '2 ca (Pass: 20% → 100%)',
        '1 ca (Sửa thụt lề docstring)',
        '1 ca (Chuẩn hóa kwargs)',
        '1 ca (Khởi tạo receiver)'
    ]
    for idx, (cnt, callout, col) in enumerate(zip(r2_cases, callouts, r2_colors)):
        ax2.text(cnt + 0.08, idx, callout, va='center', fontweight='bold', color=col, fontsize=8.5)

    plt.tight_layout()
    plt.savefig(OUT_DIR / "fig_critic_repair_attribution.png", dpi=300)
    plt.savefig(OUT_DIR / "fig_critic_repair_attribution.svg")
    plt.close()
    print("[+] Saved fig_critic_repair_attribution.png and .svg")


def plot_case_studies_comparison():
    """Figure: Case Studies comparison before vs after Grounding refinement."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2))
    
    cases = ['Case 1: numpydoc\n(Thuộc tính AST)', 
             'Case 2: genty_dataset\n(Ký tự @genty_dataset)']
    
    pass_before = [40.0, 40.0]
    pass_after  = [60.0, 60.0]
    
    line_before = [21.88, 24.39]
    line_after  = [32.50, 39.02]

    x = np.arange(len(cases))
    width = 0.30
    
    # Panel 1: Pass Rate
    rects1 = ax1.bar(x - width/2, pass_before, width, label='Trước Tinh Chỉnh', color=C_AMBER, edgecolor=C_TEXT_DARK, linewidth=0.8)
    rects2 = ax1.bar(x + width/2, pass_after, width, label='Sau Tinh Chỉnh', color=C_GREEN, edgecolor=C_TEXT_DARK, linewidth=0.8)
    
    ax1.set_ylabel('Tỷ Lệ Vượt Qua - Pass Rate (%)', fontsize=10, fontweight='bold')
    ax1.set_title('(a) Tăng Trưởng Tỷ Lệ Vượt Qua', pad=10, color=C_NAVY)
    ax1.set_xticks(x)
    ax1.set_xticklabels(cases, fontsize=9.0, fontweight='bold')
    ax1.set_ylim(0, 80)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.legend(loc='upper left', fontsize=8.5)
    
    for r1, r2 in zip(rects1, rects2):
        ax1.text(r1.get_x() + r1.get_width()/2, r1.get_height() + 1.2, f'{r1.get_height():.0f}%', ha='center', va='bottom', fontsize=8.5, fontweight='bold')
        ax1.text(r2.get_x() + r2.get_width()/2, r2.get_height() + 1.2, f'{r2.get_height():.0f}%\n(+20%)', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=C_GREEN)

    # Panel 2: Line Coverage
    rects3 = ax2.bar(x - width/2, line_before, width, label='Trước Tinh Chỉnh', color=C_AMBER, edgecolor=C_TEXT_DARK, linewidth=0.8)
    rects4 = ax2.bar(x + width/2, line_after, width, label='Sau Tinh Chỉnh', color=C_CYAN, edgecolor=C_TEXT_DARK, linewidth=0.8)
    
    ax2.set_ylabel('Độ Phủ Dòng Mã - Line Coverage (%)', fontsize=10, fontweight='bold')
    ax2.set_title('(b) Tăng Trưởng Độ Phủ Dòng Mã', pad=10, color=C_NAVY)
    ax2.set_xticks(x)
    ax2.set_xticklabels(cases, fontsize=9.0, fontweight='bold')
    ax2.set_ylim(0, 52)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    ax2.legend(loc='upper left', fontsize=8.5)

    for r1, r2 in zip(rects3, rects4):
        gain = r2.get_height() - r1.get_height()
        ax2.text(r1.get_x() + r1.get_width()/2, r1.get_height() + 1.0, f'{r1.get_height():.1f}%', ha='center', va='bottom', fontsize=8.5, fontweight='bold')
        ax2.text(r2.get_x() + r2.get_width()/2, r2.get_height() + 1.0, f'{r2.get_height():.1f}%\n(+{gain:.1f}%)', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=C_NAVY)

    plt.tight_layout()
    plt.savefig(OUT_DIR / "fig_case_studies_comparison.png", dpi=300)
    plt.savefig(OUT_DIR / "fig_case_studies_comparison.svg")
    plt.close()
    print("[+] Saved fig_case_studies_comparison.png and .svg")


def plot_pareto_frontier_ci_cd():
    """Figure: Pareto Frontier of Mutation Score & Coverage vs Latency & Cost."""
    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    
    systems = [
        ('Zero-Shot Baseline', 3.2, 24.13, 18.20, 0.0006, C_AMBER, 'o'),
        ('Council Standard', 7.4, 37.75, 28.50, 0.0019, C_PURPLE, 's'),
        ('Upstream Call-Graph RAG', 42.5, 41.20, 31.00, 0.0450, C_RED, '^'),
        ('Council-SOTA (Đề xuất)', 5.8, 47.70, 37.97, 0.0013, C_GREEN, '*'),
    ]
    
    for name, lat, cov, mut, cost, col, m in systems:
        size = 140 if m != '*' else 300
        ax.scatter(lat, cov, color=col, s=size, marker=m, edgecolor='black', linewidth=1.0, label=name, zorder=5)
        
        if 'Council-SOTA' in name:
            ax.annotate(f"{name}\nLine: {cov:.1f}% | Lat: {lat:.1f}s | ${cost:.4f}",
                        xy=(lat, cov), xytext=(lat + 2, cov - 2.5),
                        arrowprops=dict(arrowstyle="->", lw=1.3, color=C_GREEN),
                        fontweight='bold', fontsize=8.5, color=C_GREEN,
                        bbox=dict(boxstyle="round,pad=0.3", fc="#E8F5E9", ec=C_GREEN, lw=1))
        elif 'Upstream' in name:
            ax.annotate(f"{name}\nLine: {cov:.1f}% | Lat: 42.5s",
                        xy=(lat, cov), xytext=(lat - 16, cov - 5),
                        arrowprops=dict(arrowstyle="->", lw=1.0, color=C_RED),
                        fontweight='bold', fontsize=8.0, color=C_RED)
        elif 'Standard' in name:
            ax.annotate(f"{name}\nLine: {cov:.1f}% | Lat: {lat:.1f}s",
                        xy=(lat, cov), xytext=(lat + 1.5, cov + 1),
                        fontweight='bold', fontsize=8.0, color=C_PURPLE)
        else:
            ax.annotate(f"{name}\nLine: {cov:.1f}% | Lat: {lat:.1f}s",
                        xy=(lat, cov), xytext=(lat - 1.5, cov - 5),
                        fontweight='bold', fontsize=8.0, color=C_AMBER)

    # Draw Pareto Frontier Curve
    pareto_x = [3.2, 5.8]
    pareto_y = [24.13, 47.70]
    ax.plot(pareto_x, pareto_y, linestyle='--', color=C_GREEN, linewidth=1.8, label='Biên Pareto Tối Ưu', zorder=3)

    ax.fill_between([0, 50], [0, 0], [55, 55], color=C_GREY_LIGHT, alpha=0.5, zorder=1)
    
    ax.set_xlabel('Thời Gian Phản Hồi (Giây / Test Suite)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Độ Phủ Dòng Mã Đạt Được (%)', fontsize=10, fontweight='bold')
    ax.set_title('ĐƯỜNG BIÊN PARETO TRONG TÍCH HỢP LIÊN TỤC (CI/CD)', pad=12, color=C_NAVY)
    ax.set_xlim(0, 48)
    ax.set_ylim(15, 55)
    ax.grid(True, linestyle='--', alpha=0.5, zorder=2)
    ax.legend(loc='lower right', frameon=True, fontsize=8.5)

    plt.tight_layout()
    plt.savefig(OUT_DIR / "fig_pareto_frontier_ci_cd.png", dpi=300)
    plt.savefig(OUT_DIR / "fig_pareto_frontier_ci_cd.svg")
    plt.close()
    print("[+] Saved fig_pareto_frontier_ci_cd.png and .svg")


def plot_tco_breakeven_analysis():
    """Figure: TCO Annual Economics comparing Cloud Serverless LPU vs On-Premise GPU Cluster."""
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    
    scales_kloc = np.array([10, 25, 50, 100, 200, 300, 500, 1000])
    cloud_cost = 46.15 * scales_kloc
    gpu_cost = 19644 + 2.5 * scales_kloc
    
    ax.plot(scales_kloc, gpu_cost, color=C_RED, marker='s', linewidth=2.0, label='GPU Tại Chỗ (On-Premise GPU)', zorder=4)
    ax.plot(scales_kloc, cloud_cost, color=C_GREEN, marker='o', linewidth=2.2, label='Đám Mây LPU Serverless (Pay-As-You-Go)', zorder=5)

    ax.scatter([100], [4615], color=C_GREEN, s=120, zorder=6, edgecolor='black')
    ax.scatter([100], [19894], color=C_RED, s=120, zorder=6, edgecolor='black')
    
    ax.annotate("Mốc 100 KLOC: Tiết kiệm 76.5% TCO\n(Cloud: $4.615 vs On-Prem: $19.644)",
                xy=(100, 4615), xytext=(125, 9500),
                arrowprops=dict(arrowstyle="->", lw=1.3, color=C_NAVY),
                fontweight='bold', fontsize=8.5, color=C_NAVY,
                bbox=dict(boxstyle="round,pad=0.3", fc="#E3F2FD", ec=C_BLUE, lw=1))

    breakeven_x = 19644 / (46.15 - 2.5)
    breakeven_y = 46.15 * breakeven_x
    ax.scatter([breakeven_x], [breakeven_y], color=C_PURPLE, s=140, marker='X', zorder=6, edgecolor='black')
    ax.annotate(f"Điểm Hòa Vốn: ~{breakeven_x:.0f} KLOC",
                xy=(breakeven_x, breakeven_y), xytext=(breakeven_x - 140, breakeven_y + 7000),
                arrowprops=dict(arrowstyle="->", lw=1.3, color=C_PURPLE),
                fontweight='bold', fontsize=8.5, color=C_PURPLE,
                bbox=dict(boxstyle="round,pad=0.3", fc="#F3E5F5", ec=C_PURPLE, lw=1))

    ax.set_xlabel('Quy Mô Mã Nguồn (Kilo Lines of Code - KLOC)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Tổng Chi Phí Sở Hữu Hàng Năm (USD/Năm)', fontsize=10, fontweight='bold')
    ax.set_title('SO SÁNH TỔNG CHI PHÍ SỞ HỮU (TCO) HÀNG NĂM', pad=12, color=C_NAVY)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax.set_xlim(0, 600)
    ax.set_ylim(0, 45000)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='upper left', frameon=True, fontsize=9.0)

    plt.tight_layout()
    plt.savefig(OUT_DIR / "fig_tco_breakeven_analysis.png", dpi=300)
    plt.savefig(OUT_DIR / "fig_tco_breakeven_analysis.svg")
    plt.close()
    print("[+] Saved fig_tco_breakeven_analysis.png and .svg")


if __name__ == '__main__':
    print("Generating Master's Thesis Figures...")
    plot_cold_start_comparison()
    plot_council_sota_architecture()
    plot_critic_repair_attribution()
    plot_case_studies_comparison()
    plot_pareto_frontier_ci_cd()
    plot_tco_breakeven_analysis()
    print("[+] All 6 publication-grade figures generated successfully in monograph_final_deliverables/figures/!")
