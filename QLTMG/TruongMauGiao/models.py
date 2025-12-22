import json

from TruongMauGiao import db, app
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Base (db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, unique=True)

class Category(Base):
    students = relationship('Student', backref="category", lazy=True)

class Student(Base):
    SDT = Column(String(10), nullable=False)
    nameParent=Column(String(150), nullalbe=True)
    image = Column(String(300), default="https://cdn2.cellphones.com.vn/insecure/rs:fill:0:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/d/i/dien-thoai-samsung-galaxy-s25_3__1.png")
    cate_id = Column(Integer, ForeignKey(Category.id),nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        c1 = Category(name="Trẻ")
        c2 = Category(name="Giáo viên")
        c3 = Category(name="Quản trị viên")

        db.session.add_all([c1, c2, c3])  # tạo script
        with open("data/student.json", encoding="utf-8") as f:
            students = json.load(f)

            for p in students:
                stud = Student(**p)
                db.session.add(stud)

        db.session.commit()  # run script
