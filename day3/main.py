import requests
import re
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, insert, select

# --- 1. THIẾT LẬP DATABASE (SQLAlchemy Core) ---
# Tạo file database web_data.db trong cùng thư mục
engine = create_engine('sqlite:///web_data.db')
metadata = MetaData()

# Định nghĩa cấu trúc bảng
books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(250)),
    Column('price', Float),
    Column('stock_status', String(100))
)

# Lệnh tạo bảng nếu chưa tồn tại
metadata.create_all(engine)

# --- 2. HÀM CÀO DỮ LIỆU THÔNG MINH ---
def scrape_books(num_pages=5):
    all_books = []
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    
    print(f"🕵️  Bắt đầu cào {num_pages} trang dữ liệu...")
    
    for page in range(1, num_pages + 1):
        url = base_url.format(page)
        try:
            response = requests.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"⚠️  Bỏ qua trang {page} (Lỗi {response.status_code})")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article', class_='product_pod')

            for art in articles:
                title = art.h3.a['title']
                price_text = art.find('p', class_='price_color').text
                
                # Dùng REGEX để chỉ lấy số và dấu chấm (ví dụ: £51.77 -> 51.77)
                # Cách này sạch hơn replace từng ký tự lạ
                price_match = re.search(r"[\d.]+", price_text)
                price = float(price_match.group()) if price_match else 0.0
                
                stock = art.find('p', class_='instock availability').text.strip()

                all_books.append({
                    "title": title,
                    "price": price,
                    "stock_status": stock
                })
            print(f"✅ Đã xong trang {page}")
            
        except Exception as e:
            print(f"❌ Lỗi khi cào trang {page}: {e}")
            
    return all_books

# --- 3. LƯU VÀO DATABASE (DÙNG BULK INSERT) ---
def save_to_db(data):
    if not data:
        print("📭 Không có dữ liệu để lưu.")
        return
        
    # Dùng engine.begin() để tự động Commit hoặc Rollback nếu có lỗi
    with engine.begin() as conn:
        print(f"📥 Đang lưu {len(data)} cuốn sách vào Database...")
        
        # Xóa dữ liệu cũ (để mỗi lần chạy file là làm mới hoàn toàn)
        conn.execute(books_table.delete())
        
        # BULK INSERT: Chèn hàng loạt một lúc thay vì chạy vòng lặp
        # Cách này nhanh hơn gấp nhiều lần khi dữ liệu lớn
        conn.execute(insert(books_table), data)
        
    print("🚀 Hoàn tất: Dữ liệu đã nằm gọn trong SQL!")

# --- 4. HÀM KIỂM TRA KẾT QUẢ ---
def verify_data():
    with engine.connect() as conn:
        # Lấy 5 cuốn sách đầu tiên để xem thử
        query = select(books_table).limit(5)
        result = conn.execute(query).fetchall()
        
        print("\n--- KẾT QUẢ TRONG DATABASE (5 CUỐN ĐẦU) ---")
        for row in result:
            print(f"📖 {row.title[:30]}... | 💰 {row.price} £ | ✅ {row.stock_status}")

# --- CHƯƠNG TRÌNH CHÍNH ---
if __name__ == "__main__":
    # 1. Cào dữ liệu (Bạn có thể sửa số trang tùy ý)
    scraped_data = scrape_books(num_pages=3)
    
    # 2. Lưu vào SQL
    save_to_db(scraped_data)
    
    # 3. Kiểm tra lại
    verify_data()