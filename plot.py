import matplotlib.pyplot as plt

# Dữ liệu cho biểu đồ
categories = ['Mẫu hợp lệ\n(Đưa vào phân tích)', 'Bị loại do thiếu\ndữ liệu (NaN)', 'Bị loại do tỷ trọng\nTSCĐ < 5%']
values = [62, 17, 4]
colors = ['#2ca02c', '#d62728', '#ff7f0e'] # Màu: Xanh lá (Hợp lệ), Đỏ (Bị loại NaN), Cam (Bị loại K/A)

# Khởi tạo biểu đồ
plt.figure(figsize=(8, 6))
bars = plt.bar(categories, values, color=colors, edgecolor='black', linewidth=1.2)

# Thêm con số trên đầu mỗi cột
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, str(yval), 
             ha='center', va='bottom', fontsize=12, fontweight='bold')

# Tùy chỉnh Tiêu đề và Nhãn
plt.title('PHÂN LOẠI SỐ LƯỢNG MẪU QUAN SÁT QUA QUÁ TRÌNH TIỀN XỬ LÝ', fontsize=14, pad=20, fontweight='bold')
plt.ylabel('Số lượng quan sát', fontsize=12, fontweight='bold')
plt.ylim(0, max(values) + 10) # Tạo khoảng trống phía trên cột
plt.grid(axis='y', linestyle='--', alpha=0.7) # Thêm lưới ngang cho dễ nhìn

# Lưu ảnh chất lượng cao để chèn vào báo cáo
plt.tight_layout()
plt.savefig('bieu_do_loc_mau.png', dpi=300)
plt.show()

print("Đã lưu biểu đồ thành công vào file 'bieu_do_loc_mau.png'")