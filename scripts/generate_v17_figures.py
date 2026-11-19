"""Generate publication-grade figures for Monograph v17."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, ArrowStyle

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'reports/Tieu_Luan_CNPMTT_Council_SOTA_v17_assets'
ASSETS.mkdir(parents=True, exist_ok=True)

# 1. Architecture Figure
def make_architecture():
    fig, ax = plt.subplots(figsize=(8.2, 4.4), dpi=300)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis('off')
    
    # Background container for phases
    phase_boxes = [
        (0.02, 0.54, 0.46, 0.42, 'GIAI ĐOẠN 1: TRÍCH XUẤT TĨNH & KHÁM PHÁ THIẾT LẬP', '#F0F4F8'),
        (0.52, 0.54, 0.46, 0.42, 'GIAI ĐOẠN 2: LẬP NGỮ CẢNH & SINH KIỂM THỬ', '#F0F7F4'),
        (0.52, 0.04, 0.46, 0.44, 'GIAI ĐOẠN 3: THỰC THI HỘP CÁT & THU THẬP BẰNG CHỨNG', '#FDF8F0'),
        (0.02, 0.04, 0.46, 0.44, 'GIAI ĐOẠN 4: ĐÁNH GIÁ CHẤT LƯỢNG & SỬA LỖI TỰ ĐỘNG', '#FAF0F2'),
    ]
    for x, y, w, h, title, bg in phase_boxes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.01', facecolor=bg, edgecolor='#B0BEC5', lw=1.2))
        ax.text(x + 0.02, y + h - 0.045, title, fontsize=8.2, fontweight='bold', color='#37474F')

    # Step boxes inside phases
    steps = [
        # Phase 1
        (0.04, 0.57, 0.19, 0.28, '1.1 Phân tích AST\n• Cây cú pháp T_AST(M)\n• Chữ ký & docstring\n• Bảng phạm vi Γ_scope', '#FFFFFF', '#1E88E5'),
        (0.26, 0.57, 0.20, 0.28, '1.2 Thăm dò Thiết lập\n• Khám phá tham số\n• Tạo đối số khả thi S(f)\n• Ngăn rò rỉ oracle ngầm', '#FFFFFF', '#1E88E5'),
        # Phase 2
        (0.54, 0.57, 0.20, 0.28, '2.1 Đóng gói Ngữ cảnh\n• Hàm mục tiêu f + import\n• Khai báo phụ trợ d ∈ Dep(f)\n• Giới hạn token budget B', '#FFFFFF', '#2E7D32'),
        (0.76, 0.57, 0.20, 0.28, '2.2 Suy luận LLM\n• Prompting chuẩn hóa\n• Quy cách: 3 hàm test\n• Mô hình 20B/14B', '#FFFFFF', '#2E7D32'),
        # Phase 3
        (0.54, 0.07, 0.20, 0.32, '3.1 Hộp cát Pytest\n• Cô lập tiến trình phụ\n• Giới hạn 20s/120s\n• Bắt lỗi thu thập/gọi', '#FFFFFF', '#D84315'),
        (0.76, 0.07, 0.20, 0.32, '3.2 Đo đạc Độ phủ\n• Coverage.py (line/branch)\n• Kiểm tra chạm thân f\n• Khóa nghiệm ngặt QG', '#FFFFFF', '#D84315'),
        # Phase 4
        (0.26, 0.07, 0.20, 0.32, '4.1 Chẩn đoán Lỗi\n• Phân loại lỗi cú pháp/gọi\n• Trích lọc traceback\n• Vòng phản hồi sửa lỗi', '#FFFFFF', '#C2185B'),
        (0.04, 0.07, 0.19, 0.32, '4.2 Bộ Chứng cứ\n• Chấp nhận/Bác bỏ\n• Độ phủ phạt SC_penalized\n• Đánh giá Đột biến (MS)', '#FFFFFF', '#C2185B')
    ]
    for x, y, w, h, text, bg, border in steps:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.008', facecolor=bg, edgecolor=border, lw=1.4))
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=7.5, linespacing=1.35, color='#212121')

    # Arrows connecting steps
    conn = [
        ((0.23, 0.71), (0.26, 0.71)),
        ((0.46, 0.71), (0.54, 0.71)),
        ((0.74, 0.71), (0.76, 0.71)),
        ((0.86, 0.57), (0.86, 0.39)),
        ((0.76, 0.23), (0.74, 0.23)),
        ((0.54, 0.23), (0.46, 0.23)),
        ((0.26, 0.23), (0.23, 0.23)),
    ]
    for a, b in conn:
        ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='->', lw=1.6, color='#455A64'))

    # Feedback loop arrow from 4.1 to 2.2
    ax.annotate('', xy=(0.86, 0.57), xytext=(0.36, 0.39),
                arrowprops=dict(arrowstyle='->', lw=1.4, linestyle='dashed',
                                connectionstyle='angle,angleA=90,angleB=180,rad=8', color='#C2185B'))
    ax.text(0.48, 0.46, 'Vòng lặp sửa lỗi chẩn đoán (Diagnostic Feedback, tối đa 2 vòng)', 
            fontsize=7.2, color='#C2185B', style='italic', ha='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF', edgecolor='#C2185B', lw=0.8))

    fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
    fig.savefig(ASSETS / 'architecture.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Generated architecture.png")

# 2. Project Tiers Figure (Filtered by High-Yield, Moderate, Intractable)
def make_project_tiers():
    tiers = {
        'TẦNG 1: HIỆU QUẢ CAO (HIGH-YIELD & TRACTABLE)': [
            ('docstring_parser', 20.0, 25, 'Phân tích chuỗi thuần túy; hợp đồng dữ liệu rõ ràng'),
            ('cookiecutter', 18.2, 22, 'Cấu hình template; ít phụ thuộc phần cứng'),
            ('sanic', 10.3, 39, 'Hàm routing & header; chữ ký hàm tường minh'),
            ('python-string-utils', 8.3, 42, 'Hàm xử lý chuỗi độc lập; không có trạng thái ngầm'),
            ('youtube-dl', 7.9, 70, 'Trích xuất regex & metadata; đầu vào chuỗi xác định'),
            ('thefuck', 6.5, 46, 'Quy tắc sửa lỗi CLI; kiểm tra độc lập từng rule')
        ],
        'TẦNG 2: TRUNG BÌNH & ỔN ĐỊNH (MODERATE & NEUTRAL)': [
            ('httpie', 6.1, 90, 'Thành phần mạng & CLI; bão hòa độ phủ cơ sở'),
            ('tqdm', 5.6, 18, 'Thanh tiến trình; yêu cầu mock luồng I/O / sys.stderr'),
            ('pypara', 4.4, 34, 'Đối tượng kế toán; cấu trúc miền phụ thuộc phức tạp'),
            ('tornado', -1.4, 69, 'Khung bất đồng bộ I/O loop; phụ thuộc socket nội bộ'),
            ('flutes', -3.1, 16, 'Tiện ích cấu trúc dữ liệu nâng cao')
        ],
        'TẦNG 3: SUY BIẾN KỸ THUẬT (INTRACTABLE / DEGENERATE)': [
            ('PySnooper', 0.0, 17, 'Phụ thuộc C-extension (sys.settrace); hộp cát bị chặn'),
            ('dataclasses-json', 0.0, 8, 'Metaclass & MRO động; lỗi xác thực schema lúc sinh'),
            ('apimd', 0.0, 11, 'Trình biên dịch AST nội bộ; vi phạm ràng buộc visitor'),
            ('isort', -12.5, 16, 'Nhiễu ngữ cảnh; token khai báo phụ làm phân tán prompt'),
            ('flutils', -16.0, 25, 'Tràn ngân sách token; suy giảm do trùng lặp biểu tượng')
        ]
    }
    
    fig, ax = plt.subplots(figsize=(8.2, 5.8), dpi=300)
    
    y_labels = []
    y_vals = []
    y_colors = []
    tier_markers = []
    
    current_y = 0
    for tier_name, projs in tiers.items():
        tier_markers.append((current_y, tier_name))
        for name, diff, n_targets, note in projs:
            y_labels.append(f"{name} (N={n_targets})")
            y_vals.append(diff)
            if diff > 5.0:
                y_colors.append('#2E7D32')  # Dark green
            elif diff > 0.0:
                y_colors.append('#81C784')  # Light green
            elif diff == 0.0:
                y_colors.append('#78909C')  # Gray
            else:
                y_colors.append('#D32F2F')  # Red
            current_y += 1
        current_y += 0.8  # spacing between tiers
        
    y_positions = []
    pos = 0
    for tier_name, projs in tiers.items():
        for _ in projs:
            y_positions.append(pos)
            pos += 1
        pos += 0.8
        
    ax.barh(y_positions, y_vals, color=y_colors, height=0.68, edgecolor='#37474F', lw=0.6)
    ax.axvline(0, color='#37474F', lw=1.0, linestyle='--')
    
    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel('Chênh lệch Tỷ lệ Chấp nhận: Ngữ cảnh kết hợp trừ Mã nguồn đơn lẻ (Điểm phần trăm - pp)', fontsize=9, fontweight='bold')
    ax.set_title('Phân loại Thực nghiệm 21 Dự án theo 3 Tầng Kỹ thuật Phần mềm (3.870 Lượt thực thi)', fontsize=10.5, fontweight='bold', pad=12)
    ax.grid(axis='x', alpha=0.2, linestyle=':')
    
    # Add value annotations
    for y, val in zip(y_positions, y_vals):
        sign = '+' if val > 0 else ''
        ax.text(val + (0.5 if val >= 0 else -0.5), y, f"{sign}{val:.1f}%", 
                va='center', ha='left' if val >= 0 else 'right', fontsize=7.5, fontweight='bold')
        
    fig.tight_layout()
    fig.savefig(ASSETS / 'project_tiers.png', dpi=300)
    plt.close(fig)
    print("Generated project_tiers.png")

# 3. Effects Figure
def make_effects():
    fig, ax = plt.subplots(figsize=(7.5, 3.2), dpi=300)
    contrasts = [
        ('Ngữ cảnh kết hợp so với Mã nguồn (C - A)\n[Ước lượng chính RQ1]', 1.86, -1.86, 5.59, '#1E88E5', 'p = 0.3464'),
        ('Thiết lập so với Mã nguồn (B - A)\n[Đóng góp thiết lập RQ2]', -3.07, -8.72, 1.03, '#D32F2F', 'p = 0.2859'),
        ('Ngữ cảnh kết hợp so với Thiết lập (C - B)\n[Đóng góp khai báo phụ trợ RQ2]', 4.94, 0.43, 10.88, '#2E7D32', 'p = 0.0553*')
    ]
    
    y_pos = [0, 1, 2]
    for i, (label, diff, lo, hi, color, pval) in enumerate(contrasts):
        ax.errorbar(diff, i, xerr=[[diff - lo], [hi - diff]], fmt='o', capsize=6, capthick=1.5,
                    color=color, markersize=8, lw=2.0)
        ax.text(hi + 0.6, i, f"{diff:+.2f} pp\n95% CI [{lo:+.2f}, {hi:+.2f}]\n({pval})", 
                va='center', fontsize=8, color='#263238', linespacing=1.2)
        
    ax.axvline(0, linestyle='--', color='#546E7A', lw=1.2)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([c[0] for c in contrasts], fontsize=8.5)
    ax.set_xlabel('Chênh lệch tỷ lệ chấp nhận cân bằng dự án (Điểm phần trăm - pp)', fontsize=9, fontweight='bold')
    ax.set_title('Ước lượng Chênh lệch Tỷ lệ Chấp nhận và Khoảng tin cậy 95% (Sign-flip Exact Test)', fontsize=10, fontweight='bold')
    ax.set_xlim(-12, 16)
    ax.set_ylim(-0.6, 2.6)
    ax.grid(axis='x', alpha=0.25)
    fig.tight_layout()
    fig.savefig(ASSETS / 'effects.png', dpi=300)
    plt.close(fig)
    print("Generated effects.png")

# 4. Mutation & Coverage Illusion Figure
def make_mutation():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.8), dpi=300)
    
    # Left: Mutation Operators Kill Rate
    ops = ['SIR (Statement\nRemoval)', 'AOR (Arithmetic\nOperator)', 'ROR (Relational\nOperator)', 'BVR (Bitwise\nOperator)']
    kills = [82.61, 33.33, 32.89, 0.00]
    totals = ['19/23', '10/30', '42/120', '0/14']
    colors = ['#2E7D32', '#FBC02D', '#FB8C00', '#D32F2F']
    
    bars = ax1.bar(ops, kills, color=colors, edgecolor='#37474F', lw=1.0, width=0.55)
    ax1.set_ylabel('Tỷ lệ Tiêu diệt Đột biến (Kill Rate %)', fontsize=8.5, fontweight='bold')
    ax1.set_title('Độ nhạy Toán tử Đột biến (187 AST Mutants)', fontsize=9.5, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.25, linestyle=':')
    
    for bar, pct, frac in zip(bars, kills, totals):
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 2.5, f"{pct:.1f}%\n({frac})", 
                 ha='center', va='bottom', fontsize=7.5, fontweight='bold')
        
    # Right: The Coverage Illusion Case Study
    cases = ['codetiming_timer', 'pycg_classes']
    cov = [80.85, 41.74]
    ms = [20.00, 90.00]
    
    x = np.arange(len(cases))
    width = 0.32
    
    rects1 = ax2.bar(x - width/2, cov, width, label='Độ phủ Dòng (Statement Coverage %)', color='#1E88E5', edgecolor='#37474F')
    rects2 = ax2.bar(x + width/2, ms, width, label='Điểm Đột biến (Mutation Score %)', color='#D81B60', edgecolor='#37474F')
    
    ax2.set_ylabel('Phần trăm (%)', fontsize=8.5, fontweight='bold')
    ax2.set_title('Ảo tưởng Độ phủ (Coverage Illusion): Độ phủ vs Điểm diệt lỗi', fontsize=9.5, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(cases, fontsize=8.5, fontweight='bold')
    ax2.set_ylim(0, 110)
    ax2.legend(fontsize=7.8, loc='upper center', bbox_to_anchor=(0.5, -0.15), frameon=True)
    ax2.grid(axis='y', alpha=0.25, linestyle=':')
    
    for rect in rects1:
        h = rect.get_height()
        ax2.text(rect.get_x() + rect.get_width()/2, h + 2, f"{h:.1f}%", ha='center', va='bottom', fontsize=7.5)
    for rect in rects2:
        h = rect.get_height()
        ax2.text(rect.get_x() + rect.get_width()/2, h + 2, f"{h:.1f}%", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#D81B60')

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.22)
    fig.savefig(ASSETS / 'coverage_illusion_mutation.png', dpi=300)
    plt.close(fig)
    print("Generated coverage_illusion_mutation.png")

# 5. Cost & Efficiency Tradeoff Figure
def make_cost_efficiency():
    fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=300)
    arms = ['Mã nguồn đơn lẻ\n(Arm A: Source)', 'Thăm dò Thiết lập\n(Arm B: Setup)', 'Ngữ cảnh kết hợp\n(Arm C: Context+Setup)']
    costs = [0.230, 0.279, 0.311] # USD per accepted suite
    accepted = [378, 383, 423] # Accepted suites
    tokens = [2870, 3420, 3980] # Average tokens per suite
    
    x = np.arange(len(arms))
    width = 0.35
    
    ax1 = ax
    ax2 = ax1.twinx()
    
    rects1 = ax1.bar(x - width/2, costs, width, label='Chi phí ước tính / Bộ test đạt (USD)', color='#3949AB', edgecolor='#263238')
    rects2 = ax2.bar(x + width/2, accepted, width, label='Số bộ test đạt chuẩn (/1.290 lượt)', color='#00897B', edgecolor='#263238')
    
    ax1.set_ylabel('Chi phí trên mỗi Bộ kiểm thử đạt (USD)', color='#3949AB', fontsize=8.5, fontweight='bold')
    ax2.set_ylabel('Số bộ kiểm thử đạt chuẩn chấp nhận', color='#00897B', fontsize=8.5, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(arms, fontsize=8.5)
    ax1.set_ylim(0, 0.42)
    ax2.set_ylim(0, 520)
    
    ax1.set_title('Đánh đổi Chi phí & Hiệu quả Sinh kiểm thử trên 3 Nhánh Thực nghiệm', fontsize=10, fontweight='bold')
    
    for rect in rects1:
        h = rect.get_height()
        ax1.text(rect.get_x() + rect.get_width()/2, h + 0.012, f"${h:.3f}", ha='center', va='bottom', fontsize=8, color='#3949AB', fontweight='bold')
    for rect in rects2:
        h = rect.get_height()
        ax2.text(rect.get_x() + rect.get_width()/2, h + 15, f"{int(h)} bộ", ha='center', va='bottom', fontsize=8, color='#00897B', fontweight='bold')

    # Add total budget note
    fig.text(0.5, 0.02, 'Tổng chi phí thực thi toàn bộ 3.870 lượt đạt 1,425 USD (nằm trong trần kiểm soát 3,00 USD)',
             ha='center', fontsize=7.8, style='italic', color='#455A64')

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.18)
    fig.savefig(ASSETS / 'cost_token_efficiency.png', dpi=300)
    plt.close(fig)
    print("Generated cost_token_efficiency.png")

if __name__ == '__main__':
    make_architecture()
    make_project_tiers()
    make_effects()
    make_mutation()
    make_cost_efficiency()
    print("All v17 figures successfully generated!")
