from tkinter import *
from tkinter import ttk
from src.Model.DonHang import *
from src.Model.CuocPhi import *
from src.Model.ChuongTrinhGiamGia import *
from src.Model.SanPham import *
from tkinter import messagebox as mb
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import requests
import os
import shutil

token = "f6676c9d-b9e2-11ef-9128-eee9c4aedda3"
apiAddress_district = "https://online-gateway.ghn.vn/shiip/public-api/master-data/district"
apiAddress_ward = "https://online-gateway.ghn.vn/shiip/public-api/master-data/ward?district_id"
apiAddress_province = "https://online-gateway.ghn.vn/shiip/public-api/master-data/province"

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#f8f8f8")
        self.root.columnconfigure(0, weight=1)

        danhSachDonHang = DanhSachDonHang()
        danhSachCuocPhi = DanhSachCuocPhi()
        self.danhSachSanPham = DanhSachSanPham([])
        danhSachCuocPhi.tai_tu_file("src/database/cuocPhiDB.json")
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
            cuocPhi = danhSachCuocPhi.timKiemCuocPhi(selected_name)
            set_readonly_entry(phiVanChuyen_box,"{:,}".format(int(cuocPhi.cuocPhi)))
            set_readonly_entry(tongTien_box,"{:,}".format(int(cuocPhi.cuocPhi)))
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
                ward_response = requests.get(apiAddress_ward, headers=ward_header, json=ward_param)
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
                    tenNguoiGui_box.delete(0,END)
                    soDienThoaiNguoiGui_box.delete(0,END)
                    diaChi_box.delete(0, END)
                    phiVanChuyen_box.delete(0, END)
                    trongLuong_box.delete(0,END)
                    tongTien_box.delete(0, END)
                    ghiChu_box.delete("1.0",END)
                    set_readonly_entry(maDonHang_box,item_values[0])
                    tenNguoiNhan_box.insert(0, item_values[1])
                    soDienThoai_box.insert(0, "0" + str(item_values[2]))
                    tenNguoiGui_box.insert(0, item_values[3])
                    soDienThoaiNguoiGui_box.insert(0, "0" + str(item_values[4]))

                    parts = item_values[5].split(",")
                    house_address = parts[0].strip()
                    phuong_part = parts[1].strip()
                    quan_part = parts[2].strip()
                    thanhpho = parts[3].strip()

                    diaChi_box.insert(0, house_address)
                    thanhPho_box.set(thanhpho)
                    #thanhPhoBox_on_select(None)
                    quan_box.set(quan_part)
                    #quanBox_on_select(None)
                    phuong_box.set(phuong_part)

                    phuongThucThanhToan_box.set(item_values[7])
                    set_readonly_entry(phiVanChuyen_box,str(item_values[8]).replace(" VNĐ",""))

                    chu = ''.join(c for c in item_values[9]if c.isalpha())
                    so = ''.join(c for c in item_values[9] if c.isdigit())
                    trongLuong_box.insert(0,so)
                    donViTinh_cb.set(chu)
                    for dh in danhSachDonHang.danhSachDonHang:
                        if dh.ma_don_hang == item_values[0]:
                            self.danhSachSanPham = dh.danhSachSanPham
                    ghiChu_box.insert("1.0",item_values[10])
                    set_readonly_entry(tongTien_box,str(item_values[11]).replace(" VNĐ",""))
                    trangThai_box.set(item_values[12])
                    btn_taoDonHang.config(text="Tạo đơn hàng",command=taoDonHang_click)


        def row_selection_sanPham_table():            
            selected_item = sanPham_table.focus()
            if selected_item:
                item_values = sanPham_table.item(selected_item)['values']
                if item_values:
                    set_readonly_entry(maSanPham_box,item_values[0])
                    tenSanPham_box.delete(0,END)
                    tenSanPham_box.insert(0,item_values[1])

                    soLuong_box.delete(0,END)
                    soLuong_box.insert(0,item_values[2])

                    file_path = "E:\\Python\\Tkinter\\Project\\1\\src\\image\\image_donhang\\"+item_values[3]
                    img = Image.open(file_path)
                    img = img.resize((100, 100))
                    photo = ImageTk.PhotoImage(img)
                    image_label_sanPham.config(image=photo)
                    image_label_sanPham.image = photo

                    select_image.selected_image_path = file_path
                    select_image.selected_image_name = item_values[3]

                    btn_taoSanPham.config(text="Tạo sản phẩm",command=themSanPham)

        def taoDonHang_click():
            clear_box()
            set_readonly_entry(maDonHang_box,danhSachDonHang.taoMaDonHang())
            btn_taoDonHang.config(text="Xác nhận",command=save)
        
        def suaDonHang_click():
            result = mb.askyesno("Thông báo","Bạn có chắc chắn muốn chỉnh sửa đơn hàng không ?")           
            if result == YES:
                donHangEdited = danhSachDonHang.timKiemDonHangTheoMaDon(maDonHang_box.get())
                if donHangEdited != None:
                    if donHangEdited.trang_thai == "Đã giao":
                        mb.showwarning("Cảnh báo","Đơn hàng đã giao không thể sửa")
                        return
                    if validate_value():
                        donHang = DonHang(maDonHang_box.get(),
                                    tenNguoiNhan_box.get(),
                                    soDienThoai_box.get(),
                                    tenNguoiGui_box.get(),
                                    soDienThoaiNguoiGui_box.get(),
                                    diaChi_box.get() + "," +phuong_box.get() +","+quan_box.get() +","+ thanhPho_box.get(),
                                    phuongThucThanhToan_box.get(),
                                    self.danhSachSanPham.dssp,
                                    trongLuong_box.get()+""+donViTinh_cb.get(),
                                    phiVanChuyen_box.get().replace(",",""),                                
                                    ghi_chu=ghiChu_box.get("1.0", END).strip(),
                                    tong_tien=int(tongTien_box.get().replace(",","")),                                                   
                                    trang_thai=trangThai_box.get())            
                        if danhSachDonHang.suaDonHang(donHang):
                            load_data()                          
                            mb.showinfo("Thông báo","Chỉnh sửa đơn hàng thành công")            
                        else:
                            mb.showerror("Lỗi","Chỉnh sửa đơn hàng thất bại")
                    else:
                        mb.showwarning("Cảnh báo","Dữ liệu không được để trống")
                else:
                    mb.showerror("Lỗi","Không tìm thấy đơn hàng")

        def xoaDonHang_click():
            result = mb.askyesno("Thông báo","Bạn có chắc chắn muốn xóa đơn hàng không ?")
            if result == YES:
                dh_xoa = danhSachDonHang.timKiemDonHangTheoMaDon(maDonHang_box.get())
                if dh_xoa != None:
                    if dh_xoa.trang_thai == "Đã giao":
                        if danhSachDonHang.xoaDonHangTheoMaDon(maDonHang_box.get()):
                            load_data()
                            mb.showinfo("Thông báo","Xóa đơn hàng thành công")            
                        else:
                            mb.showerror("Lỗi","Xóa đơn hàng thất bại")
                    else:
                        mb.showwarning("Cảnh báo","Đơn hàng chưa được giao, xóa thất bại")
                else:
                    mb.showerror("Lỗi","Không tìm thấy đơn hàng")

        def is_number(char):
            return char.isdigit()
        
        def clear_box():            
            tenNguoiNhan_box.delete(0, END)
            soDienThoai_box.delete(0, END)
            tenNguoiGui_box.delete(0,END)
            self.danhSachSanPham = DanhSachSanPham([])
            soDienThoaiNguoiGui_box.delete(0,END)
            diaChi_box.delete(0, END)
            set_readonly_entry(phiVanChuyen_box,"")
            set_readonly_entry(tongTien_box,"")
            trongLuong_box.delete(0,END)   
            ghiChu_box.delete("1.0",END)              
            quan_box["values"] = []
            quan_box.set("")
            phuong_box["values"] = []
            phuong_box.set("")
            thanhPho_box.set("")
            trangThai_box.set("")
            phuongThucThanhToan_box.set("")
            
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
            if len(self.danhSachSanPham.dssp) == 0:
                return False
            if not(trangThai_box.get()):
                return False
            if not(trongLuong_box.get()):
                return False
            if not(phiVanChuyen_box.get()):
                return False
            if not(tongTien_box.get()):
                return False
            return True
        
        def save():
            if validate_value():
                donHang = DonHang(maDonHang_box.get(),
                                tenNguoiNhan_box.get(),
                                soDienThoai_box.get(),
                                tenNguoiGui_box.get(),
                                soDienThoaiNguoiGui_box.get(),
                                diaChi_box.get() + "," +phuong_box.get() +","+quan_box.get() +","+ thanhPho_box.get(),
                                phuongThucThanhToan_box.get(),
                                self.danhSachSanPham.dssp,
                                trongLuong_box.get()+""+donViTinh_cb.get(),
                                phiVanChuyen_box.get().replace(",",""),
                                ghi_chu=ghiChu_box.get("1.0", END).strip(),
                                tong_tien=int(tongTien_box.get().replace(",","")),                                        
                                trang_thai=trangThai_box.get())
                result = danhSachDonHang.themDonHang(donHang)
                if result:
                    load_data()
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
                phiVanChuyen = "{:,} VNĐ".format(int(item.phi_van_chuyen))
                tongTien = "{:,} VNĐ".format(int(item.tong_tien))
                packageTable.insert("", END, values=(item.ma_don_hang, item.tenNguoiNhan, item.soDienThoai, item.tenNguoiGui,item.soDienThoaiNguoiGui,item.dia_chi_giao,item.ngay_dat,
                                                        item.phuong_thuc_thanh_toan, phiVanChuyen,item.trong_luong, item.ghi_chu,
                                                        tongTien, item.trang_thai,), tags=(tag,))

        def load_data_sanPham():
            for item in sanPham_table.get_children():
                sanPham_table.delete(item)    
            for index, item in enumerate(self.danhSachSanPham.dssp):
                tag = "evenrow" if index % 2 == 0 else "oddrow"   
                sanPham_table.insert("", END, values=(item.ma_san_pham,item.ten_san_pham,item.so_luong,item.hinh_anh), tags=(tag,))

        def select_image():
            file_path = filedialog.askopenfilename(
                title="Chọn hình ảnh",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")],
                parent=themSanPham_win
            )
            if file_path:
                image_name = os.path.basename(file_path)
                img = Image.open(file_path)
                img = img.resize((100, 100))
                photo = ImageTk.PhotoImage(img)
                image_label_sanPham.config(image=photo)
                image_label_sanPham.image = photo

                select_image.selected_image_path = file_path
                select_image.selected_image_name = image_name

        def make_label_entry(row, col, label, entry_box, combobox=False, values=None):
            Label(nhapLieu_frame, text=label, bg="#f0f4f8").grid(row=row, column=col, sticky='w')
            if combobox:
                cb = ttk.Combobox(nhapLieu_frame, values=values or [], state="readonly", width=27)
                cb.grid(row=row, column=col + 1)
                return cb
            else:
                ent = Entry(nhapLieu_frame, width=30, bd=0, validate='key', validatecommand=vcmd if "Số" in label or "Trọng" in label else None)
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

        def on_enter(event):
            widget = event.widget
            widget.delete(0, END)

        def on_leave(event):
            name = search_box.get()
            if name == "":
                search_box.insert(0, "Tìm kiếm")

        def search():
            for item in packageTable.get_children():
                packageTable.delete(item)
            nd_timkiem = search_box.get().strip()
            user_timkiem = []
            for donHang in danhSachDonHang.danhSachDonHang:
                if nd_timkiem != "" and nd_timkiem != "Tìm kiếm":
                    if str(donHang.ma_don_hang) == nd_timkiem or str(donHang.tenNguoiNhan) == nd_timkiem or str(donHang.soDienThoai) == nd_timkiem:
                        user_timkiem.append(donHang)
                else:
                    user_timkiem.append(donHang)

            for index, item in enumerate(user_timkiem):
                tag = "evenrow" if index % 2 == 0 else "oddrow"            
                phiVanChuyen = "{:,} VNĐ".format(int(item.phi_van_chuyen))
                tongTien = "{:,} VNĐ".format(int(item.tong_tien))
                packageTable.insert("", END, values=(item.ma_don_hang, item.tenNguoiNhan, item.soDienThoai, item.tenNguoiGui,
                                                        item.soDienThoaiNguoiGui,item.dia_chi_giao,item.ngay_dat,
                                                        item.phuong_thuc_thanh_toan, phiVanChuyen,item.trong_luong, item.ghi_chu,
                                                        tongTien, item.trang_thai,), tags=(tag,))
        
        def on_weight_input():
            try:                
                value = float(trongLuong_box.get())
                if value >= 1000 and donViTinh_cb.get() == "gram":
                    # Tự động chuyển sang kg
                    donViTinh_cb.set("kg")
                    trongLuong_box.delete(0, END)
                    trongLuong_box.insert(0, str(int(value / 1000)))  # rút gọn còn 1.x
                elif donViTinh_cb.get() != "kg":
                    donViTinh_cb.set("gram")                
                tinh_tong_tien()
            except ValueError:
                pass

        def tinh_tong_tien(*args):
            try:
                weight_str = trongLuong_box.get()
                if not weight_str:
                    # tongTien_box.config(state="normal")
                    # tongTien_box.delete(0, END)
                    # tongTien_box.config(state="readonly")
                    return

                weight = float(weight_str)
                unit = donViTinh_cb.get()

                # Quy đổi sang kg
                if unit == "gram":
                    weight_kg = weight / 1000
                else:
                    weight_kg = weight

                dsct = DanhSachChuongTrinh([])
                dsct.tai_tu_file("src/database/chuongTrinhGiamGiaDB.json")
                ct = dsct.timChuongTrinhDangDienRa()

                # Tính tổng tiền
                if weight_kg <=20:
                    tong_tien = int(phiVanChuyen_box.get().replace(",","")) + 15000
                else:
                    tong_tien = int(phiVanChuyen_box.get().replace(",","")) + 50000

                if ct is not None:
                    tong_tien = int(tong_tien * (100-ct.phanTramGiam) / 100)
                
                # Cập nhật vào box
                set_readonly_entry(tongTien_box,f"{tong_tien:,}")

            except ValueError:
                pass  # bỏ qua nếu người dùng nhập chưa hợp lệ
        
        def loc_du_lieu():
            for item in packageTable.get_children():
                packageTable.delete(item)            
            user_timkiem = []
            for donHang in danhSachDonHang.danhSachDonHang:                
                if donHang.trang_thai == filter_cb.get():
                    user_timkiem.append(donHang)            

            for index, item in enumerate(user_timkiem):
                tag = "evenrow" if index % 2 == 0 else "oddrow"            
                phiVanChuyen = "{:,} VNĐ".format(int(item.phi_van_chuyen))
                tongTien = "{:,} VNĐ".format(int(item.tong_tien))
                packageTable.insert("", END, values=(item.ma_don_hang, item.tenNguoiNhan, item.soDienThoai, item.tenNguoiGui,
                                                        item.soDienThoaiNguoiGui,item.dia_chi_giao,item.ngay_dat,
                                                        item.phuong_thuc_thanh_toan, phiVanChuyen,item.trong_luong, item.ghi_chu,
                                                        tongTien, item.trang_thai,), tags=(tag,))

        def themSanPham():
            clear_themSanPham_boxes()            
            set_readonly_entry(maSanPham_box,self.danhSachSanPham.taoMaSanPham())
            btn_taoSanPham.config(text="Xác nhận",command=save_themSanPham)

        def validate_sanPham_value():
            if not(tenSanPham_box.get()):
                return False
            if not(soLuong_box.get()):
                return False
            if not(select_image.selected_image_path):
                return False
            return True
        
        def save_themSanPham():
            if validate_sanPham_value():
                sanPham = SanPham(
                    maSanPham_box.get(),
                    tenSanPham_box.get(),
                    soLuong_box.get(),
                    select_image.selected_image_name
                )
                result = self.danhSachSanPham.themSanPham(sanPham)
                if result:
                    if not kiem_tra_anh_da_ton_tai(select_image.selected_image_name):
                        luu_anh()
                    load_data_sanPham()
                    mb.showinfo("Thông báo","Thêm sản phẩm thành công",parent=themSanPham_win)                    
                else:
                    mb.showerror("Lỗi","Thêm sản phẩm thất bại",parent=themSanPham_win)
                    set_readonly_entry(maSanPham_box,"")
            else:
                mb.showwarning("Cảnh báo","Dữ liệu không được để trống",parent=themSanPham_win)
                set_readonly_entry(maSanPham_box,"")
            clear_themSanPham_boxes()
            btn_taoSanPham.config(text="Tạo sản phẩm",command=themSanPham)
                        
        def suaSanPham():
            result = mb.askyesno("Thông báo","Bạn có chắc chắn muốn chỉnh sửa sản phẩm không ?",parent=themSanPham_win)           
            if result == YES:                
                if validate_sanPham_value():
                    sanPham = SanPham(
                        maSanPham_box.get(),
                        tenSanPham_box.get(),
                        soLuong_box.get(),
                        select_image.selected_image_name
                    )            
                    if self.danhSachSanPham.suaSanPham(sanPham):
                        load_data_sanPham()
                        if not kiem_tra_anh_da_ton_tai(select_image.selected_image_name):
                            luu_anh()                            
                        mb.showinfo("Thông báo","Chỉnh sửa sản phẩm thành công",parent=themSanPham_win)            
                    else:
                        mb.showerror("Lỗi","Chỉnh sửa sản phẩm thất bại",parent=themSanPham_win)
                else:
                    mb.showwarning("Cảnh báo","Dữ liệu không được để trống",parent=themSanPham_win)
            
        def xoaSanPham():        
            result = mb.askyesno("Thông báo","Bạn có chắc chắn muốn xóa sản phẩm không ?",parent=themSanPham_win)
            if result == YES:
                if self.danhSachSanPham.xoaSanPham(maSanPham_box.get()):
                    load_data_sanPham()
                    mb.showinfo("Thông báo","Xóa sản phẩm thành công",parent=themSanPham_win)            
                else:
                    mb.showerror("Lỗi","Xóa sản phẩm thất bại",parent=themSanPham_win)

        def clear_themSanPham_boxes():
            set_readonly_entry(maSanPham_box,"")
            tenSanPham_box.delete(0,END)
            soLuong_box.delete(0,END)
            image_label_sanPham.config(image=None)
            image_label_sanPham.image = None
            select_image.selected_image_path = ""
            select_image.selected_image_name = ""

        def themSanPham_window():            
            global themSanPham_win
            themSanPham_win = Toplevel()
            themSanPham_win.configure(bg="#f8f8f8")
            themSanPham_win.columnconfigure(0, weight=1)
            themSanPham_win.title("Thêm sản phẩm")

            WIDTH = 900
            HEIGHT = 600

            screen_width = themSanPham_win.winfo_screenwidth()
            screen_height = themSanPham_win.winfo_screenheight()

            x = int((screen_width - WIDTH) / 2)
            y = int((screen_height - HEIGHT) / 2)
            themSanPham_win.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
            themSanPham_win.configure(bg="#fff")
            themSanPham_win.resizable(False, False)

            sanPham_table_frame = Frame(themSanPham_win, padx=10, pady=5, bg="#f8f8f8")
            sanPham_table_frame.grid(row=0, column=0, sticky="news")
            columns = ("#1", "#2", "#3", "#4")
            global sanPham_table
            sanPham_table = ttk.Treeview(sanPham_table_frame, columns=columns, show="headings")
            headings = ["Mã sản phẩm","Tên sản phẩm","Số lượng","Hình ảnh"]
            for i, h in enumerate(headings, 1):
                sanPham_table.heading(f"#{i}", text=h, anchor="w")

            widths = [100, 150, 100, 150]
            for i, w in enumerate(widths, 1):
                if w == 0:
                    sanPham_table.column(f"#{i}", width=w,stretch=False) 
                else:   
                    sanPham_table.column(f"#{i}", width=w, anchor="w")

            sanPham_table.tag_configure("oddrow", background="#f0f0f0")
            sanPham_table.tag_configure("evenrow", background="#ffffff")
            sanPham_scrollbar = ttk.Scrollbar(sanPham_table_frame, orient="vertical", command=sanPham_table.yview)
            sanPham_table.configure(yscroll=sanPham_scrollbar.set)
            sanPham_scrollbar.pack(side="right", fill="y")
            sanPham_table.pack(fill="both", expand=TRUE)
            load_data_sanPham()
            sanPham_table.bind("<<TreeviewSelect>>", lambda e: row_selection_sanPham_table())

            themSanPham_frame = LabelFrame(themSanPham_win,text="Thông tin sản phẩm" ,bg="#f0f4f8", font=("Arial", 12, "bold"))
            themSanPham_frame.grid(row=1,column=0,padx=10,pady=10,sticky="news")

            maSanPham_label = Label(themSanPham_frame, text="Mã sản phẩm", bg="#f0f4f8").grid(row=0, column=0, sticky='w')
            global maSanPham_box
            maSanPham_box = Entry(themSanPham_frame, width=30, bd=0)
            maSanPham_box.grid(row=0,column=1)
            maSanPham_box.config(state="readonly")

            tenSanPham_label = Label(themSanPham_frame, text="Tên sản phẩm", bg="#f0f4f8").grid(row=0, column=2, sticky='w')
            global tenSanPham_box
            tenSanPham_box = Entry(themSanPham_frame, width=30, bd=0)
            tenSanPham_box.grid(row=0,column=3)

            soLuong_label = Label(themSanPham_frame, text="Số lượng", bg="#f0f4f8").grid(row=1, column=0, sticky='w')
            global soLuong_box
            soLuong_box = Entry(themSanPham_frame, width=30, bd=0,validate="key",validatecommand=vcmd)
            soLuong_box.grid(row=1,column=1)

             # Nút để chọn ảnh
            btn_themAnhSanPham = Button(themSanPham_frame, text="Chọn ảnh", command=select_image)
            btn_themAnhSanPham.grid(row=1,column=2)

            # Label để hiển thị ảnh
            global image_label_sanPham
            image_label_sanPham = Label(themSanPham_frame)
            image_label_sanPham.grid(row=1,column=3)

            for widget in themSanPham_frame.winfo_children():
                widget.grid_configure(padx=8, pady=8)

            themSanPham_btn = Frame(themSanPham_win,bg="#f0f4f8")
            themSanPham_btn.grid(row=2,column=0,padx=10,pady=10,sticky="se")
            global btn_taoSanPham
            btn_taoSanPham = Button(themSanPham_btn, text="Tạo sản phẩm", width=20, height=2, bg="green", fg="white", font=("Arial", 10), command=themSanPham)
            btn_taoSanPham.grid(row=0, column=0, padx=5)
            btn_suaSanPham = Button(themSanPham_btn, text="Sửa sản phẩm", width=20, height=2, bg="blue", fg="white", font=("Arial", 10), command=suaSanPham)
            btn_suaSanPham.grid(row=0, column=1, padx=5)
            btn_xoaSanPham = Button(themSanPham_btn, text="Xóa sản phẩm", width=20, height=2, bg="red", fg="white", font=("Arial", 10), command=xoaSanPham)
            btn_xoaSanPham.grid(row=0, column=2, padx=5)

            dh = danhSachDonHang.timKiemDonHangTheoMaDon(maDonHang_box.get())
            if dh != None:
                if dh.trang_thai == "Đã giao":
                    btn_taoSanPham.config(state='disabled')
                    btn_suaSanPham.config(state='disabled')
                    btn_xoaSanPham.config(state='disabled')

            themSanPham_win.grab_set()
            root.wait_window(themSanPham_win)  
            

        # Search
        search_frame = Frame(self.root, padx=10, pady=5, bg="#f8f8f8")
        search_frame.grid(row = 0,column=0,sticky="news")

        Label(search_frame, text="Lọc dữ liệu theo trạng thái",bg="#f0f4f8").grid(row=0,column=0, padx=10)
        filter_cb = ttk.Combobox(search_frame,values=["Đang giao","Đã giao"],state="readonly")
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
        table_frame = Frame(self.root, padx=10, pady=5, bg="#f8f8f8")
        table_frame.grid(row=1, column=0, sticky="news")

        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#12", "#13")
        packageTable = ttk.Treeview(table_frame, columns=columns, show="headings")
        headings = ["Mã đơn hàng", "Tên người nhận", "SĐT","Tên người gửi","Số điện thoại người gửi", "Địa chỉ","Ngày đặt", "PT Thanh toán", "Phí VC","Trọng lượng","", "Tổng tiền", "Trạng thái"]
        for i, h in enumerate(headings, 1):
            packageTable.heading(f"#{i}", text=h, anchor="w")

        widths = [100, 150, 100, 150, 100, 250, 100, 150, 120, 100, 0, 120, 120]
        for i, w in enumerate(widths, 1):
            if w == 0:
                packageTable.column(f"#{i}", width=w,stretch=False) 
            else:   
                packageTable.column(f"#{i}", width=w, anchor="w")

        packageTable.tag_configure("oddrow", background="#f0f0f0")
        packageTable.tag_configure("evenrow", background="#ffffff")
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=packageTable.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=packageTable.xview)
        packageTable.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        packageTable.pack(fill="both", expand=TRUE)

        load_data()        
        packageTable.bind("<<TreeviewSelect>>", lambda e: row_selection())

        # Validate
        vcmd = (self.root.register(is_number), '%S')

        # Input Frame
        nhapLieu_frame = LabelFrame(self.root, text="Thông tin đơn hàng", bg="#f0f4f8", font=("Arial", 12, "bold"))
        nhapLieu_frame.grid(row=2, column=0, sticky="news", padx=10, pady=5)

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
            province_names = [p["ProvinceName"] for p in province_list if p["ProvinceName"] not in ["Hà Nội 02","Ngoc test", "Test","Test - Alert - Tỉnh - 001"]]
        else:
            print("Lỗi khi gọi GHN API:", response.status_code, response.text)

        thanhPho_box = make_label_entry(1, 0, "Thành phố", Entry, combobox=True, values=province_names)
        thanhPho_box.bind("<<ComboboxSelected>>", thanhPhoBox_on_select)

        quan_box = make_label_entry(1, 2, "Quận", Entry, combobox=True)
        quan_box.bind("<<ComboboxSelected>>", quanBox_on_select)

        phuong_box = make_label_entry(1, 4, "Phường", Entry, combobox=True)

        phuongThucThanhToan_box = make_label_entry(1, 6, "Phương thức thanh toán", Entry, combobox=True, values=["Tiền mặt", "Chuyển khoản"])
        phiVanChuyen_box = make_label_entry(2, 0, "Phí vận chuyển", Entry)
        phiVanChuyen_box.config(state="readonly")

        trongLuong_label = Label(nhapLieu_frame, text="Trọng lượng", bg="#f0f4f8").grid(row=2, column=2, sticky='w')
        trongLuong_frame = Frame(nhapLieu_frame)
        trongLuong_frame.grid(row=2, column=3)
        trongLuong_box = Entry(trongLuong_frame, width=22, bd=0, validate='key', validatecommand=vcmd)
        trongLuong_box.grid(row=0, column=1)
        trongLuong_box.bind('<KeyRelease>',lambda e: on_weight_input())
        donViTinh_cb = ttk.Combobox(trongLuong_frame, values= ["gram","kg"], state="readonly", width=5)
        donViTinh_cb.grid(row=0, column=2)
        donViTinh_cb.bind("<<ComboboxSelected>>", lambda e: on_weight_input())

        tongTien_box = make_label_entry(2, 4, "Tổng tiền", Entry)
        tongTien_box.config(state="readonly")
        trangThai_box = make_label_entry(2, 6, "Trạng thái", Entry, combobox=True, values=["Đã giao", "Đang giao"])

        tenNguoiGui_box = make_label_entry(3, 0, "Tên người gửi", Entry)
        soDienThoaiNguoiGui_box = make_label_entry(3, 2, "Số điện thoại", Entry)

        ghiChu_label = Label(nhapLieu_frame,text="Ghi chú")
        ghiChu_label.grid(row=3,column=4,sticky='w')

        ghiChu_box = Text(nhapLieu_frame,height=5,width=23)
        ghiChu_box.grid(row=3,column=5)

        btn = Button(nhapLieu_frame, text="Thêm sản phẩm", command=themSanPham_window)
        btn.grid(row=3,column=6)

        for widget in nhapLieu_frame.winfo_children():
            widget.grid_configure(padx=8, pady=8)

        button_frame = Frame(self.root, bg="#f0f4f8")
        button_frame.grid(row=3, column=0, sticky="se")

        btn_taoDonHang = Button(button_frame, text="Tạo đơn hàng", width=20, height=2, bg="green", fg="white", font=("Arial", 10), command=taoDonHang_click)
        btn_taoDonHang.grid(row=0, column=0, padx=5)
        btn_suaDonHang = Button(button_frame, text="Sửa đơn hàng", width=20, height=2, bg="blue", fg="white", font=("Arial", 10), command=suaDonHang_click)
        btn_suaDonHang.grid(row=0, column=1, padx=5)
        btn_xoaDonHang = Button(button_frame, text="Xóa đơn hàng", width=20, height=2, bg="red", fg="white", font=("Arial", 10), command=xoaDonHang_click)
        btn_xoaDonHang.grid(row=0, column=2, padx=5)