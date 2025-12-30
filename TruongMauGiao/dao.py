import hashlib
import json
import os

from sqlalchemy import func
from werkzeug.utils import secure_filename

from TruongMauGiao import app, db
from TruongMauGiao.models import Category, Student, User, HealthRecord, UserRole


def load_categories():
    # with open("data/category.json", encoding="utf-8") as f:
    #     return json.load(f)
    return Category.query.all()

def count_student():
    return Student.query.count()


def load_students(q=None, cate_id=None, page=None):
    # with open("data/student.json", encoding="utf-8") as f:
    #     student = json.load(f)
    #
    #     if q:
    #         students = [p for p in students if p["name"].find(q) >= 0]
    #
    #     if cate_id:
    #         students = [p for p in students if p["cate_id"].__eq__(int(cate_id))]
    #
    #     return students
    query = Student.query

    if q:
        query = query.filter(Student.name.contains(q))

    if cate_id:
        query = query.filter(Student.cate_id.__eq__(int(cate_id)))

    if page:
        size = app.config["PAGE_SIZE"]
        start= (int(page)-1)*size
        query=query.slice(start,(start+size))

    return query.all()

def auth_user(username, password):
    password=hashlib.md5(password.encode('utf-8')).hexdigest()
    return User.query.filter(User.username.__eq__(username), User.password.__eq__(password) ).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def register_user(name, username, password, avatar=None):
    # kiểm tra username tồn tại
    if User.query.filter_by(username=username.strip()).first():
        return None   # báo trùng
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    if not avatar:
        avatar = "https://static.vecteezy.com/system/resources/previews/005/544/753/original/profile-icon-design-free-vector.jpg"
    u = User(name=name,username=username.strip(),password=password,avatar=avatar)
    db.session.add(u)
    db.session.commit()
    return u


def get_student_by_id(id):
    # with open("data/student.json", encoding="utf-8") as f:
    #     students = json.load(f)
    #
    #     for p in students:
    #         if p["id"].__eq__(id):
    #             return p
    #
    #     return None
    return Student.query.get(id)

def get_health_record_by_id(id):
    return HealthRecord.query.get(id)

def load_health_records(student_id):
    return HealthRecord.query.filter(
        HealthRecord.student_id.__eq__(student_id)
    ).order_by(
        HealthRecord.record_date.desc()
    ).all()

def add_health_record(student_id, weight, temperature, note=None):
    h = HealthRecord(
        student_id=student_id,
        weight=weight,
        temperature=temperature,
        note=note
    )

    db.session.add(h)
    db.session.commit()

    return h

def update_health_record(id, weight, temperature, note):
    h = HealthRecord.query.get(id)

    if h:
        h.weight = weight
        h.temperature = temperature
        h.note = note
        h.is_fever = temperature > 37.5
        db.session.commit()

    return h

def delete_health_record(id):
    h = HealthRecord.query.get(id)

    if h:
        db.session.delete(h)
        db.session.commit()

def stats_student_by_category():
    return db.session.query(
        Category.name,
        func.count(Student.id)
    ).join(Student).group_by(Category.id).all()

def stats_fee_by_month():
    return db.session.query(
        func.month(Student.created_date),
        func.sum(Category.hocPhi)
    ).join(Category).group_by(
        func.month(Student.created_date)
    ).all()



if __name__ == "__main__":
    print(auth_user("user","123"))
