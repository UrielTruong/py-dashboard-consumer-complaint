# KIỂM THỬ HỆ THỐNG — Dashboard Phân tích Khiếu nại Tài chính

## 1. Dữ liệu mẫu dùng để kiểm thử

| Thuộc tính      | Giá trị mẫu hợp lệ                                                                   |
| --------------- | ------------------------------------------------------------------------------------ |
| product         | Mortgage, Debt collection, Credit card, Checking or savings account                  |
| state           | CA, FL, TX, NY, GA, IL                                                               |
| channel         | Web, Referral, Phone, Postal mail, Fax, Email                                        |
| timely          | Yes, No                                                                              |
| disputed        | Yes, No                                                                              |
| response        | Closed with explanation, Closed with monetary relief, In progress, Untimely response |
| date range      | 2011-12-01 đến 2019-05-10                                                            |
| days_to_resolve | 0 → 365 (mặc định)                                                                   |

Bộ preset mẫu kèm theo (`presets.json`) dùng cho TC nhóm 7.

## 1. Kiểm thử bộ lọc (Filter)

| ID    | Mục tiêu              | Input                            | Kết quả mong đợi                                                                                |
| ----- | --------------------- | -------------------------------- | ----------------------------------------------------------------------------------------------- |
| TC-06 | Lọc theo sản phẩm     | Chọn product = Mortgage          | Mọi biểu đồ/KPI/bảng chỉ phản ánh Mortgage; tổng KPI giảm tương ứng                             |
| TC-07 | Lọc nhiều bang        | states = CA, FL, TX              | Bảng và biểu đồ chỉ chứa 3 bang này                                                             |
| TC-08 | Lọc kênh nộp          | channel = Web                    | Donut kênh chỉ còn Web (100%)                                                                   |
| TC-09 | Lọc đúng hạn          | timely = No                      | Tất cả bản ghi có Đúng hạn = No                                                                 |
| TC-10 | Lọc khiếu kiện lại    | disputed = Yes                   | KPI "Khiếu kiện lại" = 100%                                                                     |
| TC-11 | Lọc khoảng ngày xử lý | slider = 0–30                    | Cột "Số ngày" trong bảng đều ≤ 30                                                               |
| TC-12 | Lọc theo thời gian    | 2018-01-01 → 2019-05-10          | Biểu đồ trend chỉ hiện các tháng trong khoảng này                                               |
| TC-13 | Kết hợp nhiều bộ lọc  | Mortgage + CA + timely=Yes       | Kết quả thỏa đồng thời cả 3 điều kiện (AND)                                                     |
| TC-14 | Tìm kiếm tự do        | search = "wells fargo"           | Bảng chỉ hiện bản ghi có công ty/vấn đề/sản phẩm/mã chứa chuỗi này (không phân biệt hoa thường) |
| TC-15 | Đặt lại bộ lọc        | Bấm "Đặt lại bộ lọc"             | Mọi widget về mặc định, dashboard hiển thị toàn dữ liệu                                         |
| TC-16 | Lọc ra kết quả rỗng   | Kết hợp lọc không có bản ghi nào | Hiện "Không có dữ liệu", không crash                                                            |
| TC-17 | Validate ngày         | date_from > date_to              | Hệ thống không tạo FilterState lỗi (raise ValueError được chặn ở tầng UI)                       |

## 2. Kiểm thử KPI

| ID    | Mục tiêu              | Bước                                    | Kết quả mong đợi                                                         |
| ----- | --------------------- | --------------------------------------- | ------------------------------------------------------------------------ |
| TC-18 | 5 thẻ KPI hiển thị    | Mở app mặc định                         | Tổng khiếu nại, Tỷ lệ giải quyết, Đúng hạn, Khiếu kiện lại, Thời gian TB |
| TC-19 | KPI cập nhật theo lọc | Áp 1 bộ lọc bất kỳ                      | Cả 5 KPI thay đổi đồng bộ với bộ lọc                                     |
| TC-20 | Chỉ số trend          | So sánh kỳ hiện tại với kỳ trước        | Hiển thị mũi tên ▲/▼ kèm % so kỳ trước                                   |
| TC-21 | Tính đúng tỷ lệ       | Đối chiếu thủ công 1 trường hợp lọc nhỏ | Tỷ lệ giải quyết = resolved_n / n đúng                                   |

## 3. Kiểm thử biểu đồ & Insights

| ID    | Mục tiêu          | Bước                         | Kết quả mong đợi                                                                                     |
| ----- | ----------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------- |
| TC-22 | 7 biểu đồ render  | Mở app                       | Trend, product bar, issue bar, channel donut, response stacked, state list, company bar đều hiển thị |
| TC-23 | Tương tác biểu đồ | Hover lên trend line         | Hiện tooltip với tháng và số lượng                                                                   |
| TC-24 | Insights tự động  | Mở app mặc định              | Hiển thị tối đa 7 insight; mỗi thẻ có tag, tiêu đề, mô tả                                            |
| TC-25 | Spike detection   | Lọc khoảng có tháng đột biến | Insight "Bất thường" xuất hiện khi tháng cao nhất > 1.8× trung bình                                  |
| TC-26 | Insight rỗng      | Lọc ra 0 bản ghi             | Không hiển thị insight, không lỗi                                                                    |

## 4. Kiểm thử Preset (Lưu / Tải / Xóa)

| ID    | Mục tiêu                         | Bước                               | Kết quả mong đợi                                                    |
| ----- | -------------------------------- | ---------------------------------- | ------------------------------------------------------------------- |
| TC-27 | Lưu preset                       | Đặt bộ lọc → nhập tên → Lưu        | Preset ghi vào `presets.json`, hiện thông báo thành công            |
| TC-28 | Lưu thiếu tên                    | Bấm Lưu khi tên rỗng               | Cảnh báo "Nhập tên preset trước", không lưu                         |
| TC-29 | Tải preset                       | Chọn "Mortgage - California" → Tải | Toàn bộ widget điền lại đúng cấu hình; dashboard render theo preset |
| TC-30 | Xóa preset                       | Chọn preset → Xóa                  | Preset biến mất khỏi danh sách và `presets.json`                    |
| TC-31 | Preset tồn tại sau khởi động lại | Lưu preset → tắt/mở lại app        | Preset vẫn còn (đọc từ file JSON)                                   |

## 5. Kiểm thử bảng & xuất dữ liệu

| ID    | Mục tiêu            | Bước                            | Kết quả mong đợi                                                 |
| ----- | ------------------- | ------------------------------- | ---------------------------------------------------------------- |
| TC-32 | Phân trang          | Xem bảng chi tiết               | 100 bản ghi/trang; tổng số trang = ceil(n/100)                   |
| TC-33 | Chuyển trang        | Nhập số trang                   | Bảng hiển thị đúng offset, caption "Trang x/y"                   |
| TC-34 | Xuất CSV (≤100k)    | Lọc còn ≤100.000 dòng → Tải CSV | Tải file `export.csv` đầy đủ cột, mở được bằng Excel (UTF-8-sig) |
| TC-35 | Chặn xuất khi >100k | Để bộ lọc rộng (>100k dòng)     | Hiện gợi ý thu hẹp bộ lọc, ẩn nút tải                            |
