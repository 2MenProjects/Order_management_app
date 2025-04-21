from tkinter import *
from tkinter import ttk
import json
import requests
token = "5c296349-b9e1-11ef-9083-dadc35c0870d"
apiAddress_district = "https://dev-online-gateway.ghn.vn/shiip/public-api/master-data/district"
apiAddress_ward = "https://dev-online-gateway.ghn.vn/shiip/public-api/master-data/ward"
apiAddress_province = "https://dev-online-gateway.ghn.vn/shiip/public-api/master-data/province"
class HomePage:
    def __init__(self,root):
        self.root = root
        self.root.columnconfigure(0, weight=1)
        #Functions
        def thanhPhoBox_on_select(event):
            selected_name = thanhPho_box.get()
            selected = next((p for p in province_list if p["ProvinceName"] == selected_name), None)
            if selected:
                district_header = {
                    "Content-Type": "application/json",
                    "Token": token,
                }
                district_param = {
                    "province_id": selected['ProvinceID']
                }
                district_response = requests.get(apiAddress_district,headers=district_header,params=district_param)
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
                ward_param = {
                    "district_id": selected['DistrictID']
                }
                ward_response = requests.get(apiAddress_ward,headers=ward_header,params=ward_param)
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
                    maDonHang_box.delete(0,END)
                    tenNguoiNhan_box.delete(0,END)
                    soDienThoai_box.delete(0,END)
                    maDonHang_box.insert(0,item_values[0])
                    tenNguoiNhan_box.insert(0,item_values[1])
                    soDienThoai_box.insert(0,"0"+str(item_values[2]))                    
                    parts = item_values[3].split(",")
                    house_address = parts[0].strip()
                    phuong_part = parts[1].strip()
                    quan_part = parts[2].strip()
                    thanhpho = parts[3].strip()
                    diaChi_box.delete(0,END)
                    diaChi_box.insert(0,house_address)
                    thanhPho_box.set(thanhpho)
                    thanhPhoBox_on_select(None)                
                    quan_box.set(quan_part)
                    quanBox_on_select(None)
                    phuong_box.set(phuong_part)    
                    trangThai_box.set(item_values[4])                

        def taoDonHang_click():
            pass
            
        def suaDonHang_click():
            pass
        
        def xoaDonHang_click():
            pass

        #Table
        table_frame = Frame(self.root)        
        table_frame.grid(row=0,column=0,sticky="news")        

        columns = ("#1", "#2", "#3","#4","#5")
        packageTable = ttk.Treeview(table_frame, columns=columns, show="headings")
        packageTable.heading("#1",text="Mã đơn hàng")
        packageTable.heading("#2",text="Tên người nhận")
        packageTable.heading("#3",text="Số điện thoại")
        packageTable.heading("#4",text="Địa chỉ")
        packageTable.heading("#5",text="Trạng thái")
        packageTable.column("#1", width=30,anchor="center")
        packageTable.column("#2", width=50,anchor="center")
        packageTable.column("#3", width=50,anchor="center")
        packageTable.column("#4", width=200,anchor="center")
        packageTable.column("#5", width=50,anchor="center")

        packageTable.tag_configure("oddrow", background="#f0f0f0")
        packageTable.tag_configure("evenrow", background="#ffffff")
        # Thêm scrollbar dọc
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=packageTable.yview)
        packageTable.configure(yscroll=scrollbar.set)        
        scrollbar.pack(side="right", fill="y")
        packageTable.pack(fill="both",expand=TRUE)
        with open("src/database/donHangDB.json","r",encoding="utf-8") as dataFile:
            data = json.load(dataFile)
            for index, item in enumerate(data):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                address = item["diaChi"]+", "+item["phuong"]+", "+item["quan"]+", "+item["thanhPho"]
                packageTable.insert("",END,values=(item["maDonHang"],item["tenKhachHang"],item["soDienThoai"],address,item["trangThai"]),tags=(tag,))
        packageTable.bind("<<TreeviewSelect>>",lambda e:row_selection())

        #Nhập liệu
        nhapLieu_frame = LabelFrame(self.root,text="Thông tin đơn hàng")
        nhapLieu_frame.grid(row=1,column=0,sticky="news")

        maDonHang_label = Label(nhapLieu_frame,text="Mã đơn hàng")
        maDonHang_label.grid(row=0,column=0)
        maDonHang_box = Entry(nhapLieu_frame,width=30,bd=0)
        maDonHang_box.grid(row=0,column=1)

        tenNguoiNhan_label = Label(nhapLieu_frame,text="Tên người nhận")
        tenNguoiNhan_label.grid(row=0,column=2)
        tenNguoiNhan_box = Entry(nhapLieu_frame,width=30,bd=0)
        tenNguoiNhan_box.grid(row=0,column=3)

        soDienThoai_label = Label(nhapLieu_frame,text="Số điện thoại")
        soDienThoai_label.grid(row=0,column=4)
        soDienThoai_box = Entry(nhapLieu_frame,width=30,bd=0)
        soDienThoai_box.grid(row=0,column=5)

        diaChi_label = Label(nhapLieu_frame,text="Địa chỉ")
        diaChi_label.grid(row=0,column=6)
        diaChi_box = Entry(nhapLieu_frame,width=30,bd=0)
        diaChi_box.grid(row=0,column=7)

        headers = {
            "Content-Type": "application/json",
            "Token": token,
        }
        province_names = []
        response = requests.get(apiAddress_province,headers=headers)
        if response.status_code == 200:
            province_list = response.json().get("data",[])
            province_names = [p["ProvinceName"] for p in province_list if p["ProvinceName"]!="Ngoc test" and p["ProvinceName"]!="Test"]     
        else:
            print("Lỗi khi gọi GHN API:", response.status_code, response.text)

        thanhPho_label = Label(nhapLieu_frame,text="Thành phố")
        thanhPho_label.grid(row=1,column=0)
        thanhPho_box = ttk.Combobox(nhapLieu_frame,values=province_names, state="readonly",width=27)
        thanhPho_box.grid(row=1,column=1)
        thanhPho_box.bind("<<ComboboxSelected>>", thanhPhoBox_on_select)

        quan_label = Label(nhapLieu_frame,text="Quận")
        quan_label.grid(row=1,column=2)
        quan_box = ttk.Combobox(nhapLieu_frame,values=[], state="readonly",width=27)
        quan_box.grid(row=1,column=3)
        quan_box.bind("<<ComboboxSelected>>", quanBox_on_select)
        
        phuong_label = Label(nhapLieu_frame,text="Phường")
        phuong_label.grid(row=1,column=4)
        phuong_box = ttk.Combobox(nhapLieu_frame,values=[], state="readonly",width=27)
        phuong_box.grid(row=1,column=5)

        trangThai_label = Label(nhapLieu_frame,text="Trạng thái")
        trangThai_label.grid(row=1,column=6)
        trangThai_box = ttk.Combobox(nhapLieu_frame,values=["Đã giao","Đang giao"], state="readonly",width=27)
        trangThai_box.grid(row=1,column=7)

        for widget in nhapLieu_frame.winfo_children():
            widget.grid_configure(padx=5,pady=10)

        button_frame = Frame(self.root)
        button_frame.grid(row=2,column=0,sticky="news")

        taoDonHang_btn = Button(button_frame,text="Tạo đơn hàng",width=20,height=2,bd=0,background="green",fg="white",font=("Arial",10),command=taoDonHang_click)
        taoDonHang_btn.grid(row=0,column=0)

        suaDonHang_btn = Button(button_frame,text="Sửa đơn hàng",width=20,height=2,bd=0,background="blue",fg="white",font=("Arial",10),command=suaDonHang_click)
        suaDonHang_btn.grid(row=0,column=1)

        xoaDonHang_btn = Button(button_frame,text="Xóa đơn hàng",width=20,height=2,bd=0,background="red",fg="white",font=("Arial",10),command=xoaDonHang_click)
        xoaDonHang_btn.grid(row=0,column=2)

        for widget in button_frame.winfo_children():
            widget.grid_configure(padx=5,pady=10)
        
        

