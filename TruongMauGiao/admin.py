from flask_admin import Admin, expose, AdminIndexView, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from sqlalchemy import func, extract
from werkzeug.utils import redirect

from TruongMauGiao import app, db
from TruongMauGiao.models import Category, Student, UserRole


class MyCategoryView(ModelView):

    column_list = ['name','hocPhi','students']
    column_searchable_list = ['name']
    column_filters = ['name']
    column_labels = {
        "name": "Tên lớp",
        "hocPhi": "Học phí",
        "students":"Danh sách trẻ"
    }

    def is_accessible(self):
        return (
            current_user.is_authenticated
            and current_user.role == UserRole.ADMIN
        )

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')



class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return (
            current_user.is_authenticated
            and current_user.role == UserRole.ADMIN
        )

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')

class MyStudentView(ModelView):
    column_list = ['name','nameParent','category.name']
    column_searchable_list = ['name']
    column_filters = ['name']
    column_labels = {
        "name": "Tên trẻ",
        "nameParent": "Tên phụ huynh",
        "category.name": "Lớp"
    }

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class MyAdminLogoutView(BaseView):
    @expose('/')
    def index(self) -> str:
        logout_user()
        return redirect('/admin')

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class StatsView(BaseView):
    @expose('/')
    def index(self):

        # 1. Sĩ số từng lớp
        class_stats = db.session.query(
            Category.name,
            func.count(Student.id)
        ).join(Student).group_by(Category.id).all()

        # 2. Tổng thu theo tháng (ví dụ: dựa theo created_date của Student)
        fee_stats = db.session.query(
            extract('month', Student.created_date),
            func.sum(Category.hocPhi)
        ).join(Category).group_by(
            extract('month', Student.created_date)
        ).all()

        # # 3. Tỷ lệ nam / nữ
        # gender_stats = db.session.query(
        #     Student.gender,
        #     func.count(Student.id)
        # ).group_by(Student.gender).all()

        return self.render(
            'admin/stats.html',
            class_stats=class_stats,
            fee_stats=fee_stats,
            # gender_stats=gender_stats
        )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.ADMIN


admin = Admin(app=app, name="Trường Mẫu Giáo", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())

admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyStudentView(Student, db.session))
admin.add_view(StatsView("Thống kê"))
admin.add_view(MyAdminLogoutView("Đăng xuất"))
