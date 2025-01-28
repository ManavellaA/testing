from flask import Blueprint, render_template
import app.functions

oc_create_bp = Blueprint('oc_create', __name__)

@oc_create_bp.route('/OC/crear')
def oc_create():
    empresas = app.functions.get_data_from_json(app.functions.SUPPLIER_FILE)
    tipo = "Proveedor"
    return render_template('form.html', empresas=empresas, tipo=tipo)