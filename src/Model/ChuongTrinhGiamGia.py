import json
from datetime import datetime
class ChuongTrinhGiamGia:
    def __init__(self,maGiamGia,phanTramGiam,ngayBatDau,ngayKetThuc,trangThai="Chưa bắt đầu"):
        self.maGiamGia = maGiamGia
        self.phanTramGiam = int(phanTramGiam)
        self.ngayBatDau = ngayBatDau
        self.ngayKetThuc = ngayKetThuc
        self.trangThai = trangThai
    def to_dict(self):
        return {
            "maGiamGia": self.maGiamGia,
            "phanTramGiam":self.phanTramGiam,
            "ngayBatDau":self.ngayBatDau,
            "ngayKetThuc":self.ngayKetThuc,
            "trangThai":self.trangThai            
        } 
    @classmethod
    def from_dict(cls, data):        
        chuongTrinh = cls(
            maGiamGia = data["maGiamGia"],
            phanTramGiam = data["phanTramGiam"],
            ngayBatDau = data["ngayBatDau"],
            ngayKetThuc = data["ngayKetThuc"],
            trangThai = data["trangThai"]
        )        
        return chuongTrinh

class DanhSachChuongTrinh:
    def __init__(self,dsct = []):
        self.dsct = dsct
    def themChuongTrinh(self,chuongTrinh):
        try:            
            self.dsct.append(chuongTrinh)
            self.luu_vao_file("src/database/chuongTrinhGiamGiaDB.json")
            return True
        except Exception as e:
            print("Lỗi: ",e)
            return False    
    
    def xoaChuongTrinh(self,maGiamGia):
        chuongTrinhXoa = self.timKiemChuongTrinhTheoMaGiam(maGiamGia)
        if chuongTrinhXoa !=None:
            self.dsct.remove(chuongTrinhXoa)
            self.luu_vao_file("src/database/chuongTrinhGiamGiaDB.json")
            return True
        else:
            return False

    def suaChuongTrinh(self,chuongTrinh):
        for i, ct in enumerate(self.dsct):
            if ct.maGiamGia == chuongTrinh.maGiamGia:
                self.dsct[i] = chuongTrinh
                self.luu_vao_file("src/database/chuongTrinhGiamGiaDB.json")
                return True
        return False    
    
    def taoMaChuongTrinh(self):
        if len(self.dsct) == 0:
            return "GM00001"
        else:
            ct = self.dsct[-1]    
            chu = ''.join(c for c in ct.maGiamGia if c.isalpha())
            so = ''.join(c for c in ct.maGiamGia if c.isdigit())
            so_moi = int(so) + 1
            so_moi_dinh_dang = str(so_moi).zfill(len(so))
            return chu + so_moi_dinh_dang
        
    def timKiemChuongTrinh(self,chuongTrinh):
        for ct in self.dsct:
            if ct.maGiamGia == chuongTrinh.maGiamGia:
                return ct
        return None
    
    def timKiemChuongTrinhTheoMaGiam(self,maGiam):
        for ct in self.dsct:
            if ct.maGiamGia == maGiam:
                return ct
        return None
    
    def timChuongTrinhDangDienRa(self):
        for ct in self.dsct:
            if ct.trangThai == "Đang diễn ra":
                return ct
        return None

    def luu_vao_file(self, ten_file):
        data = [ct.to_dict() for ct in self.dsct]
        with open(ten_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, default=str)

    def tai_tu_file(self, ten_file):
        try:
            with open(ten_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.dsct = [ChuongTrinhGiamGia.from_dict(ct) for ct in data]
            self.cap_nhat_trang_thai_chuong_trinh()
            self.luu_vao_file(ten_file)
        except FileNotFoundError:
            self.dsct = []

    def cap_nhat_trang_thai_chuong_trinh(self):
            today = datetime.now().date()
            for ct in self.dsct:
                ngay_bat_dau = datetime.strptime(ct.ngayBatDau, "%d-%m-%Y").date()
                ngay_ket_thuc = datetime.strptime(ct.ngayKetThuc, "%d-%m-%Y").date()
                if ngay_bat_dau <= today <= ngay_ket_thuc:
                    ct.trangThai = "Đang diễn ra"
                elif today < ngay_bat_dau:
                    ct.trangThai = "Chưa bắt đầu"
                elif today > ngay_ket_thuc:
                    ct.trangThai = "Đã kết thúc"
    