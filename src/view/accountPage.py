from tkinter import *
from tkinter import ttk
import json
import os
from src.Model.NhanVien import NhanVien
from tkinter import messagebox as mb
import hashlib


class AccountPage:
    def __init__(self, root):
        self.root = root
        self.root.columnconfigure(0, weight=1)

        self.filename = "src/database/account.json"
        self.dstk = []
        self.data = self.load_data_from_file(self.filename)

        self.dstk = [NhanVien.from_dict(user) for user in self.data]

        self.treeview_bind_id = None

        self.create_frame_account_table()
        self.create_frame_duoi_table()

    def row_selection(self):
        selected_item = self.accountTable.focus()
        if selected_item:
            item_values = self.accountTable.item(selected_item)['values']
            if item_values:
                self.btn_remove.config(state="normal")
                self.btn_edit.config(state="normal")

                self.entry_fullname.config(state="normal")
                self.entry_username.config(state="normal")
                self.entry_password.config(state="normal")
                # cho combobox bấm vào đc, nhưng ko cho người dùng gõ vào
                self.entry_role.config(state="readonly")

                self.entry_fullname.delete(0, END)
                self.entry_username.delete(0, END)
                self.entry_password.delete(0, END)

                self.entry_username.insert(0, item_values[0])
                self.entry_fullname.insert(0, item_values[1])
                self.entry_password.insert(0, item_values[2])
                self.entry_role.set(item_values[3])

                self.entry_fullname.config(state="readonly")
                self.entry_username.config(state="readonly")
                self.entry_password.config(state="readonly")
                self.entry_role.config(state="disabled")

    def create_frame_account_table(self):
        def search():
            for item in self.accountTable.get_children():
                self.accountTable.delete(item)
            nd_timkiem = self.entry_tim_kiem.get().strip()
            self.user_timkiem = []
            for user in self.data:
                if nd_timkiem != "":
                    if str(user["tenTaiKhoan"]) == nd_timkiem or str(user["tenNguoiDung"]) == nd_timkiem or str(user["matKhau"]) == nd_timkiem or str(user["loaiTaiKhoan"]) == nd_timkiem:
                        self.user_timkiem.append(user)

                else:
                    self.user_timkiem.append(user)

            for index, item in enumerate(self.user_timkiem):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.accountTable.insert("", END, values=(
                    item["tenTaiKhoan"], item["tenNguoiDung"], item["matKhau"], item["loaiTaiKhoan"]), tags=(tag,))

        self.frame_search = Frame(self.root)
        # Bám sát lề phải, cách 10px
        self.frame_search.grid(row=0, column=0, sticky="e", padx=50, pady=5)

        # Entry tìm kiếm (nằm bên trái nút tìm kiếm, cách 20px)
        self.entry_tim_kiem = Entry(
            self.frame_search, width=20, font=("Arial", 13))
        self.entry_tim_kiem.grid(row=0, column=0, padx=(0, 20))

        # Button tìm kiếm (bên phải, cách tường phải 10px thông qua padx của frame_search)
        self.btn_search = Button(
            self.frame_search, width=10, text="Tìm kiếm", font=("Arial", 13, "bold"),
            bg="black", fg="white", bd=1, command=search
        )
        self.btn_search.grid(row=0, column=1)

        # Table
        self.table_frame = Frame(self.root)
        self.table_frame.grid(row=1, column=0, sticky="news")

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
        self.accountTable.column("#4", width=50, anchor="center")

        self.accountTable.tag_configure("oddrow", background="#f0f0f0")
        self.accountTable.tag_configure("evenrow", background="#ffffff")

        # Thêm scrollbar dọc
        self.scrollbar = ttk.Scrollbar(
            self.table_frame, orient="vertical", command=self.accountTable.yview)
        self.accountTable.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.accountTable.pack(fill="both", expand=True)

        for index, item in enumerate(self.data):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.accountTable.insert("", END, values=(
                item["tenTaiKhoan"], item["tenNguoiDung"], item["matKhau"], item["loaiTaiKhoan"]), tags=(tag,))

        self.treeview_bind_id = self.accountTable.bind(
            "<<TreeviewSelect>>", lambda e: self.row_selection())

    def create_frame_duoi_table(self):
        self.frame_duoi_table = Frame(self.root)
        self.frame_duoi_table.grid(row=2, column=0, sticky="news", pady=10)

        self.frame_duoi_table.columnconfigure(0, weight=3)
        self.frame_duoi_table.columnconfigure(1, weight=1)
        self.frame_duoi_table.rowconfigure(0, weight=1)

        self.frame_left = Frame(self.frame_duoi_table)
        self.frame_left.grid(row=0, column=0, sticky="nsew")

        self.frame_left.columnconfigure(0, weight=1)
        self.frame_left.rowconfigure(0, weight=0)
        self.frame_left.rowconfigure(1, weight=1)

        self.create_frame_button()
        self.create_entry()

        self.create_frame_hien_thi_so_luong()

    def create_frame_button(self):
        def refresh_table():
            for item in self.accountTable.get_children():
                self.accountTable.delete(item)

            for index, user in enumerate(self.dstk):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.accountTable.insert("", END, values=(
                    user.ten_tai_khoan, user.ten_nguoi_dung, user.mat_khau, user.loai_tai_khoan), tags=(tag,))

                self.lbl_so_luong_taikhoan.config(
                    text=f"Tổng số tài khoản: {len(self.dstk)}")

        def refresh_entry():
            self.entry_username.config(state="normal")
            self.entry_fullname.config(state="normal")
            self.entry_password.config(state="normal")
            self.entry_role.config(state="readonly")

            self.entry_username.delete(0, END)
            self.entry_password.delete(0, END)
            self.entry_fullname.delete(0, END)
            self.entry_role.set("user")

            self.entry_username.config(state="readonly")
            self.entry_password.config(state="readonly")
            self.entry_fullname.config(state="readonly")
            self.entry_role.config(state="disabled")

        def add_user():
            if self.btn_add["text"] == "Thêm":
                self.entry_username.config(state="normal")
                self.entry_fullname.config(state="normal")
                self.entry_password.config(state="normal")

                self.entry_username.delete(0, END)
                self.entry_fullname.delete(0, END)
                self.entry_password.delete(0, END)
                self.entry_role.set("user")

                self.entry_role.config(state="readonly")

                self.btn_add.config(text="Xác nhận")
                self.btn_remove.config(state="disabled")
                self.btn_edit.config(state="disabled")
                self.btn_refresh.config(state="disabled")
                self.btn_cancel.config(state="normal")

                self.treeview_bind_id = self.accountTable.unbind(
                    "<<TreeviewSelect>>")

            elif self.btn_add["text"] == "Xác nhận":
                username = self.entry_username.get()
                password = self.entry_password.get()
                fullname = self.entry_fullname.get()
                role = self.entry_role.get()

                if username == "":
                    mb.showwarning("Lỗi", "Vui lòng nhập username!")
                    return

                for user in self.dstk:
                    if user.ten_tai_khoan == username:
                        mb.showerror(
                            "Lỗi", "Tài khoản này đã tồn tại. Vui lòng nhập tên tài khoản khác!")
                        return

                user = NhanVien(username, fullname, password, role)
                self.dstk.append(user)
                self.save_data(self.filename)
                mb.showinfo(
                    "Thông báo", f"Thêm tài khoản {username} thành công")

                refresh_table()
                refresh_entry()
                self.btn_add.config(text="Thêm")
                self.btn_refresh.config(state="normal")
                self.btn_cancel.config(state="disabled")

                self.accountTable.bind(
                    "<<TreeviewSelect>>", lambda e: self.row_selection())

        def remove_user():
            username = self.entry_username.get()
            answer = mb.askyesno(
                "Thông báo", f"Bạn có chắc chắn muốn xóa tài khoản {username} không?")
            if answer:
                for user in self.dstk:
                    if user.ten_tai_khoan == username:
                        self.dstk.remove(user)
                        self.save_data(self.filename)
                        refresh_table()
                        refresh_entry()
                        mb.showinfo(
                            "Thông báo", f"Đã xóa thành công tài khoản {username}.")

                        self.btn_remove.config(state="disabled")
                        self.btn_edit.config(state="disabled")
                        return
            return

        def edit():
            username = self.entry_username.get()
            if self.btn_edit["text"] == "Sửa":
                self.btn_add.config(state="disabled")
                self.btn_refresh.config(state="disabled")
                self.btn_remove.config(state="disabled")

                self.btn_edit.config(text="Xác nhận")
                self.btn_cancel.config(state="normal")

                self.entry_fullname.config(state="normal")
                self.entry_password.config(state="normal")
                self.entry_role.config(state="readonly")
            else:
                new_fullname = self.entry_fullname.get().strip()
                new_password = self.entry_password.get()
                new_role = self.entry_role.get()
                answer = mb.askyesno(
                    "Thông báo", f"Bạn có chắc muốn đổi thông tin cho tài khoản {username} không?")
                if answer:
                    for user in self.dstk:
                        if user.ten_tai_khoan == username:
                            def hash_password(password):
                                return hashlib.sha256(password.encode("utf-8")).hexdigest()
                            user.ten_nguoi_dung = new_fullname
                            user.mat_khau = hash_password(new_password)
                            user.loai_tai_khoan = new_role

                            self.save_data(self.filename)
                            refresh_table()
                            refresh_entry()
                            mb.showinfo(
                                "Thông báo", f"Đã thay đổi thông tin thành công cho tài khoản {username}")

                            self.btn_add.config(state="normal")
                            self.btn_refresh.config(state="normal")
                            self.btn_edit.config(text="Sửa")
                            self.btn_remove.config(state="disabled")
                            self.btn_edit.config(state="disabled")
                            self.btn_cancel.config(state="disabled")
                            return

        def cancel():
            if self.btn_add["text"] == "Xác nhận":
                answer = mb.askyesno(
                    "Thông báo", "Bạn có chắc muốn hủy thao tác thêm không?")

                if answer:
                    self.btn_add.config(text="Thêm")
                    self.btn_refresh.config(state="normal")
                    self.btn_cancel.config(state="disabled")

                    refresh_entry()

                    self.accountTable.bind(
                        "<<TreeviewSelect>>", lambda e: self.row_selection())
                    return
                return

            elif self.btn_edit["text"] == "Xác nhận":
                answer = mb.askyesno(
                    "Thông báo", "Bạn có chắc muốn hủy thao tác sửa không?")

                if answer:
                    self.btn_edit.config(text="Sửa")
                    self.btn_edit.config(state="disabled")
                    self.btn_add.config(state="normal")
                    self.btn_remove.config(state="disabled")
                    self.btn_refresh.config(state="normal")
                    self.btn_cancel.config(state="disabled")
                    refresh_entry()
                    return
                return

        self.frame_buttons = Frame(self.frame_left)
        self.frame_buttons.grid(row=0, column=0, sticky="news", pady=10)

        self.btn_add = Button(self.frame_buttons, text="Thêm",
                              width=15, height=2, font=("Arial", 13, "bold"), bg="blue", fg="white", command=add_user)
        self.btn_add.grid(row=0, column=0, padx=10)

        self.btn_remove = Button(self.frame_buttons, text="Xóa",
                                 width=15, height=2, font=("Arial", 13, "bold"), bg="#009df7", fg="white", state="disabled", command=remove_user)
        self.btn_remove.grid(row=0, column=1, padx=10)

        self.btn_edit = Button(self.frame_buttons, text="Sửa",
                               width=15, height=2, font=("Arial", 13, "bold"), bg="#00f7f7", fg="white", state="disabled", command=edit)
        self.btn_edit.grid(row=0, column=2, padx=10)

        self.btn_refresh = Button(self.frame_buttons, text="Làm mới", width=15, height=2, font=(
            "Arial", 13, "bold"), bg="#4287f5", fg="white", command=refresh_table)
        self.btn_refresh.grid(row=1, column=0, padx=10, pady=5)

        self.btn_cancel = Button(self.frame_buttons, text="Hủy", width=15, height=2, font=(
            "Arial", 13, "bold"), bg="#f70021", fg="white", state="disabled", command=cancel)
        self.btn_cancel.grid(row=1, column=1, padx=10, pady=5)

    def create_frame_hien_thi_so_luong(self):
        self.frame_sl_taikhoan = Frame(self.frame_duoi_table)
        self.frame_sl_taikhoan.grid(row=0, column=1, sticky="ensw", padx=20)

        tong_so_tk = len(self.data)
        self.lbl_so_luong_taikhoan = Label(
            self.frame_sl_taikhoan, text=f"Tổng số tài khoản: {tong_so_tk}", font=("Arial", 12), anchor="e")
        self.lbl_so_luong_taikhoan.grid(row=0, column=0, sticky="ew")

    def create_entry(self):
        self.frame_entries = Frame(self.frame_left)
        self.frame_entries.grid(row=1, column=0, sticky="news", pady=10)

        # Username
        self.lbl_username = Label(
            self.frame_entries, text="Tên tài khoản: ", width=15, font=("Arial", 13))
        self.lbl_username.grid(row=0, column=0, padx=10, pady=8)
        self.entry_username = Entry(
            self.frame_entries,
            width=20,
            font=("Arial", 13),
            bd=1,
            relief="solid",
            highlightbackground="gray",
            highlightthickness=2,
            highlightcolor="blue",
            state="readonly")  # ko cho người dùng gõ vào
        self.entry_username.grid(row=0, column=1, padx=10, pady=8)

        # Tên người dùng
        self.lbl_fullname = Label(
            self.frame_entries, text="Tên người dùng: ", width=15, font=("Arial", 13))
        self.lbl_fullname.grid(row=1, column=0, padx=10, pady=8)
        self.entry_fullname = Entry(
            self.frame_entries,
            width=20,
            font=("Arial", 13),
            bd=1,
            relief="solid",
            highlightbackground="gray",
            highlightthickness=2,
            highlightcolor="blue",
            state="readonly")
        self.entry_fullname.grid(row=1, column=1, padx=10, pady=8)

        # Mật khẩu
        self.lbl_password = Label(
            self.frame_entries, text="Mật khẩu: ", width=15, font=("Arial", 13))
        self.lbl_password.grid(row=2, column=0, padx=10, pady=8)
        self.entry_password = Entry(
            self.frame_entries,
            width=20,
            font=("Arial", 13),
            bd=1,
            relief="solid",
            highlightbackground="gray",
            highlightthickness=2,
            highlightcolor="blue",
            state="readonly")
        self.entry_password.grid(row=2, column=1, padx=10, pady=8)

        # Role
        self.lbl_role = Label(
            self.frame_entries, text="Loại tài khoản: ", width=15, font=("Arial", 13))
        self.lbl_role.grid(row=3, column=0, padx=10, pady=8)
        self.entry_role = ttk.Combobox(
            self.frame_entries,
            width=20,
            font=("Arial", 13),
            state="disabled",  # ko cho người dùng bấm vào
            values=["admin", "user"])
        self.entry_role.current(1)  # mặc định là user
        self.entry_role.grid(row=3, column=1, padx=10, pady=8)

    def load_data_from_file(self, filename):
        """
        if not os.path.exists(filename):
            self.data = []
            admin = NhanVien("admin", "admin", "1234", "admin")

            self.data.append(admin.to_dict())

            os.makedirs(os.path.dirname(filename), exist_ok=True)

            self.save_data(filename)
            return self.data
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_data(self, filename):
        data = [user.to_dict() for user in self.dstk]
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
