class LichLamViec:
    def __init__(self, ngay, thu, gioLam):
        self.ngay = ngay
        self.thu = thu
        self.gioLam = gioLam

    def to_dict(self):
        return {
            "ngay": self.ngay,
            "thu": self.thu,
            "gioLam": self.gioLam
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["ngay"], data["thu"], data["gioLam"])
