import hashlib
import json

from TruongMauGiao import app
from TruongMauGiao.models import Category, Student, User


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

if __name__ == "__main__":
    print(auth_user("user","123"))
