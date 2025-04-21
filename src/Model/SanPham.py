class SanPham:
    def __init__(self, ma_san_pham, ten_san_pham, don_gia, so_luong):
        self.ma_san_pham = ma_san_pham
        self.ten_san_pham = ten_san_pham
        self.don_gia = don_gia
        self.so_luong = so_luong

    def tinh_thanh_tien(self):
        return self.don_gia * self.so_luong

    def to_dict(self):
        return {
            "ma_san_pham": self.ma_san_pham,
            "ten_san_pham": self.ten_san_pham,
            "don_gia": self.don_gia,
            "so_luong": self.so_luong,
            "thanh_tien": self.tinh_thanh_tien()
        }

    def __str__(self):
        return f"{self.ten_san_pham} x {self.so_luong} - {self.tinh_thanh_tien()} VNĐ"
