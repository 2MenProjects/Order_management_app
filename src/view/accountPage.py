from tkinter import *
from tkinter import ttk
import json
import os
from src.Model.NhanVien import NhanVien


class AccountPage:
    def __init__(self, root):
        self.root = root
        self.root.columnconfigure(0, weight=1)

        def row_selection():
            selected_item = self.accountTable.focus()
            if selected_item:
                item_values = self.accountTable.item(selected_item)['values']
                if item_values:
                    pass

        # Table
        self.table_frame = Frame(self.root)
        self.table_frame.grid(row=0, column=0, sticky="news")

        columns = ("#1", "#2", "#3", "#4")
        self.accountTable = ttk.Treeview(
            self.table_frame, columns=columns, show="headings")
        self.accountTable.heading("#1", text="Tên tài khoản")
        self.accountTable.heading("#2", text="Tên người dùng")
        self.accountTable.heading("#3", text="Mật khẩu")
        self.accountTable.heading("#4", text="Loại tài khoản")
        self.accountTable.column("#1", width=30, anchor="center")
        self.accountTable.column("#2", width=50, anchor="center")
        self.accountTable.column("#3", width=50, anchor="center")
        self.accountTable.column("#4", width=200, anchor="center")

        self.accountTable.tag_configure("oddrow", background="#f0f0f0")
        self.accountTable.tag_configure("evenrow", background="#ffffff")

        # Thêm scrollbar dọc
        self.scrollbar = ttk.Scrollbar(
            self.table_frame, orient="vertical", command=self.accountTable.yview)
        self.accountTable.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.accountTable.pack(fill="both", expand=True)

        filename = "src/database/account.json"
        self.data = self.load_data_from_file(filename)

        for index, item in enumerate(self.data):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.accountTable.insert("", END, values=(
                item["tenTaiKhoan"], item["tenNguoiDung"], item["matKhau"], item["loaiTaiKhoan"]), tags=(tag,))

        self.accountTable.bind("<<TreeviewSelect>>", lambda e: row_selection())

    def load_data_from_file(self, filename):
        if not os.path.exists(filename):
            data = []
            admin = NhanVien("admin", "admin", "1234", "admin")

            data.append(admin.to_dict())

            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return data

        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
