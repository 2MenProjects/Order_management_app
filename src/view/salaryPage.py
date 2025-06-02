from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter import filedialog as fd
import json
from src.Model.TaiXe import TaiXe
from src.Model.LichLamViec import LichLamViec
import random
import re
import openpyxl
from datetime import datetime, date
import calendar


class SalaryPage:
    def __init__(self, root, switch_page, detail_page_func):
        self.root = root
        self.root.configure(bg="#f0f4f8")
        self.root.columnconfigure(0, weight=1)

        self.switch_page = switch_page
        self.detail_page_func = detail_page_func

        self.filename = "src/database/detail_employee.json"
        self.file_driver = "src/database/driver.json"
        self.fileyear = "src/database/years.json"
        self.file_account = "src/database/account.json"

        self.dataLich = self.load_detail_employee(self.filename)
        self.dataDriver = self.load_data_from_file(self.file_driver)
        self.dataAccount = self.load_data_from_file(self.file_account)

        self.dstx = [TaiXe.from_dict(taixe) for taixe in self.dataDriver]

        lbl_title = Label(
            self.root, text=f"Quản lý lương", font=("Arial", 13), bg="#f0f4f8")
        lbl_title.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        today = datetime.now()
        nam_hien_tai = today.year
        ds_nam_hoat_dong = self.load_years()

        self.cbo_Thang = ttk.Combobox(self.root, width=20, font=(
            "Arial", 13), state="normal", values=[f"Tháng {i}" for i in range(1, 13)])
        self.cbo_Thang.current(today.month - 1)
        self.cbo_Thang.grid(row=0, column=1, padx=10)

        self.cbo_Nam = ttk.Combobox(self.root, width=20, font=(
            "Arial", 13), state="normal", values=[f"Năm {i}" for i in ds_nam_hoat_dong])
        self.cbo_Nam.current(ds_nam_hoat_dong.index(nam_hien_tai))
        self.cbo_Nam.grid(row=0, column=2, padx=5)

        def loc_table():
            self.refresh_table()

        self.btn_filter = Button(
            self.root, text="Lọc", font=("Arial", 13), bg="#3D2AEE", width=5, fg="white", command=loc_table)
        self.btn_filter.grid(row=0, column=3, padx=5)

        self.create_frame_table()
        self.create_frame_duoi_table()
        self.refresh_table()

    def row_selection(self):
        selected_item = self.table.focus()
        if selected_item:
            item_values = self.table.item(selected_item)['values']
            if item_values:
                self.btn_xem.config(state="normal")

                self.maNhanVien = item_values[0]

    def load_data_from_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            mb.showerror("Lỗi", f"Lỗi đọc file driver: {e}")
            return

    def load_years(self):
        try:
            with open(self.fileyear, "r", encoding="utf-8") as file:
                years = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            years = []

        current_year = datetime.now().year
        if current_year not in years:
            years.append(current_year)
            years.sort()

            with open(self.fileyear, "w", encoding="utf-8") as file:
                json.dump(years, file, indent=4)

        return years

    def create_frame_table(self):
        self.frame_table = Frame(self.root)
        self.frame_table.grid(row=1, column=0, sticky="news", columnspan=4)

        columns = ("Mã", "Họ và tên", "Chức vụ", "Lương cơ bản",
                   "Tổng công (giờ)", "Tổng lương")
        self.table = ttk.Treeview(self.frame_table, columns=columns,
                                  show="headings", height=15)
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=150)

        self.table.tag_configure("oddrow", background="#f0f0f0")
        self.table.tag_configure("evenrow", background="#ffffff")
        self.scrollbar = ttk.Scrollbar(
            self.frame_table, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.table.pack(fill="both", expand=True)

        self.table.bind("<<TreeviewSelect>>", lambda e: self.row_selection())

    def create_frame_duoi_table(self):
        self.frame_duoi_table = Frame(self.root)
        self.frame_duoi_table.grid(
            row=2, column=0, sticky="news", columnspan=4)

        self.frame_duoi_table.columnconfigure(0, weight=1)
        self.frame_duoi_table.columnconfigure(1, weight=10)

        self.frame_left = Frame(self.frame_duoi_table)
        self.frame_left.grid(row=0, column=0, sticky="news")

        self.create_frame_buttons()
        self.create_frame_sl_gio_lam()

    def create_frame_buttons(self):
        def in_bang_cham_cong(thang, nam):
            file_path = fd.asksaveasfilename(defaultextension=".xlsx", filetypes=[
                                             ("Excel files", "*.xlsx")], title="In bảng chấm công", initialfile=f"Bang_Cham_Cong_Thang_{thang}_nam_{nam}.xlsx")
            if not file_path:
                return

            wb = openpyxl.Workbook()
            wb.remove(wb.active)

            danh_sach_nhan_vien = []

            for nv in self.dataAccount:
                danh_sach_nhan_vien.append({
                    "ma": nv["tenTaiKhoan"],
                    "ten": nv["tenNguoiDung"],
                    "chuc_vu": nv["loaiTaiKhoan"],
                    "luong_co_ban": nv["luongCoBan"]
                })

            for nv in self.dataDriver:
                danh_sach_nhan_vien.append({
                    "ma": nv["maTaiXe"],
                    "ten": nv["tenTaiXe"],
                    "chuc_vu": "Nhân viên giao hàng",
                    "luong_co_ban": nv["luongCoBan"]
                })

            # calendar.monthrange(nam, thang) -> (first_weekday, number_of_days)
            so_ngay = calendar.monthrange(nam, thang)[1]

            for nv in danh_sach_nhan_vien:
                ma = nv["ma"]
                ten = nv["ten"]
                chuc_vu = nv["chuc_vu"]
                luong_co_ban = "{:,}đ".format(
                    int(nv["luong_co_ban"])).replace(",", ".")

                sheet_name = ma
                ws = wb.create_sheet(title=sheet_name)

                ws.append([f"Bảng chấm công tháng {thang} năm {nam}"])
                ws.append(["Mã nhân viên: ", ma])
                ws.append(["Họ tên: ", ten])
                ws.append(["Chức vụ: ", chuc_vu])
                ws.append(["Lương cơ bản: ", luong_co_ban])
                ws.append([])
                ws.append(["Ngày", "Thứ", "Giờ làm"])

                for ngay in range(1, so_ngay + 1):
                    thu = date(nam, thang, ngay).strftime(
                        "%A")  # -> Tên đầy đủ của thứ trong tuần
                    thu_vn = {
                        "Monday": "Hai", "Tuesday": "Ba", "Wednesday": "Tư",
                        "Thursday": "Năm", "Friday": "Sáu",
                        "Saturday": "Bảy", "Sunday": "Chủ nhật"
                    }.get(thu, thu)
                    ws.append([f"{ngay:02d}/{thang}/{nam}", thu_vn, ""])

            try:
                wb.save(file_path)
                mb.showinfo("Thành công", "Xuất file Excel thành công!")
            except Exception as e:
                mb.showerror("Lỗi", f"Không thể lưu file:\n{e}")

        def chon_nam_thang():
            popup = Toplevel(self.root)
            popup.title("Chọn tháng và năm")
            popup.geometry("300x150")

            Label(popup, text="Tháng: ").pack(pady=5)
            cbo_Thang = ttk.Combobox(popup, values=list(
                range(1, 13)), state="readonly")
            cbo_Thang.current(0)
            cbo_Thang.pack()

            Label(popup, text="Năm:").pack(pady=5)
            current_year = datetime.now().year
            cbo_nam = ttk.Combobox(popup, values=list(
                range(current_year - 5, current_year + 6)), state="readonly")
            cbo_nam.set(current_year)
            cbo_nam.pack()

            def confirm():
                thang = int(cbo_Thang.get())
                nam = int(cbo_nam.get())
                popup.destroy()
                in_bang_cham_cong(thang, nam)

            Button(popup, text="Xác nhận", command=confirm).pack(pady=10)

        def xem():
            self.switch_page(lambda: self.detail_page_func(self.maNhanVien))

        self.frame_buttons = Frame(self.frame_left)
        self.frame_buttons.grid(row=0, column=0, sticky="news")
        self.btn_xem = Button(self.frame_buttons, text="Xem", width=15, height=2, font=(
            "Arial", 13, "bold"), bg="#00B050", fg="white", state="disabled", command=xem)
        self.btn_xem.grid(row=0, column=0, padx=10, pady=5)

        self.btn_In_Bang_Cham_Cong = Button(self.frame_buttons, text="In bảng chấm công",
                                            bg="#C32AE2",
                                            fg="white",
                                            width=20,
                                            height=2,
                                            font=("Arial", 13, "bold"), command=chon_nam_thang)
        self.btn_In_Bang_Cham_Cong.grid(row=0, column=1, pady=5, padx=10)

    def create_frame_sl_gio_lam(self):
        self.frame_tong_gio_lam = Frame(self.frame_duoi_table)
        self.frame_tong_gio_lam.grid(row=0, column=1, sticky="news")
        self.frame_tong_gio_lam.columnconfigure(0, weight=1)

    def refresh_table(self):
        self.btn_xem.config(state="disabled")

        for row in self.table.get_children():
            self.table.delete(row)

        thang = int(self.cbo_Thang.get().replace("Tháng ", ""))
        nam = int(self.cbo_Nam.get().replace("Năm ", ""))

        for index, user in enumerate(self.dataAccount):
            ma = user["tenTaiKhoan"]
            hoten = user["tenNguoiDung"]
            luong_co_ban = int(user["luongCoBan"])
            chuc_vu = user["loaiTaiKhoan"]

            lich_lam = self.dataLich.get(ma, [])
            lich_trong_thang = []

            for x in lich_lam:
                try:
                    ngay_dt = datetime.strptime(x.ngay, "%d/%m/%Y")
                    if ngay_dt.month == thang and ngay_dt.year == nam:
                        lich_trong_thang.append(x)
                except:
                    continue

            tong_cong = sum(x.gioLam for x in lich_trong_thang)
            tong_luong = tong_cong * luong_co_ban

            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.table.insert("", END, values=(
                ma, hoten, chuc_vu, "{:,}đ".format(
                    luong_co_ban).replace(",", "."), tong_cong,
                "{:,}đ".format(tong_luong).replace(",", ".")), tags=(tag,))

        for index, tx in enumerate(self.dataDriver):
            ma = tx["maTaiXe"]
            hoten = tx["tenTaiXe"]
            luong_co_ban = int(tx["luongCoBan"])
            chuc_vu = "Nhân viên giao hàng"

            lich_lam = self.dataLich.get(ma, [])
            lich_trong_thang = []

            for x in lich_lam:
                try:
                    ngay_dt = datetime.strptime(x.ngay, "%d/%m/%Y")
                    if ngay_dt.month == thang and ngay_dt.year == nam:
                        lich_trong_thang.append(x)
                except:
                    continue

            tong_cong = sum(x.gioLam for x in lich_trong_thang)
            tong_luong = tong_cong * luong_co_ban

            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.table.insert("", END, values=(
                ma, hoten, chuc_vu, "{:,}đ".format(
                    luong_co_ban).replace(",", "."), tong_cong,
                "{:,}đ".format(tong_luong).replace(",", ".")), tags=(tag,))

    def load_detail_employee(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            result = {}
            for item in data:
                ma = item["maNhanVien"]
                nam = item["Nam"]
                thang = item["Thang"]
                lich_raw = item["lichLamViec"]

                lich = []
                for x in lich_raw:
                    ngay_str = f"{x['ngay']:02d}/{thang:02d}/{nam}"
                    lich.append(LichLamViec(ngay=ngay_str,
                                thu=x["thu"], gioLam=x["gioLam"]))

                if ma in result:
                    result[ma].extend(lich)
                else:
                    result[ma] = lich

            return result
        except (json.JSONDecodeError, FileNotFoundError):
            return []
