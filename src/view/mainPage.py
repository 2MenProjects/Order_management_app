from tkinter import *
from tkinter import ttk
from src.view.packagePage import HomePage as packagePage
from src.view.accountPage import AccountPage as AccountPage


class MainPage:
    def __init__(self, shared_text="Phuc"):
        self.shared_text = shared_text
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

        def switch_Indication(indicator_Label, page):
            home_Btn_Indicator.config(bg=menuBarColor)
            account_Btn_Indicator.config(bg=menuBarColor)
            delivery_Btn_Indicator.config(bg=menuBarColor)
            about_Btn_Indicator.config(bg=menuBarColor)
            update_Btn_Indicator.config(bg=menuBarColor)
            indicator_Label.config(bg="White")
            if menuBarFrame.winfo_width() > 45:
                fold_MenuBar()
            for frame in mainPageFrame.winfo_children():
                frame.destroy()
            page()

        def extending_Animation():
            currentWidthMenuBar = menuBarFrame.winfo_width()
            if not currentWidthMenuBar > 200:
                currentWidthMenuBar += 10
                menuBarFrame.config(width=currentWidthMenuBar)
                # mainPageFrame.place(relwidth=1.0 - currentWidthMenuBar/925, relheight=1.0, x=currentWidthMenuBar)
                root.after(ms=8, func=extending_Animation)

        def folding_Animation():
            currentWidthMenuBar = menuBarFrame.winfo_width()
            if currentWidthMenuBar != 45:
                currentWidthMenuBar -= 10
                menuBarFrame.config(width=currentWidthMenuBar)
                # mainPageFrame.place(relwidth=1.0 - currentWidthMenuBar/925, relheight=1.0, x=currentWidthMenuBar)
                root.after(ms=8, func=folding_Animation)

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

        def about_Page():
            aboutPage = Frame(mainPageFrame)
            aboutPageLabel = Label(
                aboutPage, text="About Page", font=("Bold", 20))
            aboutPageLabel.place(x=100, y=200)
            aboutPage.pack(fill=BOTH, expand=True)
            aboutPage.bind("<Button-1>", lambda e: fold_MenuBar())

        def update_Page():
            updatePage = Frame(mainPageFrame)
            updatePageLabel = Label(
                updatePage, text="Update Page", font=("Bold", 20))
            updatePageLabel.place(x=100, y=200)
            updatePage.pack(fill=BOTH, expand=True)
            updatePage.bind("<Button-1>", lambda e: fold_MenuBar())

        def delivery_Page():
            deliveryPage = Frame(mainPageFrame)
            deliveryPageLabel = Label(
                deliveryPage, text="Delivery Page", font=("Bold", 20))
            deliveryPageLabel.place(x=100, y=200)
            deliveryPage.pack(fill=BOTH, expand=True)
            deliveryPage.bind("<Button-1>", lambda e: fold_MenuBar())

        # Icons
        toggle_Icon = PhotoImage(file="src/image/toggle_btn_icon.png")
        close_Icon = PhotoImage(file="src/image/close_btn_icon.png")
        home_Icon = PhotoImage(file="src/image/store.png")
        account_Icon = PhotoImage(file="src/image/accountant.png")
        delivery_Icon = PhotoImage(file="src/image/delivery-truck.png")
        update_Icon = PhotoImage(file="src/image/updates_icon.png")
        about_Icon = PhotoImage(file="src/image/about_icon.png")

        # Toggle sidemenu
        mainPageFrame = Frame(root)
        # mainPageFrame.pack(side="right",fill="y")
        mainPageFrame.place(x=45,y=0, width=1280, height=700)
        mainPageFrame.bind("<Button-1>", lambda e: fold_MenuBar())
        menuBarFrame = Frame(root, bg="#383838")

        # Color
        menuBarColor = "#383838"

        # Menu items
        toggle_Menu_Btn = Button(menuBarFrame, image=toggle_Icon, bg=menuBarColor,
                                 border=0, activebackground=menuBarColor, command=extend_MenuBar)
        toggle_Menu_Btn.place(x=4, y=10)

        # Home
        home_Menu_Btn = Button(menuBarFrame, image=home_Icon, bg=menuBarColor, border=0,
                               activebackground=menuBarColor, command=lambda: switch_Indication(home_Btn_Indicator, home_Page))
        home_Menu_Btn.place(x=9, y=130, width=30, height=40)

        home_Btn_Indicator = Label(menuBarFrame, bg=menuBarColor)
        home_Btn_Indicator.place(x=3, y=130, height=40, width=3)

        home_Page_Label = Label(menuBarFrame, bg=menuBarColor,
                                text="Đơn hàng", fg="White", font=("Bold", 15), anchor=W)
        home_Page_Label.place(x=45, y=130, width=100, height=40)
        home_Page_Label.bind(
            "<Button-1>", lambda e: switch_Indication(home_Btn_Indicator, home_Page))

        # Account
        account_Menu_Btn = Button(menuBarFrame, image=account_Icon, bg=menuBarColor, border=0,
                                  activebackground=menuBarColor, command=lambda: switch_Indication(account_Btn_Indicator, account_Page))
        account_Menu_Btn.place(x=9, y=190, width=30, height=40)

        account_Btn_Indicator = Label(menuBarFrame, bg=menuBarColor)
        account_Btn_Indicator.place(x=3, y=190, height=40, width=3)

        account_Page_Label = Label(
            menuBarFrame, bg=menuBarColor, text="Tài khoản", fg="White", font=("Bold", 15), anchor=W)
        account_Page_Label.place(x=45, y=190, width=100, height=40)
        account_Page_Label.bind(
            "<Button-1>", lambda e: switch_Indication(account_Btn_Indicator, account_Page))

        # Delivery
        delivery_Menu_Btn = Button(menuBarFrame, image=delivery_Icon, bg=menuBarColor, border=0,
                                   activebackground=menuBarColor, command=lambda: switch_Indication(delivery_Btn_Indicator, delivery_Page))
        delivery_Menu_Btn.place(x=9, y=250, width=35, height=40)

        delivery_Btn_Indicator = Label(menuBarFrame, bg=menuBarColor)
        delivery_Btn_Indicator.place(x=3, y=250, height=40, width=3)

        delivery_Page_Label = Label(
            menuBarFrame, bg=menuBarColor, text="Vận chuyển", fg="White", font=("Bold", 15), anchor=W)
        delivery_Page_Label.place(x=45, y=250, width=110, height=40)
        delivery_Page_Label.bind(
            "<Button-1>", lambda e: switch_Indication(delivery_Btn_Indicator, delivery_Page))

        # Update
        update_Menu_Btn = Button(menuBarFrame, image=update_Icon, bg=menuBarColor, border=0,
                                 activebackground=menuBarColor, command=lambda: switch_Indication(update_Btn_Indicator, update_Page))
        update_Menu_Btn.place(x=9, y=310, width=30, height=40)

        update_Btn_Indicator = Label(menuBarFrame, bg=menuBarColor)
        update_Btn_Indicator.place(x=3, y=310, height=40, width=3)

        update_Page_Label = Label(menuBarFrame, bg=menuBarColor,
                                  text="Update", fg="White", font=("Bold", 15), anchor=W)
        update_Page_Label.place(x=45, y=310, width=100, height=40)
        update_Page_Label.bind(
            "<Button-1>", lambda e: switch_Indication(update_Btn_Indicator, update_Page))

        # About
        about_Menu_Btn = Button(menuBarFrame, image=about_Icon, bg=menuBarColor, border=0,
                                activebackground=menuBarColor, command=lambda: switch_Indication(about_Btn_Indicator, about_Page))
        about_Menu_Btn.place(x=9, y=370, width=30, height=40)

        about_Btn_Indicator = Label(menuBarFrame, bg=menuBarColor)
        about_Btn_Indicator.place(x=3, y=370, height=40, width=3)

        about_Page_Label = Label(menuBarFrame, bg=menuBarColor,
                                 text="About", fg="White", font=("Bold", 15), anchor=W)
        about_Page_Label.place(x=45, y=370, width=100, height=40)
        about_Page_Label.bind(
            "<Button-1>", lambda e: switch_Indication(about_Btn_Indicator, about_Page))

        switch_Indication(home_Btn_Indicator, home_Page)

        menuBarFrame.pack(side=LEFT, fill=Y)
        menuBarFrame.pack_propagate(flag=False)
        menuBarFrame.configure(width=45)

        root.mainloop()
