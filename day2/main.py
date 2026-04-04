import time
from abc import ABC, abstractmethod

# 1. DECORATOR: Ghi nhật ký hệ thống
def system_log(func):
    def wrapper(*args, **kwargs):
        print(f"\n[LOG] Thực hiện lệnh: {func.__name__.upper()}")
        return func(*args, **kwargs)
    return wrapper

# 2. OOP & KẾ THỪA
class Employee(ABC):
    def __init__(self, emp_id, name, base_salary):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = base_salary

    @abstractmethod
    def calculate_salary(self):
        pass

    def __str__(self):
        return f"ID: {self.emp_id:<5} | Tên: {self.name:<15} | Lương: {self.calculate_salary():,.0f} VNĐ"

class FullTimeEmployee(Employee):
    def calculate_salary(self):
        return self.base_salary * 1.2 # Lương + 20% thưởng

class PartTimeEmployee(Employee):
    def __init__(self, emp_id, name, rate, hours):
        super().__init__(emp_id, name, 0)
        self.rate = rate
        self.hours = hours
    def calculate_salary(self):
        return self.rate * self.hours

# 3. CONTEXT MANAGER: Quản lý phiên làm việc
class HRApp:
    def __enter__(self):
        print("🚀 Đang khởi động hệ thống quản lý nhân sự...")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("\n🔒 Đã đóng hệ thống an toàn.")

# 4. GENERATOR: Lọc dữ liệu thông minh (Tiết kiệm bộ nhớ)
def salary_filter_generator(employees, min_salary):
    for emp in employees:
        if emp.calculate_salary() >= min_salary:
            yield emp

# 5. LỚP QUẢN LÝ CHÍNH
class HRManager:
    def __init__(self):
        self.employees = []

    @system_log
    def add_emp(self, emp):
        self.employees.append(emp)
        print(f"✅ Đã thêm nhân viên thành công!")

    def show_all(self):
        print("\n--- DANH SÁCH TẤT CẢ NHÂN VIÊN ---")
        if not self.employees: print("Chưa có nhân viên nào.")
        for e in self.employees: print(e)

    def delete_emp(self, eid):
        old_len = len(self.employees)
        self.employees = [e for e in self.employees if str(e.emp_id) != str(eid)]
        if len(self.employees) < old_len:
            print(f"🗑️ Đã xóa nhân viên có ID: {eid}")
        else:
            print(f"❌ Không tìm thấy ID này.")

    def total_payroll(self):
        total = sum(e.calculate_salary() for e in self.employees)
        print(f"\n💰 TỔNG QUỸ LƯƠNG CÔNG TY: {total:,.0f} VNĐ")

# --- GIAO DIỆN CHÍNH ---
def main():
    with HRApp():
        manager = HRManager()
        while True:
            print("\n" + "="*40)
            print("      HỆ THỐNG QUẢN LÝ NHÂN SỰ v2.0")
            print("="*40)
            print("1. Thêm nhân viên")
            print("2. Xem danh sách nhân viên")
            print("3. Xóa nhân viên (theo ID)")
            print("4. Lọc nhân viên lương cao (Generator)")
            print("5. Thống kê tổng quỹ lương")
            print("6. Thoát")
            print("="*40)
            
            choice = input("Mời bạn nhập lựa chọn (1-6): ")

            if choice == '1':
                name = input("Họ tên: ")
                eid = input("ID: ")
                type_emp = input("Loại (1: Fulltime, 2: Parttime): ")
                if type_emp == '1':
                    sal = float(input("Lương cơ bản: "))
                    manager.add_emp(FullTimeEmployee(eid, name, sal))
                else:
                    rate = float(input("Lương/giờ: "))
                    hrs = float(input("Số giờ làm: "))
                    manager.add_emp(PartTimeEmployee(eid, name, rate, hrs))

            elif choice == '2':
                manager.show_all()

            elif choice == '3':
                eid = input("Nhập ID cần xóa: ")
                manager.delete_emp(eid)

            elif choice == '4':
                # Kiểm tra nếu danh sách nhân viên đang trống
                if not manager.employees:
                    print("⚠️ Danh sách trống, không có nhân viên để lọc.")
                else:
                    # Sử dụng hàm max() với tham số key là hàm tính lương để tìm nhân viên lương cao nhất
                    # Đây là cách viết cực kỳ Pythonic thay vì dùng vòng lặp for truyền thống
                    top_emp = max(manager.employees, key=lambda e: e.calculate_salary())
                    
                    print(f"\n--- NHÂN VIÊN CÓ LƯƠNG CAO NHẤT ---")
                    print(f"⭐ Tên: {top_emp.name}")
                    print(f"🆔 ID: {top_emp.emp_id}")
                    print(f"💰 Mức lương: {top_emp.calculate_salary():,.0f} VNĐ")

            elif choice == '5':
                manager.total_payroll()

            elif choice == '6':
                print("Đang thoát...")
                break
            else:
                print("⚠️ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()

    