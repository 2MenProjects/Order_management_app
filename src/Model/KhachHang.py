class KhachHang:
    def __init__(self, ma_khach_hang, ho_ten, so_dien_thoai, email=None, dia_chi=None):
        self.ma_khach_hang = ma_khach_hang
        self.ho_ten = ho_ten
        self.so_dien_thoai = so_dien_thoai
        self.email = email
        self.dia_chi = dia_chi

    def __str__(self):
        return f"{self.ho_ten} ({self.so_dien_thoai})"
    
    def to_dict(self):
        return {
            "ma_khach_hang": self.ma_khach_hang,
            "ho_ten": self.ho_ten,
            "so_dien_thoai": self.so_dien_thoai,
            "email": self.email,
            "dia_chi": self.dia_chi
        }
