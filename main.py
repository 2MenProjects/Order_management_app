from src.view.loginPage import start_login
from src.view.mainPage import MainPage

if __name__ == "__main__":
    def handle_login_success(loaiTaiKhoan):
        MainPage(loaiTaiKhoan)

    start_login(on_login_success=handle_login_success)
