import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EnumStatus(enum.Enum):
    Ditolak = 0
    Disetujui = 1
    Pending = 2

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(EnumStatus), default=EnumStatus.Pending, nullable=False)