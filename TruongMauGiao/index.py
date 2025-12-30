import hashlib
import math

import cloudinary
from flask import render_template, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

import dao
from TruongMauGiao import app, db, login
from TruongMauGiao.decorator import admin_required, staff_required, anonymous_required
from TruongMauGiao.models import UserRole, User, Student


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
    err_msg = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username, password)

        if user:
            login_user(user)
            if user.role == UserRole.ADMIN:
                return redirect('/admin')
            return redirect('/')
        else:
            err_msg = "Tên đăng nhập hoặc mật khẩu không đúng!"

    return render_template("login.html", err_msg=err_msg)


@app.route('/logout')
@login_required
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

@app.route('/add_student', methods=['GET', 'POST'])
def add_student_route():
    q = request.args.get("q")
    cate_id = request.args.get("cate_id")
    page = request.args.get("page")
    studs = dao.load_students(q=q, cate_id=cate_id, page=page)
    pages = math.ceil(dao.count_student() / app.config["PAGE_SIZE"])

    if request.method == 'POST':
        name = request.form['name']
        Lop = request.form['Lop']
        gioiTinh = request.form['gioiTinh']
        nameParent = request.form['nameParent']
        SDT = request.form['SDT']

        # gọi hàm trong dao.py
        dao.add_student(name, Lop, gioiTinh, nameParent, SDT)
        return redirect(url_for('add_student_route'))

    studs = Student.query.all()
    return render_template('add_student.html', studs=studs, pages=pages)


@app.route('/delete_student/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    dao.delete_student(id)
    return redirect('add_student_route')


@app.route('/edit-student/<int:id>', methods=['GET', 'POST'])
def edit_student_route(id):
    if request.method == 'POST':
        dao.edit_student(
            id,
            name=request.form['name'],
            Lop=request.form['Lop'],
            gioiTinh=request.form['gioiTinh'],
            nameParent=request.form['nameParent'],
            SDT=request.form['SDT'])
        return redirect(url_for('add_student_route'))

    hs = Student.query.get(id)
    return render_template('edit_student.html', hs=hs)

@app.route('/delete_student/<int:id>/invoice')
@login_required
def export_invoice(id):
    invoice = dao.get_invoice(id)
    stud= dao.get_student_by_id(id)
    return render_template('invoice.html', stud=stud, invoice=invoice)


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/admin/stats')
@admin_required
def admin_stats():
    class_stats = dao.stats_student_by_category()
    fee_stats = dao.stats_fee_by_month()

    return render_template(
        'admin/stats.html',
        class_stats=class_stats,
        fee_stats=fee_stats
    )


@app.route("/register", methods=['GET', 'POST'])
def register():
    err_msg = None

    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        avatar = request.files.get("avatar")

        # 1. Kiểm tra mật khẩu
        if password != confirm:
            err_msg = "Mật khẩu không khớp!"
            return render_template("register.html", err_msg=err_msg)

        # 2. Upload avatar (nếu có)
        avatar_url = None
        if avatar and avatar.filename:
            res = cloudinary.uploader.upload(avatar)
            avatar_url = res["secure_url"]

        # 3. Tạo user và bắt trùng username
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            err_msg = "Tên đăng nhập đã tồn tại!"
            return render_template("register.html", err_msg=err_msg)

        dao.register_user(name, username, password, avatar_url)
        return redirect("/login")

    return render_template("register.html", err_msg=err_msg)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    success_msg = None
    err_msg = None

    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        avatar_file = request.files.get("avatar")

        # Kiểm tra mật khẩu
        if password:
            if password != confirm:
                err_msg = "Mật khẩu không trùng!"
                return render_template("profile.html", err_msg=err_msg)

            current_user.password = hashlib.md5(password.encode("utf-8")).hexdigest()

        # Cập nhật tên
        current_user.name = name

        # Cập nhật avatar
        if avatar_file and avatar_file.filename:
            res = cloudinary.uploader.upload(avatar_file)
            current_user.avatar = res["secure_url"]

        db.session.commit()
        success_msg = "Cập nhật thành công!"

    return render_template("profile.html", success_msg=success_msg, err_msg=err_msg)


@app.route("/students/<int:id>/health", methods=['get', 'post'])
@staff_required
def health_record(id):
    stud = dao.get_student_by_id(id)

    if request.method == 'POST':
        weight = float(request.form.get("weight"))
        temperature = float(request.form.get("temperature"))
        note = request.form.get("note")

        dao.add_health_record(id, weight, temperature, note)
        return redirect(f"/students/{id}/health")

    records = dao.load_health_records(id)
    return render_template("health_record.html", stud=stud, records=records)


@app.route("/health/<int:id>/edit", methods=['post'])
def edit_health(id):
    weight = float(request.form.get("weight"))
    temperature = float(request.form.get("temperature"))
    note = request.form.get("note")

    record = dao.update_health_record(id, weight, temperature, note)
    return redirect(f"/students/{record.student_id}/health")


@app.route("/health/<int:id>/delete")
def delete_health(id):
    record = dao.get_health_record_by_id(id)
    student_id = record.student_id
    dao.delete_health_record(id)
    return redirect(f"/students/{student_id}/health")


if __name__ == '__main__':
    app.run(debug=True)
