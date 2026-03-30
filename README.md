# Phân tích Hàm sản xuất Cobb-Douglas Ngành Thép Việt Nam (2020-2024)

Dự án phân tích kinh tế lượng nhằm ước lượng hàm sản xuất Cobb-Douglas cho ngành thép Việt Nam ở cấp độ doanh nghiệp, đánh giá vai trò của Vốn và Lao động đối với Doanh thu thuần bằng phương pháp Pooled OLS. 

Bài tập lớn môn Kinh tế học Đại cương (KTDC) - Trường Đại học Bách Khoa TP.HCM (HCMUT).

## 📁 Cấu trúc thư mục (Repository Structure)

```text
├── data.xlsx                 # File dữ liệu Báo cáo tài chính (đầu vào)
├── code.py                   # Script xử lý dữ liệu, chạy mô hình Pooled OLS và kiểm định
├── plot.py                   # Script vẽ và xuất các biểu đồ trực quan
├── requirements.txt          # Danh sách các thư viện Python cần thiết
├── README.md                 # Tài liệu hướng dẫn (File này)
├── bieu_do_loc_mau.png       # Biểu đồ phân loại số lượng mẫu qua các bước lọc
├── correlation_matrix.png    # Ma trận tương quan (Correlation Matrix)
├── residual_plot.png         # Đồ thị phân phối phần dư (Kiểm định White)
└── scatter_plots.png         # Đồ thị phân tán thể hiện tương quan giữa các biến
```

## 🛠️ Cài đặt & Môi trường (Prerequisites)

Dự án sử dụng Python 3.x. Để cài đặt các thư viện hỗ trợ phân tích dữ liệu cần thiết, hãy mở terminal/command prompt tại thư mục dự án và chạy lệnh sau:

```bash
pip install -r requirements.txt
```

## 🚀 Hướng dẫn chạy code (How to Run)

**Bước 1:** Clone repository này về máy và mở terminal tại thư mục dự án.

**Bước 2:** Chạy file code chính để tiền xử lý dữ liệu từ `data.xlsx` và in ra kết quả mô hình hồi quy cùng các kiểm định thống kê:

```bash
python code.py
```

**Bước 3:** Chạy file vẽ biểu đồ để tạo ra các hình ảnh trực quan phân tích (các file `.png` sẽ được xuất ra và lưu trực tiếp trong thư mục):

```bash
python plot.py
```

## 📈 Kết quả chính (Key Findings)

* **Mô hình Pooled OLS:** Có độ phù hợp cao (R² = 0.925). Không xảy ra hiện tượng phương sai sai số thay đổi.
* **Lao động:** Tác động tích cực và có ý nghĩa thống kê cao (p < 0.01). Khi lao động tăng 1%, doanh thu tăng 0.7308%.
* **Vốn:** Có tác động dương nhưng chưa có ý nghĩa thống kê ở mức 5% (p = 0.183), nguyên nhân chủ yếu do độ trễ đầu tư và tình trạng dư thừa công suất thời kỳ 2020-2024.
* **Hiệu suất theo quy mô:** Toàn ngành đang ở trạng thái **Hiệu suất giảm theo quy mô (Decreasing Returns to Scale)** với tổng hệ số α = 0.8093 < 1.
