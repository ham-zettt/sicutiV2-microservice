import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EnumStatus(enum.Enum):
    Ditolak = 0
    Disetujui = 1
    Pending = 2

class PengajuanCuti(db.Model):
    __tablename__ = 'transaksi'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    alasan = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(EnumStatus), default=EnumStatus.Pending, nullable=False)

    def __init__(self, nama, alasan, status=EnumStatus.Pending):
        self.nama = nama
        self.alasan = alasan
        self.status = status

# docker exec -it mysql_db bash