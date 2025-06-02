from tkinter import *
from tkinter import ttk
from src.Model.DonHang import *
from tkinter import messagebox as mb
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import requests
import os
import shutil

token = "5c296349-b9e1-11ef-9083-dadc35c0870d"
apiAddress_district = "https://dev-online-gateway.ghn.vn/shiip/public-api/master-data/district"
apiAddress_ward = "https://dev-online-gateway.ghn.vn/shiip/public-api/master-data/ward"
apiAddress_province = "https://dev-online-gateway.ghn.vn/shiip/public-api/master-data/province"

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#f0f4f8")
        self.root.columnconfigure(0, weight=1)

        danhSachDonHang = DanhSachDonHang()        
        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=('Arial', 10), rowheight=30)
        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))
        style.configure("TLabel", font=('Arial', 20))
        style.configure("TEntry", font=('Arial', 20))
        style.configure("TCombobox", font=('Arial', 20))
        style.configure("TButton", font=('Arial', 20, 'bold'), padding=6)

        # Functions...
        def thanhPhoBox_on_select(event):
            selected_name = thanhPho_box.get()
            selected = next((p for p in province_list if p["ProvinceName"] == selected_name), None)
            if selected:
                district_header = {
                    "Content-Type": "application/json",
                    "Token": token,
                }
                district_param = {"province_id": selected['ProvinceID']}
                district_response = requests.get(apiAddress_district, headers=district_header, params=district_param)
                if district_response.status_code == 200:
                    global districts
                    districts = district_response.json()["data"]
                    district_names = [d["DistrictName"] for d in districts]
                    quan_box.set("")
                    quan_box.config(values=district_names)
                    phuong_box.set("")
                else:
                    print("Lỗi:", district_response.status_code, district_response.text)

        def quanBox_on_select(event):
            selected_name = quan_box.get()
            selected = next((d for d in districts if d["DistrictName"] == selected_name), None)
            if selected:
                ward_header = {
                    "Content-Type": "application/json",
                    "Token": token,
                }
                ward_param = {"district_id": selected['DistrictID']}
                ward_response = requests.get(apiAddress_ward, headers=ward_header, params=ward_param)
                if ward_response.status_code == 200:
                    wards = ward_response.json()["data"]
                    ward_names = [w["WardName"] for w in wards]
                    phuong_box.set("")
                    phuong_box.config(values=ward_names)
                else:
                    print("Lỗi:", ward_response.status_code, ward_response.text)

        def row_selection():
            selected_item = packageTable.focus()
            if selected_item:
                item_values = packageTable.item(selected_item)['values']
                if item_values:
                    tenNguoiNhan_box.delete(0, END)
                    soDienThoai_box.delete(0, END)
                    diaChi_box.delete(0, END)
                    phiVanChuyen_box.delete(0, END)
                    maGiamGia_box.delete(0, END)
                    tongTien_box.delete(0, END)
                    ghiChu_box.delete("1.0",END)
                    set_readonly_entry(maDonHang_box,item_values[0])
                    tenNguoiNhan_box.insert(0, item_values[1])
                    soDienThoai_box.insert(0, "0" + str(item_values[2]))

                    parts = item_values[3].split(",")
                    house_address = parts[0].strip()
                    phuong_part = parts[1].strip()
                    quan_part = parts[2].strip()
                    thanhpho = parts[3].strip()

                    diaChi_box.insert(0, house_address)
                    thanhPho_box.set(thanhpho)
                    thanhPhoBox_on_select(None)
                    quan_box.set(quan_part)
                    quanBox_on_select(None)
                    phuong_box.set(phuong_part)

                    phuongThucThanhToan_box.set(item_values[5])
                    phiVanChuyen_box.insert(0, item_values[6])
                    maGiamGia_box.insert(0, item_values[8])
                    ghiChu_box.insert("1.0",item_values[9])
                    tongTien_box.insert(0, item_values[10])                    
                    trangThai_box.set(item_values[11])
                    
                    #Set ảnh
                    image_path = "src/image/image_donhang" + "/" + item_values[7]
                    select_image.selected_image_path = image_path
                    select_image.selected_image_name = item_values[7]                    
                    img = Image.open(image_path)
                    img = img.resize((100, 100))
                    photo = ImageTk.PhotoImage(img)
                    image_label.config(image=photo)
                    image_label.image = photo

        def taoDonHang_click():
            clear_box()
            set_readonly_entry(maDonHang_box,danhSachDonHang.taoMaDonHang())
            btn_taoDonHang.config(text="Xác nhận",command=save)
        
        def suaDonHang_click():            
            result = mb.askyesno("Thông báo","Bạn có chắc chắn muốn chỉnh sửa đơn hàng không ?")           
            if result == YES:
                if validate_value() and hasattr(select_image, 'selected_image_path'):
                    donHang = DonHang(maDonHang_box.get(),
                                tenNguoiNhan_box.get(),
                                soDienThoai_box.get(),
                                diaChi_box.get() + "," +phuong_box.get() +","+quan_box.get() +","+ thanhPho_box.get(),
                                phuongThucThanhToan_box.get(),
                                select_image.selected_image_name,
                                phiVanChuyen_box.get(),                                
                                maGiamGia_box.get(),
                                ghi_chu=ghiChu_box.get("1.0", END),
                                tong_tien=int(tongTien_box.get()),                                                   
                                trang_thai=trangThai_box.get())            
                    if danhSachDonHang.suaDonHang(donHang):
                        load_data()
                        if not kiem_tra_anh_da_ton_tai(select_image.selected_image_name):
                            luu_anh()                            
                        mb.showinfo("Thông báo","Chỉnh sửa đơn hàng thành công")            
                    else:
                        mb.showerror("Lỗi","Chỉnh sửa đơn hàng thất bại")
                else:
                    mb.showwarning("Cảnh báo","Dữ liệu không được để trống")
        def xoaDonHang_click():
            result = mb.askyesno("Thông báo","Bạn có chắc chắn muốn xóa đơn hàng không ?")
            if result == YES:
                if danhSachDonHang.xoaDonHangTheoMaDon(maDonHang_box.get()):
                    load_data()
                    mb.showinfo("Thông báo","Xóa đơn hàng thành công")            
                else:
                    mb.showerror("Lỗi","Xóa đơn hàng thất bại")

        def is_number(char):
            return char.isdigit()
        
        def clear_box():    
            tenNguoiNhan_box.delete(0, END)
            soDienThoai_box.delete(0, END)
            diaChi_box.delete(0, END)
            phiVanChuyen_box.delete(0, END)
            maGiamGia_box.delete(0, END)
            tongTien_box.delete(0, END)      
            ghiChu_box.delete("1.0",END)              
            quan_box["values"] = []
            quan_box.set("")
            phuong_box["values"] = []
            phuong_box.set("")
            thanhPho_box.set("")
            
        def validate_value():
            if not(tenNguoiNhan_box.get()):
                return False
            if not(soDienThoai_box.get()):
                return False
            if not(diaChi_box.get()):
                return False
            if not(thanhPho_box.get()):
                return False
            if not(quan_box.get()):
                return False
            if not(phuong_box.get()):
                return False
            if not(phuongThucThanhToan_box.get()):
                return False
            if not(trangThai_box.get()):
                return False
            if not(phiVanChuyen_box.get()):
                return False
            if not(tongTien_box.get()):
                return False
            return True
        
        def save():
            if validate_value() and hasattr(select_image, 'selected_image_path'):
                donHang = DonHang(maDonHang_box.get(),
                                tenNguoiNhan_box.get(),
                                soDienThoai_box.get(),
                                diaChi_box.get() + "," +phuong_box.get() +","+quan_box.get() +","+ thanhPho_box.get(),
                                phuongThucThanhToan_box.get(),
                                select_image.selected_image_name,
                                phiVanChuyen_box.get(),
                                maGiamGia_box.get(),                                
                                ghi_chu=ghiChu_box.get("1.0", END),
                                tong_tien=int(tongTien_box.get()),                                        
                                trang_thai=trangThai_box.get())
                result = danhSachDonHang.themDonHang(donHang)
                if result:
                    if not kiem_tra_anh_da_ton_tai(select_image.selected_image_name):
                        luu_anh()
                    mb.showinfo("Thông báo","Thêm đơn hàng thành công")                    
                else:
                    mb.showerror("Lỗi","Thêm đơn hàng thất bại")
                    set_readonly_entry(maDonHang_box,"")
            else:
                mb.showwarning("Cảnh báo","Dữ liệu không được để trống")
                set_readonly_entry(maDonHang_box,"")
            clear_box()
            btn_taoDonHang.config(text="Tạo đơn hàng",command=taoDonHang_click)

        def set_readonly_entry(entry_widget, value):
            entry_widget.config(state="normal")
            entry_widget.delete(0, END)
            entry_widget.insert(0, value)
            entry_widget.config(state="readonly")

        def load_data():
            for item in packageTable.get_children():
                packageTable.delete(item)
            danhSachDonHang.tai_tu_file("src/database/donHangDB.json")        
            for index, item in enumerate(danhSachDonHang.danhSachDonHang):
                tag = "evenrow" if index % 2 == 0 else "oddrow"            
                packageTable.insert("", END, values=(item.ma_don_hang, item.tenNguoiNhan, item.soDienThoai, item.dia_chi_giao,item.ngay_dat,
                                                        item.phuong_thuc_thanh_toan, item.phi_van_chuyen,item.hinh_anh, item.ma_giam_gia, item.ghi_chu,
                                                        item.tong_tien, item.trang_thai), tags=(tag,))

        def select_image():
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")]
            )
            if file_path:
                image_name = os.path.basename(file_path)
                img = Image.open(file_path)
                img = img.resize((100, 100))
                photo = ImageTk.PhotoImage(img)
                image_label.config(image=photo)
                image_label.image = photo

                select_image.selected_image_path = file_path
                select_image.selected_image_name = image_name
                print(select_image.selected_image_path)
                print(select_image.selected_image_name)

        def make_label_entry(row, col, label, entry_box, combobox=False, values=None):
            Label(nhapLieu_frame, text=label, bg="#f0f4f8").grid(row=row, column=col, sticky='w')
            if combobox:
                cb = ttk.Combobox(nhapLieu_frame, values=values or [], state="readonly", width=27)
                cb.grid(row=row, column=col + 1)
                return cb
            else:
                ent = Entry(nhapLieu_frame, width=30, bd=0, validate='key', validatecommand=vcmd if "Số" in label or "tiền" in label  or "Phí" in label else None)
                ent.grid(row=row, column=col + 1)
                return ent

        def kiem_tra_anh_da_ton_tai(ten_anh):
            duong_dan = os.path.join("src\\image\\image_donhang", ten_anh)
            return os.path.exists(duong_dan)

        def luu_anh():
            image_folder = os.path.join("src", "image", "image_donhang")
            os.makedirs(image_folder, exist_ok=True)  # Tạo folder nếu chưa có
            save_path = os.path.join(image_folder, select_image.selected_image_name)
            try:
                shutil.copy(select_image.selected_image_path, save_path)
                print(f"Đã lưu ảnh vào: {save_path}")
            except Exception as e:
                print(f"Lỗi khi lưu ảnh: {e}")

        # Table
        table_frame = Frame(self.root, padx=10, pady=5, bg="#f8f8f8")
        table_frame.grid(row=0, column=0, sticky="news")

        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#12")
        packageTable = ttk.Treeview(table_frame, columns=columns, show="headings")
        headings = ["Mã đơn hàng", "Tên người nhận", "SĐT", "Địa chỉ","Ngày đặt", "PT Thanh toán", "Phí VC","", "Mã giảm giá","", "Tổng tiền", "Trạng thái"]
        for i, h in enumerate(headings, 1):
            packageTable.heading(f"#{i}", text=h, anchor="w")

        widths = [100, 150, 100, 250, 100 ,150, 120, 0, 120, 0, 120, 120]
        for i, w in enumerate(widths, 1):
            if w == 0:
                packageTable.column(f"#{i}", width=w,stretch=False) 
            else:   
                packageTable.column(f"#{i}", width=w, anchor="w")

        packageTable.tag_configure("oddrow", background="#f0f0f0")
        packageTable.tag_configure("evenrow", background="#ffffff")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=packageTable.yview)
        packageTable.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        packageTable.pack(fill="both", expand=TRUE)

        load_data()        
        packageTable.bind("<<TreeviewSelect>>", lambda e: row_selection())

        # Validate
        vcmd = (self.root.register(is_number), '%S')

        # Input Frame
        nhapLieu_frame = LabelFrame(self.root, text="Thông tin đơn hàng", bg="#f0f4f8", font=("Arial", 12, "bold"))
        nhapLieu_frame.grid(row=1, column=0, sticky="news", padx=10, pady=5)

        maDonHang_box = make_label_entry(0, 0, "Mã đơn hàng", Entry)
        maDonHang_box.config(state="readonly")
        tenNguoiNhan_box = make_label_entry(0, 2, "Tên người nhận", Entry)
        soDienThoai_box = make_label_entry(0, 4, "Số điện thoại", Entry)
        diaChi_box = make_label_entry(0, 6, "Địa chỉ", Entry)

        headers = {"Content-Type": "application/json", "Token": token}
        province_names = []
        response = requests.get(apiAddress_province, headers=headers)
        if response.status_code == 200:
            province_list = response.json().get("data", [])
            province_names = [p["ProvinceName"] for p in province_list if p["ProvinceName"] not in ["Ngoc test", "Test"]]
        else:
            print("Lỗi khi gọi GHN API:", response.status_code, response.text)

        thanhPho_box = make_label_entry(1, 0, "Thành phố", Entry, combobox=True, values=province_names)
        thanhPho_box.bind("<<ComboboxSelected>>", thanhPhoBox_on_select)

        quan_box = make_label_entry(1, 2, "Quận", Entry, combobox=True)
        quan_box.bind("<<ComboboxSelected>>", quanBox_on_select)

        phuong_box = make_label_entry(1, 4, "Phường", Entry, combobox=True)

        phuongThucThanhToan_box = make_label_entry(1, 6, "Phương thức thanh toán", Entry, combobox=True, values=["Tiền mặt", "Chuyển khoản"])
        phiVanChuyen_box = make_label_entry(2, 0, "Phí vận chuyển", Entry)
        maGiamGia_box = make_label_entry(2, 2, "Mã giảm giá", Entry)
        tongTien_box = make_label_entry(2, 4, "Tổng tiền", Entry)
        trangThai_box = make_label_entry(2, 6, "Trạng thái", Entry, combobox=True, values=["Đã giao", "Đang giao"])

        ghiChu_label = Label(nhapLieu_frame,text="Ghi chú")
        ghiChu_label.grid(row=3,column=0,sticky='w')

        ghiChu_box = Text(nhapLieu_frame,height=5,width=23)
        ghiChu_box.grid(row=3,column=1)

        # Nút để chọn ảnh
        btn = Button(nhapLieu_frame, text="Chọn ảnh", command=select_image)
        btn.grid(row=3,column=2)

        # Label để hiển thị ảnh
        image_label = Label(nhapLieu_frame)
        image_label.grid(row=3,column=3)

        for widget in nhapLieu_frame.winfo_children():
            widget.grid_configure(padx=8, pady=8)

        button_frame = Frame(self.root, bg="#f0f4f8")
        button_frame.grid(row=4, column=0, sticky="se")

        btn_taoDonHang = Button(button_frame, text="Tạo đơn hàng", width=20, height=2, bg="green", fg="white", font=("Arial", 10), command=taoDonHang_click)
        btn_taoDonHang.grid(row=0, column=0, padx=5)
        btn_suaDonHang = Button(button_frame, text="Sửa đơn hàng", width=20, height=2, bg="blue", fg="white", font=("Arial", 10), command=suaDonHang_click)
        btn_suaDonHang.grid(row=0, column=1, padx=5)
        btn_xoaDonHang = Button(button_frame, text="Xóa đơn hàng", width=20, height=2, bg="red", fg="white", font=("Arial", 10), command=xoaDonHang_click)
        btn_xoaDonHang.grid(row=0, column=2, padx=5)