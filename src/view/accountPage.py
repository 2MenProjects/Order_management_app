from tkinter import *
from tkinter import ttk
import json

class AccountPage:
    def __init__(self,root):
        self.root = root
        self.root.columnconfigure(0, weight=1)

        def row_selection():
            selected_item = accountTable.focus()
            if selected_item:
                item_values = accountTable.item(selected_item)['values']
                if item_values:                
                    pass              

        #Table
        table_frame = Frame(self.root)        
        table_frame.grid(row=0,column=0,sticky="news")        

        columns = ("#1", "#2", "#3","#4")
        accountTable = ttk.Treeview(table_frame, columns=columns, show="headings")
        accountTable.heading("#1",text="Tên tài khoản")
        accountTable.heading("#2",text="Tên người dùng")
        accountTable.heading("#3",text="Mật khẩu")
        accountTable.heading("#4",text="Loại tài khoản")        
        accountTable.column("#1", width=30,anchor="center")
        accountTable.column("#2", width=50,anchor="center")
        accountTable.column("#3", width=50,anchor="center")
        accountTable.column("#4", width=200,anchor="center")

        accountTable.tag_configure("oddrow", background="#f0f0f0")
        accountTable.tag_configure("evenrow", background="#ffffff")

         # Thêm scrollbar dọc
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=accountTable.yview)
        accountTable.configure(yscroll=scrollbar.set)        
        scrollbar.pack(side="right", fill="y")
        accountTable.pack(fill="both",expand=TRUE)
        with open("src/database/account.json","r",encoding="utf-8") as dataFile:
            data = json.load(dataFile)
            for index, item in enumerate(data):
                tag = "evenrow" if index % 2 == 0 else "oddrow"                
                accountTable.insert("",END,values=(item["tenTaiKhoan"],item["tenTaiKhoan"],item["matKhau"],item["loaiTaiKhoan"]),tags=(tag,))
        accountTable.bind("<<TreeviewSelect>>",lambda e:row_selection())
