from flask_admin import Admin, expose, AdminIndexView, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from werkzeug.utils import redirect

from TruongMauGiao import app, db
from TruongMauGiao.models import Category, Student


class MyCategoryView(ModelView):
    column_list = ['name','hocPhi','students'] #hiển thị những ttin chỉ định
    column_searchable_list = ['name'] #tìm kiếm
    column_filters = ['name'] #bộ lọc
    column_labels = {
        "name": "Tên lớp",
        "hocPhi": "Học phí",
        "students":"Danh sách trẻ"
    }

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self) -> str:
        return self.render('admin/index.html')

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

admin = Admin(app=app, name="Trường Mẫu Giáo", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())

admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyStudentView(Student, db.session))
admin.add_view(MyAdminLogoutView("Đăng xuất"))