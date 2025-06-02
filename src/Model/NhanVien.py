import hashlib

class NhanVien:
    def __init__(self, ten_tai_khoan, ten_nguoi_dung, mat_khau, loai_tai_khoan, so_dien_thoai, dia_chi, cccd, ngan_hang, stk_ngan_hang, luong_co_ban, is_hashed=False):
        self.ten_tai_khoan = ten_tai_khoan
        self.ten_nguoi_dung = ten_nguoi_dung
        self.mat_khau = mat_khau if is_hashed else self.hash_password(mat_khau)
        self.loai_tai_khoan = loai_tai_khoan
        self.so_dien_thoai = so_dien_thoai
        self.dia_chi = dia_chi
        self.cccd = cccd
        self.ngan_hang = ngan_hang
        self.stk_ngan_hang = stk_ngan_hang
        self.luong_co_ban = luong_co_ban

    def hash_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def to_dict(self):
        return {
            "tenTaiKhoan": self.ten_tai_khoan,
            "tenNguoiDung": self.ten_nguoi_dung,
            "matKhau": self.mat_khau,
            "loaiTaiKhoan": self.loai_tai_khoan,
            "soDienThoai": self.so_dien_thoai,
            "diaChi": self.dia_chi,
            "cccd": self.cccd,
            "nganHang": self.ngan_hang,
            "stk_nganHang": self.stk_ngan_hang,
            "luongCoBan": self.luong_co_ban
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["tenTaiKhoan"],
            data["tenNguoiDung"],
            data["matKhau"],
            data["loaiTaiKhoan"],
            data["soDienThoai"],
            data["diaChi"],
            data["cccd"],
            data["nganHang"],
            data["stk_nganHang"],
            data["luongCoBan"],
            is_hashed=True
        )
