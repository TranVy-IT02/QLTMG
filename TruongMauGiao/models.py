import json
from datetime import datetime
from enum import Enum as RoleEnum
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum, Boolean, Float
from sqlalchemy.orm import relationship
from TruongMauGiao import db, app


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, unique=True)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)


class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2


class User(Base, UserMixin):
    username = Column(String(150), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    avatar = Column(String(500),
                    default="https://static.vecteezy.com/system/resources/previews/005/544/753/original/profile-icon-design-free-vector.jpg")
    role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


class Category(Base):
    hocPhi= Column(Float, nullable=False)
    students = relationship('Student', backref="category", lazy=True)



class Student(Base):
    image = Column(String(500),
                   default="https://cdn2.cellphones.com.vn/insecure/rs:fill:0:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/d/i/dien-thoai-samsung-galaxy-s25_3__1.png")
    gioiTinh=Column(String(10), nullable=False)
    nameParent = Column(String(150), nullable=False)
    SDT = Column(String(10), nullable=False)
    tienAnThem=Column(Float)
    cate_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    description = Column(Text)
    Invoice = relationship('Invoice',backref="students")


    def __str__(self):
        return self.name

class Invoice(Base):
    tongTien=Column(Float)
    ngayThu=Column(DateTime, default=datetime.now())
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    student = relationship("Student", back_populates="Invoice")

class HealthRecord(Base):
    # override name để không dùng
    name = None
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    record_date = Column(DateTime, default=datetime.now)
    weight = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    note = Column(Text)
    is_fever = Column(Boolean, default=False)
    student = relationship("Student", backref="health_records")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_fever = self.temperature > 37.5

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        c1 = Category(name="Mầm",hocPhi=1500000)
        c2 = Category(name="Chồi",hocPhi=1500000)
        c3 = Category(name="Lá",hocPhi=1500000)

        db.session.add_all([c1, c2, c3])  # tạo script
        with open("data/student.json", encoding="utf-8") as f:
            students = json.load(f)

            for p in students:
                stud = Student(**p)
                db.session.add(stud)
        import hashlib

        u1 = User(name="User", username="user", password=hashlib.md5("123".encode("utf-8")).hexdigest())
        u2 = User(name="Admin", username="admin", password=hashlib.md5("123".encode("utf-8")).hexdigest())

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()  # run script
