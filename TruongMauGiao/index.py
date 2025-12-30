import math
from flask import render_template, request, redirect, session
from flask_login import login_user, current_user, logout_user
import dao
from TruongMauGiao import app, login, admin


@app.route('/')
def index():



    return render_template('index.html', user=current_user)


@app.route('/students/<int:id>')
def details(id):
    stud = dao.get_student_by_id(id)
    return render_template('student_details.html', stud=stud)


@app.context_processor
def common_attribute():
    return {
        "cates": dao.load_categories()
    }


@app.route("/login", methods=['get', 'post'])
def login_my_username():
    if current_user.is_authenticated:
        return redirect('/add_student')

    err_msg = None

    if request.method.__eq__('post'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username, password)

        if user:
            login_user(user)
            return redirect('/add_student')
        else:
            err_msg = " Tai khoan hay mat khau khong hop le!"

    return render_template('login.html', err_msg=err_msg)

@app.route('/logout')
def logout_my_username():
    logout_user()
    return redirect('/')

@app.route('/admin-login', methods=['post'])
def admin_login_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username, password)

    if user:
        login_user(user)
        return redirect('/admin')
    else:
        err_msg = " Tai khoan hay mat khau khong hop le!"

@app.route('/add_student')
def add_student():
    q = request.args.get("q")
    cate_id = request.args.get("cate_id")
    page = request.args.get("page")
    studs = dao.load_students(q=q, cate_id=cate_id, page=page)
    pages = math.ceil(dao.count_student() / app.config["PAGE_SIZE"])
    return render_template('add_student.html', studs=studs, pages=pages)

# @app.route("/api/studs", methods=['post'])
# def add_to_studs():
#     stud = session.get('stud')
#
#     if not stud:
#         stud={}
#
#     id= request.json.get('id')
#
#     if id in stud:
#         error_msg = " Tên trẻ đã có trong danh sách!!"
#     else:
#         stud[id] = {
#             "id": id,
#             "name": request.json.get("name"),
#             "nameParent": request.json.get("nameParent")
#         }


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
