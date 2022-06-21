import base64
import os
from flask import redirect, request
from flask_admin import AdminIndexView, expose
from flask_admin.form import BaseForm
from flask_admin.contrib.sqla import ModelView
import flask_login
from models import News
from module.auth.commands import AuthCommand


class DashboardView(AdminIndexView): 

    @expose('/logout/')
    def logout_view(self):
        flask_login.logout_user()
        return redirect('../')

    @expose('/', methods=('GET', 'POST')) 
    def index(self):
        if request.method == 'POST':
            login = request.form.get('login')
            password = request.form.get('password')
            authCommand = AuthCommand()
            print(login, password)
            try:
                authCommand.login(login, password)
            except:
                return self.render('admin/dashboard_index.html', is_authenticated = False, error=True)
            return redirect('')
        else:
            is_authenticated = flask_login.current_user.is_authenticated
            return self.render('admin/dashboard_index.html', is_authenticated = is_authenticated)
            

class ApproveForm(BaseForm):
    data = {'approved': True}
    

class NotApproveForm(BaseForm):
    data = {'approved': False}
    

class NewsModelView(ModelView):

    details_template = 'admin/news_detail.html'

    column_list = (
        News.id.key,
        News.author.key,
        News.title.key,
        News.category.key,
        News.region.key,
        News.create_at.key,
        News.approved.key
    )

    column_display_pk = True
    can_view_details = True
    can_create = False
    can_delete = False
    can_edit = False

    def is_accessible(self):
        return flask_login.current_user.is_authenticated and flask_login.current_user.role == 2
        
    def inaccessible_callback(self, name, **kwargs):
        return redirect('../')
        
    @expose('/details/')
    def details_view(self):

        return_url = '../'

        if not self.can_view_details:
            return redirect(return_url)

        id = request.args.getlist('id')[0]

        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            return redirect(return_url)

        if self.details_modal and request.args.get('modal'):
            template = self.details_modal_template
        else:
            template = self.details_template

        res_path = f'news_resource_storage/newResourse{id}.png'

        if os.path.exists(res_path):
            with open(res_path, "rb") as res:
                thumb_string = str(base64.b64encode(res.read()))
            resources  = "data:image/jpeg;base64," + str(thumb_string)[2:-1]
        else:
            resources: str = model.resource
            if resources.startswith('assets'):
                resources = 'http://localhost:4200/' + resources

        content = model.content
        return self.render(template,
                           resources=resources,
                           content=content,
                           model=model,
                           details_columns=self._details_columns,
                           get_value=self.get_detail_value,
                           return_url=return_url)
                           
    @expose('/details/approve/<int:news_id>') 
    def approve(self, news_id):
        news = self.get_one(str(news_id))
        if news.approved:
            form = NotApproveForm()
        else:
            form = ApproveForm()
        self.update_model(form, news)
        # Send email
        return redirect(f'../?id={news_id}')

    @expose('/details/delete/<int:news_id>') 
    def delete(self, news_id):
        news = self.get_one(str(news_id))
        self.delete_model(news)
        # Send email
        return redirect(f'../?id={news_id}')
        
    def on_model_change(self, form, model, is_created):
        model.approved = form.data.get('approved')