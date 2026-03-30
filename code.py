import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_white

# ==========================================
# BƯỚC 1: ĐỌC DỮ LIỆU
# ==========================================
# Đảm bảo file data.xlsx nằm cùng thư mục với file code.py này
df = pd.read_excel('data.xlsx')

print("==============================================================================")
print(f"1. Số lượng mẫu thô ban đầu (Raw data): {len(df)} quan sát")

# ==========================================
# BƯỚC TIỀN XỬ LÝ DỮ LIỆU (PREPROCESSING)
# ==========================================

# Hàm làm sạch các cột số (xóa dấu chấm, xử lý chữ nan)
def clean_numeric(val):
    if pd.isna(val) or str(val).strip().lower() == 'nan':
        return np.nan
    # Xóa dấu chấm phân cách hàng ngàn và đổi phẩy thành chấm (nếu có)
    clean_val = str(val).replace('.', '').replace(',', '.')
    try:
        return float(clean_val)
    except ValueError:
        return np.nan

# Áp dụng hàm làm sạch cho các cột chứa dữ liệu
cols_to_clean = ['Y_DoanhThu', 'K_TaiSanCoDinh', 'L_LaoDong', 'TongTaiSan']
for col in cols_to_clean:
    if col in df.columns:
        df[col] = df[col].apply(clean_numeric)

# Xóa bỏ các dòng bị rỗng (NaN) ở các biến đưa vào mô hình
df_clean = df.dropna(subset=['Y_DoanhThu', 'K_TaiSanCoDinh', 'L_LaoDong', 'TongTaiSan']).copy()

print(f"2. Số lượng mẫu sau khi xóa dữ liệu khuyết thiếu (NaN): {len(df_clean)} quan sát")

# Tính tỷ lệ K/A
df_clean['K_A_Ratio'] = (df_clean['K_TaiSanCoDinh'] / df_clean['TongTaiSan']) * 100

# Lọc các công ty sản xuất (K/A >= 5%)
df_filtered = df_clean[df_clean['K_A_Ratio'] >= 5].copy()

print(f"3. Số lượng mẫu sau khi lọc công ty sản xuất (K/A >= 5%): {len(df_filtered)} quan sát")
print("==============================================================================\n")

# ==========================================
# BƯỚC CHẠY MÔ HÌNH
# ==========================================

# Chuyển đổi Y và K sang đơn vị Tỷ Đồng (chia cho 10^9)
df_filtered['Y_TyDong'] = df_filtered['Y_DoanhThu'] / 1e9
df_filtered['K_TyDong'] = df_filtered['K_TaiSanCoDinh'] / 1e9

# Lấy logarit tự nhiên (ln)
df_filtered['ln_Y'] = np.log(df_filtered['Y_TyDong'])
df_filtered['ln_K'] = np.log(df_filtered['K_TyDong'])
df_filtered['ln_L'] = np.log(df_filtered['L_LaoDong'])

# Khai báo biến X và y
X = df_filtered[['ln_K', 'ln_L']]
X = sm.add_constant(X) # Thêm hệ số chặn (beta_0)
y = df_filtered['ln_Y']

# Chạy mô hình hồi quy Pooled OLS
model = sm.OLS(y, X).fit()

# In kết quả
print(model.summary())

# ==========================================
# BƯỚC KIỂM ĐỊNH KHUYẾT TẬT
# ==========================================
# Lấy phần dư (residuals) từ mô hình
residuals = model.resid

# Chạy kiểm định White Test
white_test = het_white(residuals, model.model.exog)
labels = ['LM Statistic', 'LM-Test p-value', 'F-Statistic', 'F-Test p-value']
white_results = dict(zip(labels, white_test))

print("\n==============================================================================")
print("KẾT QUẢ KIỂM ĐỊNH WHITE (PHƯƠNG SAI SAI SỐ THAY ĐỔI)")
print("==============================================================================")
print(f"P-value của kiểm định LM: {white_results['LM-Test p-value']:.4f}")
print(f"P-value của kiểm định F : {white_results['F-Test p-value']:.4f}")

if white_results['LM-Test p-value'] < 0.05:
    print("-> KẾT LUẬN: P-value < 0.05, Bác bỏ H0. Mô hình BỊ hiện tượng phương sai sai số thay đổi!")
else:
    print("-> KẾT LUẬN: P-value >= 0.05, Chấp nhận H0. Mô hình KHÔNG BỊ phương sai sai số thay đổi (rất tốt).")

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Cài đặt phông chữ và style đồ thị cho chuẩn học thuật
plt.rcParams.update({'font.size': 12, 'font.family': 'sans-serif'})
sns.set_style("whitegrid")

# ==========================================
# BIỂU ĐỒ 1: MỐI QUAN HỆ GIỮA ĐẦU VÀO VÀ ĐẦU RA (SCATTER PLOTS)
# ==========================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Đồ thị 1: ln(Y) theo ln(K)
sns.regplot(x=df_filtered['ln_K'], y=df_filtered['ln_Y'], ax=axes[0], 
            scatter_kws={'alpha':0.6, 'color':'#1f77b4'}, line_kws={'color':'red', 'lw':2})
axes[0].set_title('Tương quan giữa Vốn và Doanh thu (Logarit)', fontweight='bold')
axes[0].set_xlabel('ln(K) - Log Vốn', fontweight='bold')
axes[0].set_ylabel('ln(Y) - Log Doanh thu', fontweight='bold')

# Ép trục tọa độ đồ thị 1 sát góc
k_min, k_max = int(np.floor(df_filtered['ln_K'].min())), int(np.ceil(df_filtered['ln_K'].max()))
y_min, y_max = int(np.floor(df_filtered['ln_Y'].min())), int(np.ceil(df_filtered['ln_Y'].max()))
axes[0].set_xlim(left=k_min, right=k_max)
axes[0].set_ylim(bottom=y_min, top=y_max)
axes[0].set_xticks(range(k_min, k_max + 1))
axes[0].set_yticks(range(y_min, y_max + 1))

# Đồ thị 2: ln(Y) theo ln(L)
sns.regplot(x=df_filtered['ln_L'], y=df_filtered['ln_Y'], ax=axes[1], 
            scatter_kws={'alpha':0.6, 'color':'#2ca02c'}, line_kws={'color':'red', 'lw':2})
axes[1].set_title('Tương quan giữa Lao động và Doanh thu (Logarit)', fontweight='bold')
axes[1].set_xlabel('ln(L) - Log Lao động', fontweight='bold')
axes[1].set_ylabel('ln(Y) - Log Doanh thu', fontweight='bold')

# Ép trục tọa độ đồ thị 2 sát góc
l_min, l_max = int(np.floor(df_filtered['ln_L'].min())), int(np.ceil(df_filtered['ln_L'].max()))
axes[1].set_xlim(left=l_min, right=l_max)
axes[1].set_ylim(bottom=y_min, top=y_max)
axes[1].set_xticks(range(l_min, l_max + 1))
axes[1].set_yticks(range(y_min, y_max + 1))

plt.tight_layout()
plt.savefig('scatter_plots.png', dpi=300)
print("Đã lưu Biểu đồ 1 đã fix format: 'scatter_plots.png'")

# ==========================================
# BIỂU ĐỒ 2: ĐỒ THỊ PHẦN DƯ (KIỂM TRA PHƯƠNG SAI SAI SỐ THAY ĐỔI)
# ==========================================
plt.figure(figsize=(8, 6))
fitted_values = model.fittedvalues
residuals = model.resid

sns.scatterplot(x=fitted_values, y=residuals, alpha=0.7, color='purple', edgecolor='black')
plt.axhline(y=0, color='red', linestyle='--', linewidth=2) # Đường trung bình 0

plt.title('Đồ thị Phần dư và Giá trị dự báo (Residuals vs Fitted)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Giá trị dự báo ln(Y)', fontsize=12, fontweight='bold')
plt.ylabel('Phần dư (Residuals)', fontsize=12, fontweight='bold')

# Ép trục tọa độ đồ thị phần dư sát góc
f_min, f_max = int(np.floor(fitted_values.min())), int(np.ceil(fitted_values.max()))
r_min, r_max = int(np.floor(residuals.min())), int(np.ceil(residuals.max()))
plt.xlim(left=f_min, right=f_max)
plt.ylim(bottom=r_min, top=r_max)
plt.xticks(range(f_min, f_max + 1))
# Trục Y của phần dư có thể là số thập phân, nên chỉ giới hạn biên
plt.yticks(np.arange(r_min, r_max + 0.5, 0.5))

plt.tight_layout()
plt.savefig('residual_plot.png', dpi=300)
print("Đã lưu Biểu đồ 2 đã fix format: 'residual_plot.png'")


# ==========================================
# BƯỚC MỚI BỔ SUNG: THỐNG KÊ MÔ TẢ & MA TRẬN TƯƠNG QUAN
# ==========================================
import matplotlib.pyplot as plt
import seaborn as sns

print("\n==============================================================================")
print("BẢNG THỐNG KÊ MÔ TẢ CÁC BIẾN (LOGARIT)")
print("==============================================================================")
# Lấy các thông số cơ bản (Mean, Std, Min, Max) và làm tròn 3 chữ số thập phân
desc_stats = df_filtered[['ln_Y', 'ln_K', 'ln_L']].describe().round(3)
print(desc_stats.loc[['mean', 'std', 'min', 'max']])

# Vẽ Ma trận tương quan (Correlation Matrix)
plt.figure(figsize=(7, 5))
corr_matrix = df_filtered[['ln_Y', 'ln_K', 'ln_L']].corr()

# Dùng seaborn để vẽ Heatmap (Biểu đồ nhiệt)
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".3f", linewidths=0.5, vmin=0, vmax=1)
plt.title('Ma trận tương quan (Correlation Matrix)', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=300)
print("\nĐã lưu biểu đồ Ma trận tương quan thành file: 'correlation_matrix.png'")