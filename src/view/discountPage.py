from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from src.Model.ChuongTrinhGiamGia import *
from tkcalendar import DateEntry
from datetime import datetime, timedelta
class DiscountPage:
    def __init__(self,root):
        self.root = root
        self.root.configure(bg="#f8f8f8")
        self.root.columnconfigure(0, weight=1)
        self.dsct = DanhSachChuongTrinh()
        #Functions
        def on_enter(event):
            widget = event.widget
            widget.delete(0, END)

        def on_leave(event):
            name = search_box.get()
            if name == "":
                search_box.insert(0, "Tìm kiếm")

        def load_data():
            for item in discountTable.get_children():
                discountTable.delete(item)
            self.dsct.tai_tu_file("src/database/chuongTrinhGiamGiaDB.json")        
            for index, item in enumerate(self.dsct.dsct):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                phanTram = str(item.phanTramGiam)+"%"
                discountTable.insert("", END, values=(item.maGiamGia,phanTram,item.ngayBatDau,item.ngayKetThuc,item.trangThai), tags=(tag,))

        def row_selection():
            selected_item = discountTable.focus()
            if selected_item:
                item_values = discountTable.item(selected_item)['values']
                if item_values:
                    # dieuKien_box.delete(0,END)
                    phanTramGiam_box.delete(0,END)
                    set_readonly_entry(maGiamGia_box,item_values[0])
                    # dieuKien_box.insert(0, item_values[1])
                    phanTramGiam_box.insert(0, item_values[1].replace("%",""))
                    ngayBatDau_box.set_date(item_values[2])
                    ngayKetThuc_box.set_date(item_values[3])
                    btn_taoChuongTrinhGiamGia.config(text="Tạo chương trình giảm giá",command=taoChuongTrinhGiamGia_click)

        def search():
            for item in discountTable.get_children():
                discountTable.delete(item)
            nd_timkiem = search_box.get().strip()
            user_timkiem = []
            for ct in self.dsct.dsct:
                if nd_timkiem != "" and nd_timkiem != "Tìm kiếm":
                    if nd_timkiem in str(ct.maGiamGia):
                        user_timkiem.append(ct)
                else:
                    user_timkiem.append(ct)

            for index, item in enumerate(user_timkiem):
                tag = "evenrow" if index % 2 == 0 else "oddrow"            
                discountTable.insert("", END, values=(item.maGiamGia,item.phanTramGiam,item.ngayBatDau,item.ngayKetThuc,item.trangThai), tags=(tag,))

        def set_readonly_entry(entry_widget, value):
            entry_widget.config(state="normal")
            entry_widget.delete(0, END)
            entry_widget.insert(0, value)
            entry_widget.config(state="readonly")

        def make_label_entry(row, col, label, entry_box, combobox=False, values=None):
            Label(nhapLieu_frame, text=label, bg="#f0f4f8").grid(row=row, column=col, sticky='w')  
            if combobox:
                cb = ttk.Combobox(nhapLieu_frame, values=values or [], state="readonly", width=27)
                cb.grid(row=row, column=col + 1)
                return cb
            else:
                ent = Entry(nhapLieu_frame, width=30, bd=0)
                ent.grid(row=row, column=col + 1)
                return ent          
        
        def clear_box():
            set_readonly_entry(maGiamGia_box,"")
            phanTramGiam_box.delete(0,END)
            ngayBatDau_box.set_date(datetime.now())
            ngayKetThuc_box.set_date(datetime.now())

        def suaChuongTrinhGiamGia_click():
            result = mb.askyesno("Thông báo","Bạn có chắc chắn muốn chỉnh sửa chương trình giảm giá không ?")           
            if result == YES:
                ct = self.dsct.timKiemChuongTrinhTheoMaGiam(maGiamGia_box.get())                
                if ct.trangThai == "Chưa bắt đầu":
                    if not(phanTramGiam_box.get()):
                        mb.showwarning("Cảnh báo","Dữ liệu không được bỏ trống")
                    else:
                        ctEdited = ChuongTrinhGiamGia(maGiamGia_box.get(),
                                                      phanTramGiam_box.get(),
                                                      ngayBatDau_box.get_date().strftime("%d-%m-%Y"),
                                                      ngayKetThuc_box.get_date().strftime("%d-%m-%Y"),
                                                      )
                        result = self.dsct.suaChuongTrinh(ctEdited)
                        if result:
                            load_data()
                            mb.showinfo("Thông báo","Sửa chương trình giảm giá thành công")
                        else:
                            mb.showerror("Lỗi","Sửa chương trình thất bại")
                else:
                    mb.showwarning("Cảnh báo","Chương trình đang bắt đầu hoặc đã kết thúc không thể chỉnh sửa")

        def taoChuongTrinhGiamGia_click():
            clear_box()
            set_readonly_entry(maGiamGia_box,self.dsct.taoMaChuongTrinh())
            # ngay_bat_dau = datetime.strptime(self.dsct.dsct[-1].ngayBatDau, "%d-%m-%Y").date()
            ngay_ket_thuc = datetime.strptime(self.dsct.dsct[-1].ngayKetThuc, "%d-%m-%Y").date()
            ngay_hien_tai = datetime.today().date()
            if isinstance(ngay_ket_thuc, datetime):
                ngay_ket_thuc = ngay_ket_thuc.date()
            if ngay_ket_thuc < ngay_hien_tai:
                ngay_ket_thuc = ngay_hien_tai
            ngayBatDau_box.config(mindate=ngay_ket_thuc+timedelta(days=1))
            ngayBatDau_box.set_date(ngay_ket_thuc+timedelta(days=1))
            ngayKetThuc_box.config(mindate=ngay_ket_thuc+timedelta(days=2))
            ngayKetThuc_box.set_date(ngay_ket_thuc+timedelta(days=2))
            btn_taoChuongTrinhGiamGia.config(text="Xác nhận",command=save)

        def save():
            if not(phanTramGiam_box.get()) == FALSE:
                ct = ChuongTrinhGiamGia(maGiamGia_box.get(),
                                        phanTramGiam_box.get(),
                                        ngayBatDau_box.get_date().strftime("%d-%m-%Y"),
                                        ngayKetThuc_box.get_date().strftime("%d-%m-%Y"),
                                        )
                result = self.dsct.themChuongTrinh(ct)
                if result:                    
                    load_data()
                    mb.showinfo("Thông báo","Thêm chương trình thành công")                    
                else:
                    mb.showerror("Lỗi","Thêm chương trình thất bại")
                    set_readonly_entry(maGiamGia_box,"")
            else:
                mb.showwarning("Cảnh báo","Dữ liệu không được để trống")
                set_readonly_entry(maGiamGia_box,"")
            clear_box()
            btn_taoChuongTrinhGiamGia.config(text="Tạo chương trình giảm giá",command=taoChuongTrinhGiamGia_click)
            if self.dsct.dsct[-1].trangThai != "Đã kết thúc":
                btn_taoChuongTrinhGiamGia.config(state='disabled')

        def xoaChuongTrinhGiamGia_click():
            ct = self.dsct.timKiemChuongTrinhTheoMaGiam(maGiamGia_box.get())
            if ct.trangThai == "Đã kết thúc":
                result = self.dsct.xoaChuongTrinh(maGiamGia_box.get())
                if result:
                    load_data()
                    mb.showinfo("Thông báo","Xóa chương trình giảm giá thành công")
                else:
                    mb.showerror("Lỗi","Xóa chương trình thất bại")
            else:
                mb.showwarning("Cảnh báo","Chương trình chưa kết thúc nên không thể xóa")
        
        def is_number(char):
            return char.isdigit()
        
        def validate_dates(*args):
            start_date = ngayBatDau_box.get_date()
            end_date = ngayKetThuc_box.get_date()
            
            if end_date <= start_date:
                # Tự động đặt lại ngày kết thúc là 1 ngày sau ngày bắt đầu
                new_end_date = start_date + timedelta(days=1)
                ngayKetThuc_box.set_date(new_end_date)

        def validate_spinbox(value_if_allowed, minval=0, maxval=100):
            if value_if_allowed == "":
                return True  # Cho phép xoá toàn bộ tạm thời
            if value_if_allowed.isdigit():
                value = int(value_if_allowed)
                return int(minval) <= value <= int(maxval)
            return False

        def loc_du_lieu():
            for item in discountTable.get_children():
                discountTable.delete(item)            
            user_timkiem = []
            for ct in self.dsct.dsct:                
                if ct.trangThai == filter_cb.get():
                    user_timkiem.append(ct)            

            for index, item in enumerate(user_timkiem):
                tag = "evenrow" if index % 2 == 0 else "oddrow"       
                phanTram = str(item.phanTramGiam)+"%"     
                discountTable.insert("", END, values=(item.maGiamGia,phanTram,item.ngayBatDau,item.ngayKetThuc,item.trangThai), tags=(tag,))

        # Search
        search_frame = Frame(self.root, padx=10, pady=5, bg="#f8f8f8")
        search_frame.grid(row = 0,column=0,sticky="news")

        Label(search_frame, text="Lọc dữ liệu theo trạng thái",bg="#f0f4f8").grid(row=0,column=0, padx=10)
        filter_cb = ttk.Combobox(search_frame,values=["Đã kết thúc","Đang diễn ra","Chưa bắt đầu"],state="readonly")
        filter_cb.grid(row=0,column=1,padx=10)
        filter_cb.bind("<<ComboboxSelected>>",lambda e:loc_du_lieu())

        refresh_photo = PhotoImage(file="src/image/refresh-page-option.png")
        refresh_btn = Button(search_frame,text="Làm mới",image=refresh_photo,command=load_data)
        refresh_btn.image = refresh_photo 
        refresh_btn.grid(row=0,column=2,padx=10)

        search_box = Entry(search_frame,font=("Arial",10))
        search_box.grid(row=0,column=3,padx=(100,0))
        search_box.insert(0, "Tìm kiếm")
        search_box.bind('<FocusIn>', on_enter)
        search_box.bind('<FocusOut>', on_leave)

        search_photo = PhotoImage(file="src/image/search.png")
        search_btn = Button(search_frame,image=search_photo,command=search)
        search_btn.image = search_photo 
        search_btn.grid(row=0,column=4)

        # Table
        table_frame = Frame(self.root, padx=10, bg="#f8f8f8")
        table_frame.grid(row=1, column=0, sticky="news")

        columns = ("#1", "#2", "#3", "#4", "#5")
        discountTable = ttk.Treeview(table_frame, columns=columns, show="headings")
        headings = ["Mã giảm giá","Phần trăm giảm","Ngày bắt đầu","Ngày kết thúc","Trạng thái"]
        for i, h in enumerate(headings, 1):
            discountTable.heading(f"#{i}", text=h, anchor="w")
        widths = [100, 120, 120, 120, 100]
        for i, w in enumerate(widths, 1):            
            discountTable.column(f"#{i}", width=w, anchor="w")

        discountTable.tag_configure("oddrow", background="#f0f0f0")
        discountTable.tag_configure("evenrow", background="#ffffff")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=discountTable.yview)
        discountTable.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        discountTable.pack(fill="both", expand=TRUE)
        load_data()
        discountTable.bind("<<TreeviewSelect>>", lambda e: row_selection())

        # Validate
        vcmd = (self.root.register(is_number), '%S')
        vcmd_spinbox = (self.root.register(validate_spinbox),"%P",0,100)

        # Input Frame
        nhapLieu_frame = LabelFrame(self.root, text="Thông tin chương trình giảm giá", bg="#f0f4f8", font=("Arial", 12, "bold"))
        nhapLieu_frame.grid(row=2, column=0, sticky="news",padx=10,pady=10)

        maGiamGia_box = make_label_entry(0, 2, "Mã giảm giá", Entry)
        maGiamGia_box.config(state="readonly")

        # dieuKien_label = Label(nhapLieu_frame,text="Điều kiện", bg="#f0f4f8").grid(row=0,column=4,sticky="w")

        # dieuKien_frame = Frame(nhapLieu_frame)
        # dieuKien_frame.grid(row=0,column=5)

        # dieuKien_cb = ttk.Combobox(dieuKien_frame,values=[""],state="readonly",width=10)
        # dieuKien_cb.grid(row=1,column=0)

        # dieuKien_box = Entry(dieuKien_frame, width=20, bd=0)
        # dieuKien_box.grid(row=1,column=1)

        phanTramGiam_label = Label(nhapLieu_frame,text="Phần trăm giảm",bg="#f0f4f8").grid(row=0,column=4)
        phanTramGiam_box = Spinbox(nhapLieu_frame,from_=0,to=100,increment=1,width=10,font=("Arial",10),validate='key', validatecommand=vcmd_spinbox)
        phanTramGiam_box.grid(row=0,column=5)

        Label(nhapLieu_frame,text="Ngày bắt đầu",bg="#f0f4f8").grid(row=0,column=6)
        ngayBatDau_box = DateEntry(nhapLieu_frame, width=20, background='darkblue',
                foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        ngayBatDau_box.grid(row=0,column=7)
        ngayBatDau_box.bind("<<DateEntrySelected>>", validate_dates)
        ngayBatDau_box.config(mindate=datetime.today().date())

        Label(nhapLieu_frame,text="Ngày kết thúc",bg="#f0f4f8").grid(row=0,column=8)
        ngayKetThuc_box = DateEntry(nhapLieu_frame, width=20, background='darkblue',
                foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        ngayKetThuc_box.grid(row=0,column=9)
        ngayKetThuc_box.config(mindate=ngayBatDau_box.get_date()+timedelta(days=1))
        ngayKetThuc_box.bind("<<DateEntrySelected>>", validate_dates)

        for widget in nhapLieu_frame.winfo_children():
            widget.grid_configure(padx=8, pady=8)

        button_frame = Frame(self.root, bg="#f0f4f8")
        button_frame.grid(row=3, column=0, sticky="ne")

        btn_taoChuongTrinhGiamGia = Button(button_frame, text="Tạo chương trình giảm giá", width=20, height=2, bg="green", fg="white", font=("Arial", 10), command=taoChuongTrinhGiamGia_click)
        btn_taoChuongTrinhGiamGia.grid(row=0, column=0, padx=10)
        btn_suaChuongTrinhGiamGia = Button(button_frame, text="Sửa chương trình giảm giá", width=20, height=2, bg="blue", fg="white", font=("Arial", 10), command=suaChuongTrinhGiamGia_click)
        btn_suaChuongTrinhGiamGia.grid(row=0, column=1, padx=10)
        btn_xoaChuongTrinhGiamGia = Button(button_frame, text="Xóa chương trình giảm giá", width=20, height=2, bg="red", fg="white", font=("Arial", 10), command=xoaChuongTrinhGiamGia_click)
        btn_xoaChuongTrinhGiamGia.grid(row=0, column=2, padx=10)

        if self.dsct.dsct[-1].trangThai != "Đã kết thúc":
            btn_taoChuongTrinhGiamGia.config(state='disabled')