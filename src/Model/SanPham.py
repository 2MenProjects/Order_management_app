
class SanPham:
    def __init__(self, ma_san_pham, ten_san_pham, so_luong,hinh_anh):
        self.ma_san_pham = ma_san_pham
        self.ten_san_pham = ten_san_pham
        self.so_luong = int(so_luong)
        self.hinh_anh = hinh_anh

    def to_dict(self):
        return {
            "ma_san_pham": self.ma_san_pham,
            "ten_san_pham": self.ten_san_pham,
            "so_luong": self.so_luong,
            "hinh_anh":self.hinh_anh
        }
    
    @classmethod
    def from_dict(cls, data):        
        sanPham = cls(
            ma_san_pham = data["ma_san_pham"],
            ten_san_pham = data["ten_san_pham"],
            so_luong = data["so_luong"],
            hinh_anh = data["hinh_anh"]
        )        
        return sanPham
        
class DanhSachSanPham:
    def __init__(self,dssp = []):
        self.dssp = dssp    
    def themSanPham(self,sanPham):
        try:            
            self.dssp.append(sanPham)
            return True
        except Exception as e:
            print("Lỗi: ",e)
            return False    
    
    def xoaSanPham(self,maSanPham):
        sanPhamXoa = self.timKiemSanPhamTheoMa(maSanPham)
        if sanPhamXoa !=None:
            self.dssp.remove(sanPhamXoa)
            return True
        else:
            return False

    def suaSanPham(self,sanPham):
        for i, sp in enumerate(self.dssp):
            if sp.ma_san_pham == sanPham.ma_san_pham:
                self.dssp[i] = sanPham
                return True
        return False    
    
    def taoMaSanPham(self):        
        if len(self.dssp) == 0:
            return "SP00001"
        else:
            sp = self.dssp[-1]    
            chu = ''.join(c for c in sp.ma_san_pham if c.isalpha())
            so = ''.join(c for c in sp.ma_san_pham if c.isdigit())
            so_moi = int(so) + 1
            so_moi_dinh_dang = str(so_moi).zfill(len(so))
            return chu + so_moi_dinh_dang
        
    def timKiemSanPham(self,sanPham):
        for sp in self.dssp:
            if sp.ma_san_pham == sanPham.ma_san_pham:
                return sp
        return None
    
    def timKiemSanPhamTheoMa(self,maSanPham):
        for sp in self.dssp:
            if sp.ma_san_pham == maSanPham:
                return sp
        return None
    
    def to_dict(self):
        danhSach = []
        for sp in self.dssp:
            danhSach.append(sp.to_dict())
        return danhSach
 
    @classmethod
    def from_dict(cls,danhSach):
        dssp = []
        for sp in danhSach:
            dssp.append(SanPham.from_dict(sp))
        return dssp

    # def luu_vao_file(self, ten_file):
    #     data = [sp.to_dict() for sp in self.dssp]
    #     with open(ten_file, 'w', encoding='utf-8') as f:
    #         json.dump(data, f, ensure_ascii=False, indent=4, default=str)

    # def tai_tu_file(self, ten_file):
    #     try:
    #         with open(ten_file, 'r', encoding='utf-8') as f:
    #             data = json.load(f)
    #             self.dssp = [SanPham.from_dict(sp) for sp in data]
    #         self.luu_vao_file(ten_file)
    #     except FileNotFoundError:
    #         self.dssp = []
