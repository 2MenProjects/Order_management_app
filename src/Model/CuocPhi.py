import json
class CuocPhi:
    def __init__(self,thanhPho,cuocPhi=0):
        self.thanhPho = thanhPho
        self.cuocPhi = int(cuocPhi)
    def __str__(self):
        return f"Thành phố: {self.thanhPho} - Cước phí: {self.cuocPhi}"    
    def to_dict(self):
        return {
            "thanhPho": self.thanhPho,
            "cuocPhi": self.cuocPhi
        } 
    @classmethod
    def from_dict(cls, data):        
        cuoc_phi = cls(
            thanhPho = data["thanhPho"],
            cuocPhi = data["cuocPhi"]            
        )        
        return cuoc_phi

class DanhSachCuocPhi:
    def __init__(self,dscp = []):
        self.dscp = dscp    
    def suaCuocPhi(self,cuocPhi):        
        for i, cp in enumerate(self.dscp):
            if cp.thanhPho == cuocPhi.thanhPho:
                self.dscp[i] = cuocPhi
                self.luu_vao_file("src/database/cuocPhiDB.json")
                return True
        return False    
        
    def timKiemCuocPhi(self,thanhPho):
        for cp in self.dscp:
            if cp.thanhPho == thanhPho:
                return cp
        return None
    
    def luu_vao_file(self, ten_file):
        data = [cuoc_phi.to_dict() for cuoc_phi in self.dscp]
        with open(ten_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, default=str)

    def tai_tu_file(self, ten_file):
        try:
            with open(ten_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.dscp = [CuocPhi.from_dict(cp) for cp in data]
        except FileNotFoundError:
            self.dscp = []
    