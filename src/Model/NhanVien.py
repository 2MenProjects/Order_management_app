import hashlib


class NhanVien:
    def __init__(self, ten_tai_khoan, mat_khau, loai_tai_khoan):
        self.ten_tai_khoan = ten_tai_khoan
        self.mat_khau = self.hash_password(mat_khau)
        self.loai_tai_khoan = loai_tai_khoan

    def hash_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def to_dict(self):
        return {
            "tenTaiKhoan": self.ten_tai_khoan,
            "matKhau": self.mat_khau,
            "loaiTaiKhoan": self.loai_tai_khoan
        }
