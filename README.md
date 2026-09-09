# ✈️ SkyBook - Flight Booking System

SkyBook là một hệ thống Web Ứng dụng Quản lý và Đặt vé Máy bay trực tuyến, được phát triển trên nền tảng **Django (Python)** và hệ quản trị cơ sở dữ liệu **PostgreSQL**. Dự án mang đến trải nghiệm UI/UX hiện đại (theo phong cách Glassmorphism) và cung cấp đầy đủ các luồng nghiệp vụ từ tìm kiếm chuyến bay, đặt chỗ, chọn ghế, đến thanh toán và hoàn tiền.

---

## 🛠 Công nghệ sử dụng
*   **Backend:** Python 3, Django Framework
*   **Database:** PostgreSQL (Lưu trữ đám mây qua Neon Tech)
*   **Frontend:** HTML5, CSS3, Vanilla JS
*   **Các thư viện nổi bật:** `psycopg2`, `dj-database-url`, `decouple` (quản lý biến môi trường), API Gửi Email.

---

## 📂 Cấu trúc Dự án (Architecture)

Dự án được chia thành các Modules (Django Apps) riêng biệt để dễ bảo trì và mở rộng:

*   `config/`: Cấu hình lõi của toàn bộ hệ thống (settings, urls route).
*   `flights/`: Quản lý danh mục (Sân bay, Hãng bay, Máy bay) và Lịch trình chuyến bay.
*   `bookings/`: Xử lý quy trình đặt vé, chọn sơ đồ ghế trên máy bay và khởi tạo vé điện tử.
*   `payments/`: Quản lý giao dịch thanh toán và quy trình duyệt Yêu cầu Hoàn tiền vé.
*   `users/`: Quản lý đăng ký, đăng nhập, phân quyền và mở rộng Hồ sơ người dùng.
*   `recommendations/`: Hiển thị các điểm đến nổi bật ngoài trang chủ.
*   `templates/`: Chứa toàn bộ giao diện HTML.
*   `static/`: Chứa CSS, JavaScript và Hình ảnh tĩnh.

---

## ✨ Tính năng nổi bật (Features)

### 👤 Khách hàng (User)
*   **Tìm kiếm nâng cao:** Tìm kiếm chuyến bay Khứ hồi / Một chiều theo ngày và điểm đến.
*   **Giao diện Chọn ghế trực quan:** Xem sơ đồ máy bay và chọn ghế ngồi thực tế (Hỗ trợ phân chia hạng ghế).
*   **Quản lý vé:** Xem danh sách vé đã đặt, xem chi tiết Vé Điện Tử (E-ticket).
*   **Hỗ trợ Hậu mãi:** Gửi yêu cầu Hủy vé & Hoàn tiền (Hệ thống tự động tính toán số % được hoàn lại dựa trên thời gian bay).
*   **Nhận thông báo:** Nhận Email chứa vé điện tử tự động sau khi thanh toán thành công.

### 🛡 Quản trị viên (Admin)
*   **Quản lý Chuyến bay:** Thêm, Sửa, Xóa lịch trình bay, điều chỉnh giá, thay đổi máy bay...
*   **Quản lý Đơn hàng:** Tra cứu thông tin mọi hành khách, thống kê luồng doanh thu thanh toán.
*   **Duyệt Hoàn tiền:** Theo dõi, phê duyệt hoặc từ chối các yêu cầu hoàn tiền vé của khách.

---

## 🚀 Hướng dẫn Cài đặt & Chạy dự án (Local Development)

### 1. Clone hoặc tải source code
Mở Terminal/CMD và trỏ tới thư mục dự án:
```bash
cd Booking
```

### 2. Thiết lập Môi trường ảo (Virtual Environment)
```bash
python -m venv venv
# Đối với Windows:
venv\Scripts\activate
# Đối với MacOS/Linux:
source venv/bin/activate
```

### 3. Cài đặt Thư viện
```bash
pip install -r requirements.txt
```

### 4. Cấu hình Biến môi trường
Dự án sử dụng file `.env` ở thư mục gốc. Bạn cần tạo file `.env` (hoặc sửa đổi) chứa các thông số kết nối Database (ví dụ Neon PostgreSQL) và Email API. Tham khảo file mẫu nếu có.

### 5. Khởi tạo Database
Biên dịch các Model thành cấu trúc SQL và đẩy lên Database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Khởi chạy Server
```bash
python manage.py runserver
```
Sau đó mở trình duyệt và truy cập: `http://127.0.0.1:8000/`

---

## 👥 Tác giả
* Developed by [Tên của bạn/Nhóm của bạn]
