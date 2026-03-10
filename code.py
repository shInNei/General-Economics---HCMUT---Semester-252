import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_white

# 1. Đọc file dữ liệu gốc
# Đảm bảo file data.xlsx nằm cùng thư mục với file code.py này
df = pd.read_excel('data.xlsx')

# ==========================================
# BƯỚC TIỀN XỬ LÝ DỮ LIỆU (PREPROCESSING)
# ==========================================

# 2. Hàm làm sạch các cột số (xóa dấu chấm, xử lý chữ nan)
def clean_numeric(val):
    if pd.isna(val) or str(val).strip().lower() == 'nan':
        return np.nan
    # Xóa dấu chấm phân cách hàng ngàn và đổi phẩy thành chấm (nếu có)
    clean_val = str(val).replace('.', '').replace(',', '.')
    try:
        return float(clean_val)
    except ValueError:
        return np.nan

# 3. Áp dụng hàm làm sạch cho các cột chứa dữ liệu
cols_to_clean = ['Y_DoanhThu', 'K_TaiSanCoDinh', 'L_LaoDong', 'TongTaiSan']
for col in cols_to_clean:
    if col in df.columns:
        df[col] = df[col].apply(clean_numeric)

# 4. Xóa bỏ các dòng bị rỗng (NaN) ở các biến đưa vào mô hình
df_clean = df.dropna(subset=['Y_DoanhThu', 'K_TaiSanCoDinh', 'L_LaoDong', 'TongTaiSan']).copy()

# 5. Tính tỷ lệ K/A
df_clean['K_A_Ratio'] = (df_clean['K_TaiSanCoDinh'] / df_clean['TongTaiSan']) * 100

# ==========================================
# BƯỚC CHẠY MÔ HÌNH
# ==========================================

# 6. Lọc các công ty sản xuất (K/A >= 5%)
df_filtered = df_clean[df_clean['K_A_Ratio'] >= 5].copy()

# 7. Chuyển đổi Y và K sang đơn vị Tỷ Đồng (chia cho 10^9)
df_filtered['Y_TyDong'] = df_filtered['Y_DoanhThu'] / 1e9
df_filtered['K_TyDong'] = df_filtered['K_TaiSanCoDinh'] / 1e9

# 8. Lấy logarit tự nhiên (ln)
df_filtered['ln_Y'] = np.log(df_filtered['Y_TyDong'])
df_filtered['ln_K'] = np.log(df_filtered['K_TyDong'])
df_filtered['ln_L'] = np.log(df_filtered['L_LaoDong'])

# 9. Khai báo biến X và y
X = df_filtered[['ln_K', 'ln_L']]
X = sm.add_constant(X) # Thêm hệ số chặn (beta_0)
y = df_filtered['ln_Y']

# 10. Chạy mô hình hồi quy Pooled OLS
model = sm.OLS(y, X).fit()

# 11. In kết quả
print("==============================================================================")
print("SỐ LƯỢNG MẪU ĐƯỢC ĐƯA VÀO CHẠY (Sau khi lọc dữ liệu rỗng và K/A < 5%):", len(df_filtered))
print("==============================================================================")
print(model.summary())

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