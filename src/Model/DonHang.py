from datetime import datetime
import Model.KhachHang

class DonHang:
    def __init__(self, ma_don_hang, khach_hang, danh_sach_san_pham,
                 dia_chi_giao, phuong_thuc_thanh_toan, phi_van_chuyen=0,
                 ma_giam_gia=None, ghi_chu="", nhan_vien_xu_ly=None):
        self.ma_don_hang = ma_don_hang
        self.khach_hang = khach_hang
        self.danh_sach_san_pham = danh_sach_san_pham
        self.dia_chi_giao = dia_chi_giao
        self.phuong_thuc_thanh_toan = phuong_thuc_thanh_toan
        self.phi_van_chuyen = phi_van_chuyen
        self.ma_giam_gia = ma_giam_gia
        self.ghi_chu = ghi_chu
        self.nhan_vien_xu_ly = nhan_vien_xu_ly

        self.ngay_dat = datetime.now()
        self.trang_thai = "Chờ xác nhận"

        self.tong_tien = self.tinh_tong_tien()

    def tinh_tong_tien(self):
        tong = sum(sp.tinh_thanh_tien() for sp in self.danh_sach_san_pham)
        if self.ma_giam_gia:
            tong *= (1 - self.ma_giam_gia / 100)
        return tong + self.phi_van_chuyen


    def cap_nhat_trang_thai(self, trang_thai_moi):
        self.trang_thai = trang_thai_moi

    def __str__(self):
        return f"Đơn hàng {self.ma_don_hang} - Khách: {self.khach_hang.ho_ten} - Tổng tiền: {self.tong_tien} VNĐ"
    
    def to_dict(self):
        parts = self.dia_chi_giao.split(",")
        house_address = parts[0].strip()
        phuong_part = parts[1].strip()
        quan_part = parts[2].strip()
        thanhpho = parts[3].strip()
        return {
            "maDonHang":self.ma_don_hang,
            "tenKhachHang":self.khach_hang.ho_ten,
            "soDienThoai":self.khach_hang.so_dien_thoai,
            "diaChi":house_address,
            "phuong":phuong_part,
            "quan":quan_part,
            "thanhPho":thanhpho,
            "danh_sach_san_pham": [sp.to_dict() for sp in self.danh_sach_san_pham],
            "trangThai":self.trang_thai
        }
