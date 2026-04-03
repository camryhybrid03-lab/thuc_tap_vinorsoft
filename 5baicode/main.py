# Bài 1: Lọc và biến đổi dữ liệu cơ bản
# Đề bài: Viết một hàm nhận vào một danh sách các số nguyên. Hàm cần trả về một danh sách mới chỉ chứa bình phương của các số chẵn có trong danh sách gốc.
# Yêu cầu: Bắt buộc dùng List Comprehension và Type Hinting.
def square_evens(numbers: list[int]) -> list[int]:
    """Trả về bình phương của các số chẵn."""
    # List comprehension kết hợp điều kiện lọc (if) và biến đổi (n**2)
    return [n**2 for n in numbers if n % 2 == 0]

# Test thử:
print(square_evens([1, 2, 3, 4, 5, 6])) 
# Kết quả: [4, 16, 36]


# Bài 2: Đếm tần suất xuất hiện (Dictionary & Logic)
# Đề bài: Viết một hàm nhận vào một đoạn văn bản (chuỗi). Hãy đếm số lần xuất hiện của mỗi từ trong đoạn văn bản đó (không phân biệt hoa thường và bỏ qua dấu câu cơ bản như phẩy, chấm). Trả về một Dictionary với key là từ, value là số lần xuất hiện.
# Yêu cầu: Sử dụng Type Hinting và các phương thức xử lý Dictionary gọn gàng (.get()).
def word_frequency(text: str) -> dict[str, int]:
    """Đếm tần suất các từ trong chuỗi."""
    # Xử lý logic: Viết thường chuỗi và loại bỏ dấu câu đơn giản, sau đó tách từ
    clean_words = text.lower().replace(",", "").replace(".", "").split()
    
    freq_dict: dict[str, int] = {}
    for word in clean_words:
        # Dictionary logic: Dùng .get(word, 0) để lấy giá trị hiện tại, nếu chưa có thì gán là 0
        freq_dict[word] = freq_dict.get(word, 0) + 1
        
    return freq_dict

# Test thử:
print(word_frequency("Python is great. Python is fast, and python is fun!"))
# Kết quả: {'python': 3, 'is': 3, 'great': 1, 'fast': 1, 'and': 1, 'fun!': 1}


# Bài 3: Rút trích dữ liệu từ cấu trúc phức tạp
# Đề bài: Cho một danh sách chứa các Dictionary đại diện cho học sinh (gồm name và score). Hãy viết hàm trả về danh sách tên của những học sinh thi đỗ (điểm >= 60).
# Yêu cầu: Kết hợp Type Hinting, truy xuất Dictionary và List Comprehension.
from typing import Union

def get_passed_students(students: list[dict[str, Union[str, int]]], passing_score: int = 60) -> list[str]:
    """Lấy danh sách tên học sinh đỗ."""
    # Sử dụng List comprehension để lặp qua danh sách dict và lọc theo điều kiện
    # Dùng student.get("score", 0) để tránh lỗi KeyError nếu dict thiếu key 'score'
    return [
        student["name"] 
        for student in students 
        if int(student.get("score", 0)) >= passing_score
    ]

# Test thử:
class_data = [
    {"name": "An", "score": 85},
    {"name": "Bình", "score": 45},
    {"name": "Cường", "score": 60}
]
print(get_passed_students(class_data))
# Kết quả: ['An', 'Cường']


# Bài 4: Đảo ngược Dictionary (Xử lý logic phức tạp)
# Đề bài: Viết hàm nhận vào một Dictionary (key: tên người, value: phòng ban). Hàm cần trả về một Dictionary bị đảo ngược: key là tên phòng ban, value là danh sách những người thuộc phòng ban đó.
# Yêu cầu: Type Hinting và sử dụng hàm setdefault của Dictionary để code Pythonic nhất.
def invert_department_dict(d: dict[str, str]) -> dict[str, list[str]]:
    """Nhóm nhân viên theo phòng ban."""
    inverted: dict[str, list[str]] = {}
    
    for employee, department in d.items():
        # Dùng setdefault: Nếu department chưa có trong inverted, tạo key với value là []
        # Sau đó append employee vào list đó. Rất Pythonic và tránh if/else dài dòng.
        inverted.setdefault(department, []).append(employee)
        
    return inverted

# Test thử:
emp_data = {"An": "IT", "Bình": "HR", "Cường": "IT", "Dung": "Marketing"}
print(invert_department_dict(emp_data))
# Kết quả: {'IT': ['An', 'Cường'], 'HR': ['Bình'], 'Marketing': ['Dung']}


# Bài 5: Phân tích cú pháp chuỗi Log (Tổng hợp kỹ năng)
# Đề bài: Cho một chuỗi log hệ thống có định dạng "ERROR:file1.py, WARN:file2.py, ERROR:file3.py". Viết hàm phân tích chuỗi này và trả về một Dictionary nhóm các file theo cấp độ log.
# Yêu cầu: Kết hợp tách chuỗi, List comprehension, Dictionary và logic nhóm dữ liệu.
def parse_system_logs(log_str: str) -> dict[str, list[str]]:
    """Phân tích chuỗi log thành Dictionary phân loại theo mức độ."""
    result: dict[str, list[str]] = {}
    
    if not log_str.strip():
        return result
        
    # List comprehension tạo ra list các tuple/list nhỏ: [['ERROR', 'file1.py'], ['WARN', 'file2.py'], ...]
    entries = [entry.strip().split(':') for entry in log_str.split(',')]
    
    # Destructuring (unpacking) trực tiếp trong vòng lặp for
    for level, filename in entries:
        result.setdefault(level, []).append(filename)
        
    return result

# Test thử:
logs = "ERROR:main.py, WARN:auth.py, INFO:utils.py, ERROR:database.py"
print(parse_system_logs(logs))
# Kết quả: {'ERROR': ['main.py', 'database.py'], 'WARN': ['auth.py'], 'INFO': ['utils.py']}