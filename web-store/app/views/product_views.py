from flask import request, flash
from app.views.shared_works import ViewResult, set_login_user, check_role
from app import app
from app.model.product import Laptop
from app.model.db_service import product_services
from app.model.input_model.product_form import LaptopForm


@app.route('/product/laptop/create', methods=['GET', 'POST'])
@check_role('admin')
@set_login_user
def create_laptop():
    form = LaptopForm()
    if request.method == 'POST' and form.validate():
        new_laptop = Laptop(product_code=form.product_code.data,
                            product_name=form.name.data,
                            description=form.description.data,
                            main_image=form.main_image.data,
                            price=form.price.data,
                            warranty=form.warranty.data,
                            manufacture=form.manufacture.data,
                            images=None,
                            comments=None,
                            promotion=form.promotion.data,
                            processor=form.processor.data,
                            memory=form.memory.data,
                            storage=form.storage.data,
                            graphic_card=form.graphic_card.data,
                            screen=form.screen.data
                            )
        service = product_services.DbService()
        service.add_new_laptop(new_laptop=new_laptop)
        flash('Create laptop ' + new_laptop.product_name + 'successuf!')
        return ViewResult('laptop_index.html', model={}, option='redirect', redirect_dest='laptop_index')
    model = {'form': form, 'title': 'Create new Laptop'}
    return ViewResult('create_laptop.html', model)


@app.route('/laptop/index')
@set_login_user
def laptop_index():
    model = {'title': 'Laptop'}
    service = product_services.DbService()
    hot_sale_product_list = service.get_laptop_list()
    model = {'product_list': hot_sale_product_list, 'title': 'Home page'}

    return ViewResult('laptop_index.html', model)


@app.route('/laptop/detail/<string:product_code>')
@set_login_user
def laptop_detail(product_code):
    service = product_services.DbService()
    laptop_detail = service.get_laptop_detail(product_code)
    if laptop_detail is None:
        model = {'title': 'Error' + product_code}
        return ViewResult('laptop_error.html', model)
    else:
        model = {'laptop': laptop_detail, 'title': 'Home page'}
        return ViewResult('laptop_detail.html', model)
