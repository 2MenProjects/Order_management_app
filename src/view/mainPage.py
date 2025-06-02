from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from src.view.packagePage import HomePage as packagePage
from src.view.accountPage import AccountPage as AccountPage
from src.view.feePage import FeePage as FeePage
from src.view.discountPage import DiscountPage as DiscountPage
from src.view.driverPage import DriverPage as DriverPage
from src.view.detail_employeePage import Detail_EmployeePage as Detail_EmployeePage
from src.view.salaryPage import SalaryPage as SalaryPage
from src.view.loginPage import start_login


class MainPage:
    def __init__(self, loaiTaiKhoan):
        self.loaiTaiKhoan = loaiTaiKhoan
        # Create the main window
        root = Tk()
        root.title("Home")

        WIDTH = 1325
        HEIGHT = 700

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = int((screen_width - WIDTH) / 2)
        y = int((screen_height - HEIGHT) / 2)
        root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
        root.configure(bg="#fff")
        root.resizable(False, False)

        # Main
        # Functions

        def switch_Frame(new_page_func):
            for widget in mainPageFrame.winfo_children():
                widget.destroy()

            new_page_func()

        def switch_Indication(indicator_Label, page):
            for i in indicators:
                indicators[i].config(bg=menuBarColor)
            indicator_Label.config(bg="White")
            if menuBarFrame.winfo_width() > 45:
                fold_MenuBar()
            for frame in mainPageFrame.winfo_children():
                frame.destroy()
            page()

        def extending_Animation():
            current = menuBarFrame.winfo_width()
            if not current > 200:
                menuBarFrame.config(width=current)
                root.after(8, extending_Animation)

        def folding_Animation():
            currentWidthMenuBar = menuBarFrame.winfo_width()
            if currentWidthMenuBar != 45:
                currentWidthMenuBar -= 10
                menuBarFrame.config(width=currentWidthMenuBar)
                root.after(8, folding_Animation)

        def extend_MenuBar():
            extending_Animation()
            toggle_Menu_Btn.config(image=close_Icon, command=fold_MenuBar)

        def fold_MenuBar():
            folding_Animation()
            toggle_Menu_Btn.config(image=toggle_Icon, command=extend_MenuBar)

        def home_Page():
            homePage = Frame(mainPageFrame)
            packagePage(homePage)
            homePage.pack(fill=BOTH)
            homePage.bind("<Button-1>", lambda e: fold_MenuBar())

        def account_Page():
            accountPage = Frame(mainPageFrame)
            AccountPage(accountPage)
            accountPage.pack(fill=BOTH, expand=True)
            accountPage.bind("<Button-1>", lambda e: fold_MenuBar())

        def discount_Page():
            discountPage = Frame(mainPageFrame)
            DiscountPage(discountPage)
            discountPage.pack(fill=BOTH, expand=True)
            discountPage.bind("<Button-1>", lambda e: fold_MenuBar())

        def fee_Page():
            feePage = Frame(mainPageFrame)
            FeePage(feePage)
            feePage.pack(fill=BOTH, expand=True)
            feePage.bind("<Button-1>", lambda e: fold_MenuBar())

        def driver_Page():
            driverPage = Frame(mainPageFrame)
            DriverPage(driverPage, switch_Frame)
            driverPage.pack(fill=BOTH, expand=True)
            driverPage.bind("<Button-1>", lambda e: fold_MenuBar())

        def detail_Employee_Page(maTaiXe):
            detailFrame = Frame(mainPageFrame)
            Detail_EmployeePage(detailFrame, switch_Frame, maTaiXe)
            detailFrame.pack(fill=BOTH, expand=True)

        def salary_Page():
            salary_Frame = Frame(mainPageFrame)
            SalaryPage(salary_Frame, switch_Frame, detail_Employee_Page)
            salary_Frame.pack(fill=BOTH, expand=True)
            salary_Frame.bind("<Button-1>", lambda e: fold_MenuBar())

        def logout():
            confirm = mb.askyesno(
                "Đăng xuất", "Bạn có chắc chắn muốn đăng xuất?")
            if confirm:
                root.destroy()  # đóng MainPage
                start_login(on_login_success=MainPage)

        # Icons
        toggle_Icon = PhotoImage(file="src/image/toggle_btn_icon.png")
        close_Icon = PhotoImage(file="src/image/close_btn_icon.png")
        icons = {
            "Đơn hàng": PhotoImage(file="src/image/store.png"),
            "Tài khoản": PhotoImage(file="src/image/accountant.png"),
            "Tài xế": PhotoImage(file="src/image/accountant.png"),
            "Lương": PhotoImage(file="src/image/salary.png"),
            "Đăng xuất": PhotoImage(file="src/image/log_out.png"),
            "Phí vận chuyển": PhotoImage(file="src/image/pay.png"),
            "Khuyến mãi": PhotoImage(file="src/image/tag.png")
        }

        # Toggle sidemenu
        mainPageFrame = Frame(root)
        # mainPageFrame.pack(side="right",fill="y")
        mainPageFrame.place(x=45, y=0, width=1280, height=700)
        mainPageFrame.bind("<Button-1>", lambda e: fold_MenuBar())
        menuBarFrame = Frame(root, bg="#383838")

        # Color
        menuBarColor = "#383838"

        # Menu items
        toggle_Menu_Btn = Button(menuBarFrame, image=toggle_Icon, bg=menuBarColor,
                                 border=0, activebackground=menuBarColor, command=extend_MenuBar)
        toggle_Menu_Btn.place(x=4, y=10)

        full_menu = [
            ("Đơn hàng", home_Page),
            ("Tài khoản", account_Page),
            ("Tài xế", driver_Page),
            ("Lương", salary_Page),
            ("Phí vận chuyển", fee_Page),
            ("Khuyến mãi", discount_Page)
        ]
        nhanvien_menu = [
            ("Đơn hàng", home_Page),
            ("Phí vận chuyển", fee_Page),
            ("Khuyến mãi", discount_Page)
        ]
        selected_menu = full_menu if loaiTaiKhoan == "Quản lý" else nhanvien_menu

        indicators = {}
        y_pos = 130
        for name, func in selected_menu:
            icon = icons[name]
            indicator = Label(menuBarFrame, bg=menuBarColor)
            indicator.place(x=3, y=y_pos, height=40, width=3)
            indicators[name] = indicator

            Button(menuBarFrame, image=icon, bg=menuBarColor, border=0,
                   activebackground=menuBarColor, command=lambda i=indicator, f=func: switch_Indication(
                       i, f)
                   ).place(x=9, y=y_pos, width=30, height=40)

            lbl = Label(menuBarFrame, bg=menuBarColor, text=name,
                        fg="White", font=("Bold", 15), anchor=W)
            lbl.place(x=45, y=y_pos, width=110, height=40)
            lbl.bind("<Button-1>", lambda e, i=indicator,
                     f=func: switch_Indication(i, f))
            y_pos += 60

        icon = icons["Đăng xuất"]
        logout_indicator = Label(menuBarFrame, bg=menuBarColor)
        logout_indicator.place(x=3, y=y_pos + 40, height=40, width=3)

        Button(menuBarFrame, image=icon, bg=menuBarColor, border=0,
               activebackground=menuBarColor,
               command=lambda: logout()  # gọi hàm xử lý đăng xuất
               ).place(x=9, y=y_pos + 40, width=30, height=40)

        lbl = Label(menuBarFrame, bg=menuBarColor, text="Đăng xuất", fg="White",
                    font=("Bold", 15), anchor=W)
        lbl.place(x=45, y=y_pos + 40, width=110, height=40)
        lbl.bind("<Button-1>", lambda e: logout())

        first_indicator, first_page = selected_menu[0]
        switch_Indication(indicators[first_indicator], first_page)

        menuBarFrame.pack(side=LEFT, fill=Y)
        menuBarFrame.pack_propagate(flag=False)
        menuBarFrame.configure(width=45)

        root.mainloop()
