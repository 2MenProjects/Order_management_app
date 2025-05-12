from datetime import datetime
from src.Model.KhachHang import KhachHang
import json

class DonHang:
    def __init__(self, ma_don_hang, tenNguoiNhan,soDienThoai,
                 dia_chi_giao, phuong_thuc_thanh_toan,hinh_anh, phi_van_chuyen=0,
                 ma_giam_gia=None, ghi_chu="",tong_tien=0,trang_thai = "Chờ xác nhận"):
        self.ma_don_hang = ma_don_hang
        self.tenNguoiNhan = tenNguoiNhan
        self.soDienThoai = soDienThoai
        self.dia_chi_giao = dia_chi_giao
        self.phuong_thuc_thanh_toan = phuong_thuc_thanh_toan
        self.hinh_anh = hinh_anh
        self.phi_van_chuyen = phi_van_chuyen
        self.ma_giam_gia = ma_giam_gia
        self.ghi_chu = ghi_chu

        self.ngay_dat = datetime.now().strftime("%d-%m-%Y")
        self.trang_thai = trang_thai

        self.tong_tien = tong_tien

    def tinh_tong_tien(self):
        pass

    def cap_nhat_trang_thai(self, trang_thai_moi):
        self.trang_thai = trang_thai_moi

    def __str__(self):
        return f"Đơn hàng {self.ma_don_hang} - Khách: {self.tenNguoiNhan} - Tổng tiền: {self.tong_tien} VNĐ"
    
    def to_dict(self):
        parts = self.dia_chi_giao.split(",")
        house_address = parts[0].strip()
        phuong_part = parts[1].strip()
        quan_part = parts[2].strip()
        thanhpho = parts[3].strip()
        return {
            "maDonHang":self.ma_don_hang,
            "tenKhachHang":self.tenNguoiNhan,
            "soDienThoai":self.soDienThoai,
            "diaChi":house_address,
            "phuong":phuong_part,
            "quan":quan_part,
            "thanhPho":thanhpho,
            "phuongThucThanhToan":self.phuong_thuc_thanh_toan,
            "phiVanChuyen":int(self.phi_van_chuyen),
            "hinhAnh":self.hinh_anh,
            "maGiamGia":self.ma_giam_gia,
            "ghiChu":self.ghi_chu,
            "ngayDat":self.ngay_dat,
            "tongTien":int(self.tong_tien),
            "trangThai":self.trang_thai
        }
    @classmethod
    def from_dict(cls, data):
        dia_chi = f'{data["diaChi"]}, {data["phuong"]}, {data["quan"]}, {data["thanhPho"]}'
        don_hang = cls(
            ma_don_hang=data["maDonHang"],
            tenNguoiNhan=data["tenKhachHang"],
            soDienThoai = data["soDienThoai"],
            dia_chi_giao=dia_chi,
            hinh_anh = data["hinhAnh"],
            phuong_thuc_thanh_toan=data["phuongThucThanhToan"],
            phi_van_chuyen=data["phiVanChuyen"],
            ma_giam_gia=data["maGiamGia"],
            ghi_chu=data["ghiChu"]
        )
        don_hang.ngay_dat = data["ngayDat"]
        # don_hang.ngay_dat = datetime.strptime(data["ngayDat"],"%d-%m-%Y")
        don_hang.trang_thai = data["trangThai"]
        don_hang.tong_tien = data["tongTien"]
        return don_hang


class DanhSachDonHang:
    def __init__(self,danhSachDonHang = []):
        self.danhSachDonHang = danhSachDonHang
    def themDonHang(self,donHang):
        try:
            self.danhSachDonHang.append(donHang)
            self.luu_vao_file("src/database/donHangDB.json")
            return True
        except Exception as e:
            print("Lỗi: ",e)
            return False
    def suaDonHang(self,donHang):
        for i, dh in enumerate(self.danhSachDonHang):
            if dh.ma_don_hang == donHang.ma_don_hang:
                self.danhSachDonHang[i] = donHang
                self.luu_vao_file("src/database/donHangDB.json")
                return True
        return False
    def xoaDonHang(self,donHang):
        donHangXoa = self.timKiemDonHang(donHang)
        if donHangXoa !=None:
            self.danhSachDonHang.remove(donHangXoa)
            self.luu_vao_file("src/database/donHangDB.json")
            return True
        else:
            return False
        
    def xoaDonHangTheoMaDon(self,maDonHang):
        donHangXoa = self.timKiemDonHangTheoMaDon(maDonHang)
        if donHangXoa !=None:
            self.danhSachDonHang.remove(donHangXoa)
            self.luu_vao_file("src/database/donHangDB.json")
            return True
        else:
            return False

    def timKiemDonHang(self,donHang):
        for dh in self.danhSachDonHang:
            if dh.ma_don_hang == donHang.ma_don_hang:
                return dh
        return None

    def timKiemDonHangTheoMaDon(self,maDonHang):
        for dh in self.danhSachDonHang:
            if dh.ma_don_hang == maDonHang:
                return dh
        return None

    def taoMaDonHang(self):
        dh = self.danhSachDonHang[-1]    
        chu = ''.join(c for c in dh.ma_don_hang if c.isalpha())
        so = ''.join(c for c in dh.ma_don_hang if c.isdigit())
        so_moi = int(so) + 1
        so_moi_dinh_dang = str(so_moi).zfill(len(so))
        return chu + so_moi_dinh_dang
    
    def luu_vao_file(self, ten_file):
        data = [don_hang.to_dict() for don_hang in self.danhSachDonHang]
        with open(ten_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, default=str)

    def tai_tu_file(self, ten_file):
        try:
            with open(ten_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.danhSachDonHang = [DonHang.from_dict(d) for d in data]
        except FileNotFoundError:
            self.danhSachDonHang = []