# Dashboard Phân tích Khiếu nại Tài chính

Ứng dụng web phân tích trực quan bộ dữ liệu khiếu nại tài chính của người tiêu dùng (Consumer Complaint Database, ~1,3 triệu bản ghi). Hệ thống cung cấp KPI tổng quan, 7 biểu đồ tương tác, insights tự động, bảng dữ liệu phân trang kèm xuất CSV và tính năng lưu/tải bộ lọc (preset).

Công nghệ: **Python + Streamlit + DuckDB + Plotly + Pandas**, tổ chức theo kiến trúc MVC.

## 1. Yêu cầu

- Python 3.9 trở lên (khuyến nghị 3.10+)
- Khoảng 1,5 GB ổ đĩa trống (cho file CSV nguồn và DuckDB)

## 2. Tải dữ liệu nguồn (đã có trong source code)

File `rows.csv` (~700 MB) **không** được kèm trong repository. Tải từ Kaggle và đặt vào thư mục gốc dự án (cùng cấp với `migrate.py`):

- Nguồn: https://www.kaggle.com/datasets/selener/consumer-complaint-database
- Sau khi giải nén, đổi tên file dữ liệu thành `rows.csv` (nếu cần) và đặt tại thư mục gốc.

## 3. Cài đặt

```bash
# Tạo và kích hoạt môi trường ảo
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Cài thư viện
pip install -r requirements.txt
```

## 4. Nạp dữ liệu vào DuckDB

```bash
python migrate.py
```

## 5. Chạy ứng dụng

```bash
streamlit run app.py
```

Mở trình duyệt tại địa chỉ Streamlit in ra (mặc định http://localhost:8501).

## 6. Cấu trúc thư mục

```
.
├── app.py                  # Điểm khởi động: gọi DashboardController().run()
├── migrate.py              # ETL: nạp rows.csv -> complaints.duckdb
├── requirements.txt        # Thư viện phụ thuộc
├── presets.json            # Bộ lọc đã lưu (preset mẫu kèm sẵn)
├── rows.csv                # Dữ liệu nguồn (tự tải, không có trong repo)
├── complaints.duckdb       # DB sinh ra sau migrate
├── KIEM_THU.md             # Bộ test case kiểm thử chức năng
└── dashboard/
    ├── config.py           # Hằng số: DB_PATH, CSV_PATH, PALETTE, US_STATES, CSS
    ├── controller.py       # Controller MVC: điều phối luồng render
    ├── models/             # Repository + Services (filter, metrics, insights, preset)
    └── views/              # KPI, charts, sidebar, insights, table
```

## 7. Kiểm thử

- Xem `KIEM_THU.md` để biết 35 test case chức năng
- Bộ preset mẫu dùng để chạy thử nhanh các kịch bản lọc tiêu biểu.

## Nguồn dữ liệu

Consumer Complaint Database — https://www.kaggle.com/datasets/selener/consumer-complaint-database
