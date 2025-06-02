from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from src.Model.CuocPhi import *

class FeePage():
    def __init__(self,root):
        self.root = root
        self.root.configure(bg="#f8f8f8")
        self.root.columnconfigure(0, weight=1)
        self.danhSachCuocPhi= DanhSachCuocPhi([])
        #Functions
        def on_enter(event):
            widget = event.widget
            widget.delete(0, END)

        def on_leave(event):
            name = search_box.get()
            if name == "":
                search_box.insert(0, "Tìm kiếm")

        def load_data():
            for item in feeTable.get_children():
                feeTable.delete(item)
            self.danhSachCuocPhi.tai_tu_file("src/database/cuocPhiDB.json")        
            for index, item in enumerate(self.danhSachCuocPhi.dscp):
                tag = "evenrow" if index % 2 == 0 else "oddrow"        
                formatted_value = "{:,} VNĐ".format(int(item.cuocPhi))    
                feeTable.insert("", END, values=(item.thanhPho,formatted_value), tags=(tag,))

        def row_selection():
            selected_item = feeTable.focus()
            if selected_item:
                item_values = feeTable.item(selected_item)['values']
                if item_values:
                    cuocPhi_box.delete(0,END)
                    set_readonly_entry(thanhPho_box,item_values[0])
                    cuoc_phi_str = str(item_values[1]).replace(" VNĐ", "")
                    cuocPhi_box.insert(0, cuoc_phi_str)

        def search():
            for item in feeTable.get_children():
                feeTable.delete(item)
            nd_timkiem = search_box.get().strip()
            user_timkiem = []
            for cuocPhi in self.danhSachCuocPhi.dscp:
                if nd_timkiem != "" and nd_timkiem != "Tìm kiếm":
                    if nd_timkiem in str(cuocPhi.thanhPho):
                        user_timkiem.append(cuocPhi)
                else:
                    user_timkiem.append(cuocPhi)

            for index, item in enumerate(user_timkiem):
                tag = "evenrow" if index % 2 == 0 else "oddrow"            
                feeTable.insert("", END, values=(item.thanhPho,item.cuocPhi), tags=(tag,))

        def set_readonly_entry(entry_widget, value):
            entry_widget.config(state="normal")
            entry_widget.delete(0, END)
            entry_widget.insert(0, value)
            entry_widget.config(state="readonly")

        def make_label_entry(row, col, label, entry_box, combobox=False, values=None):
            Label(nhapLieu_frame, text=label, bg="#f0f4f8").grid(row=row, column=col, sticky='w')            
            ent = Entry(nhapLieu_frame, width=30, bd=0)
            ent.grid(row=row, column=col + 1)
            return ent
        
        def suaCuocPhi_click():
            result = mb.askyesno("Thông báo","Bạn có chắc chắn muốn chỉnh sửa cước phí không ?")           
            if result == YES:
                if cuocPhi_box.get() != "":  
                    cuocPhiSua = CuocPhi(thanhPho_box.get(),cuocPhi_box.get().replace(",",""))
                    if self.danhSachCuocPhi.suaCuocPhi(cuocPhiSua):
                        load_data()
                        mb.showinfo("Thông báo","Chỉnh sửa cước phí thành công")            
                    else:
                        mb.showerror("Lỗi","Chỉnh sửa cước phí thất bại")
                else:
                    mb.showwarning("Cảnh báo","Dữ liệu không được để trống")

        def format_currency(event):
            # Lấy nội dung từ Entry
            value = cuocPhi_box.get()
            
            # Loại bỏ các ký tự không phải số
            value = ''.join(filter(str.isdigit, value))
            
            # Nếu không có số nào thì xóa Entry
            if not value:
                cuocPhi_box.delete(0, END)
                return

            # Format lại chuỗi thành tiền tệ có dấu phẩy
            formatted_value = "{:,}".format(int(value))

            # Cập nhật lại nội dung Entry
            cuocPhi_box.delete(0, END)
            cuocPhi_box.insert(0, formatted_value)

        # Search
        search_frame = Frame(self.root, padx=10, pady=5, bg="#f8f8f8")
        search_frame.grid(row = 0,column=0,sticky="e",rowspan=2)

        search_box = Entry(search_frame,font=("Arial",10))
        search_box.grid(row=0,column=0)
        search_box.insert(0, "Tìm kiếm")
        search_box.bind('<FocusIn>', on_enter)
        search_box.bind('<FocusOut>', on_leave)

        photo = PhotoImage(file="src/image/search.png")
        search_btn = Button(search_frame,image=photo,command=search)
        search_btn.image = photo 
        search_btn.grid(row=0,column=1)

        # Table
        table_frame = Frame(self.root, padx=10, bg="#f8f8f8")
        table_frame.grid(row=1, column=0, sticky="news")

        columns = ("#1", "#2")
        feeTable = ttk.Treeview(table_frame, columns=columns, show="headings")
        headings = ["Thành phố","Cước phí"]
        for i, h in enumerate(headings, 1):
            feeTable.heading(f"#{i}", text=h, anchor="w")
        widths = [150, 100]
        for i, w in enumerate(widths, 1):            
            feeTable.column(f"#{i}", width=w, anchor="w")

        feeTable.tag_configure("oddrow", background="#f0f0f0")
        feeTable.tag_configure("evenrow", background="#ffffff")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=feeTable.yview)
        feeTable.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        feeTable.pack(fill="both", expand=TRUE)
        load_data()
        feeTable.bind("<<TreeviewSelect>>", lambda e: row_selection())

        # Input Frame
        nhapLieu_frame = LabelFrame(self.root, text="Thông tin cước phí", bg="#f0f4f8", font=("Arial", 12, "bold"))
        nhapLieu_frame.grid(row=2, column=0, sticky="news", padx=10, pady=10)

        thanhPho_box = make_label_entry(0, 2, "Thành phố", Entry)
        thanhPho_box.config(state="readonly")
        cuocPhi_box = make_label_entry(0, 4, "Cước phí", Entry)
        cuocPhi_box.bind("<KeyRelease>", format_currency)
        for widget in nhapLieu_frame.winfo_children():
            widget.grid_configure(padx=8, pady=8)

        button_frame = Frame(self.root, bg="#f0f4f8")
        button_frame.grid(row=3, column=0, sticky="ne")

        btn_suaCuocPhi = Button(button_frame, text="Sửa cước phí", width=20, height=2, bg="blue", fg="white", font=("Arial", 10), command=suaCuocPhi_click)
        btn_suaCuocPhi.grid(row=0, column=1, padx=10)