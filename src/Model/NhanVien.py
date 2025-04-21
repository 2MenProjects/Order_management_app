class NhanVien:
    def __init__(self,ten_tai_khoan,mat_khau,loai_tai_khoan):
        self.ten_tai_khoan = ten_tai_khoan
        self.mat_khau = mat_khau
        self.loai_tai_khoan = loai_tai_khoan
    
    def to_dict(self):
        return {
            "tenTaiKhoan": "user1",
            "matKhau":"abcde",
            "loaiTaiKhoan":"admin"
        }