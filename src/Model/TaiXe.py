class TaiXe:
    def __init__(self, maTaiXe, tenTaiXe, soDienThoai, diaChi, cccd, nganHang, stk_nganHang, luongCoBan):
        self.maTaiXe = maTaiXe
        self.tenTaiXe = tenTaiXe
        self.soDienThoai = soDienThoai
        self.diaChi = diaChi
        self.cccd = cccd
        self.nganHang = nganHang
        self.stk_nganHang = stk_nganHang
        self.luongCoBan = luongCoBan

    def to_dict(self):
        return {
            "maTaiXe": self.maTaiXe,
            "tenTaiXe": self.tenTaiXe,
            "soDienThoai": self.soDienThoai,
            "diaChi": self.diaChi,
            "cccd": self.cccd,
            "nganHang": self.nganHang,
            "stk_nganHang": self.stk_nganHang,
            "luongCoBan": self.luongCoBan
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["maTaiXe"], data["tenTaiXe"], data["soDienThoai"],
                   data["diaChi"], data["cccd"], data["nganHang"], data["stk_nganHang"], data["luongCoBan"])
