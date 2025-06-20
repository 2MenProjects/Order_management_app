from tkinter import *
from tkinter import messagebox
import subprocess
# from src.view.mainPage import MainPage as mainPage
import json
import hashlib
import os
from src.Model.NhanVien import NhanVien


def start_login(on_login_success=None):
    filename = "src/database/account.json"

    win = Tk()
    win.title("Login")
    icon = PhotoImage(file="src/image/warehouse.png")
    win.iconphoto(True, icon)

    WIDTH = 925
    HEIGHT = 500

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = int((screen_width - WIDTH) / 2)
    y = int((screen_height - HEIGHT) / 2)
    win.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
    win.configure(bg="#fff")
    win.resizable(False, False)

    img = PhotoImage(file="src/image/login.png")
    Label(win, image=img, bg='white').place(x=50, y=50)

    frame = Frame(win, width=350, height=350, bg="white")
    frame.place(x=480, y=70)

    heading = Label(frame, text="Sign in", fg="#57a1f8",
                    bg="white", font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=100, y=5)
    # ----------------------------------------------------------------

    def on_enter(event):
        widget = event.widget
        widget.delete(0, END)

    def on_leave(event):
        name = user.get()
        if name == "":
            user.insert(0, "Username")

    user = Entry(frame, width=25, fg="black", bg="white",
                 font=('Microsoft YaHei UI Light', 11), border=0)
    user.place(x=30, y=80)
    user.insert(0, "Username")
    user.bind("<FocusIn>", on_enter)
    user.bind("<FocusOut>", on_leave)
    Frame(frame, width=295, height=2, bg="black").place(x=25, y=107)

    # ----------------------------------------------------------------
    def on_leave(event):
        name = passwordBox.get()
        if name == "":
            passwordBox.insert(0, "Password")

    passwordBox = Entry(frame, width=25, fg="black", show="*", bg="white", font=(
        'Microsoft YaHei UI Light', 11), border=0)
    passwordBox.place(x=30, y=150)
    passwordBox.insert(0, "Password")
    passwordBox.bind("<FocusIn>", on_enter)
    passwordBox.bind("<FocusOut>", on_leave)
    Frame(frame, width=295, height=2, bg="black").place(x=25, y=177)
    # ----------------------------------------------------------------

    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def load_data_from_file(filename):
        if not os.path.exists(filename):
            data = []
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        else:
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    data = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                data = []

        if not data:
            admin = NhanVien("admin", "admin", "1234", "admin")

            data.append(admin.to_dict())

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        return data

    load_data_from_file(filename)

    def signIn():
        username = user.get()
        password = hash_password(passwordBox.get())
        try:
            with open("src/database/account.json", "r", encoding="utf-8") as open_file:
                data = json.load(open_file)
                for line in data:
                    if line["tenTaiKhoan"] == username and line["matKhau"] == password:
                        win.destroy()
                        if on_login_success:
                            on_login_success(line["loaiTaiKhoan"])
                        return
                messagebox.showerror("Error", "Invalid credentials!")
                # if data["name"] == username and data["password"] == password:
                #     win.destroy()
                #     homePage.HomePage()  # Open Home Page
                # else:
                #     messagebox.showerror("Error","Invalid credentials!")
                # if username == "admin" and password == "1234":
                #     #subprocess.Popen(["python", "homePage.py"])
                #     win.destroy()
                #     homePage.HomePage()  # Open Home Page
                # else:
                #     messagebox.showerror("Error","Invalid credentials!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi: {e}")

    signInBtn = Button(frame, width=39, pady=7, text="Sign in", bg="#57a1f8",
                       fg="white", border=0, command=signIn, default='active')
    signInBtn.place(x=35, y=204)
    signInBtn.bind('<Return>', lambda e: signIn())

    win.mainloop()
