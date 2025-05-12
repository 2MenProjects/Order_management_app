import hashlib


class NhanVien:
    def __init__(self, ten_tai_khoan, ten_nguoi_dung, mat_khau, loai_tai_khoan, is_hashed=False):
        self.ten_tai_khoan = ten_tai_khoan
        self.ten_nguoi_dung = ten_nguoi_dung
        if is_hashed:
            self.mat_khau = mat_khau
        else:
            self.mat_khau = self.hash_password(mat_khau)
        self.loai_tai_khoan = loai_tai_khoan

    def hash_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def to_dict(self):
        return {
            "tenTaiKhoan": self.ten_tai_khoan,
            "tenNguoiDung": self.ten_nguoi_dung,
            "matKhau": self.mat_khau,
            "loaiTaiKhoan": self.loai_tai_khoan
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["tenTaiKhoan"], data["tenNguoiDung"], data["matKhau"], data["loaiTaiKhoan"], is_hashed=True)
