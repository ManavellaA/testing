from flask import Blueprint, render_template
import os
import app.functions

chapa_bp = Blueprint('chapa', __name__)

@chapa_bp.route('/chapa')
def chapaStock():
    file = "CHAPAS EN STOCK"
    Sheet_name = "STOCK CUGERONE"
    fileTipe = str(file + ".xlsx")
    app.functions.convert_file(os.path.join(app.functions.DIRECTORY_DRIVE, fileTipe), app.functions.DIRECTORY_JSON, Sheet_name)
    data = app.functions.get_data_from_json(os.path.join(app.functions.DIRECTORY_JSON, str(file + "-" + Sheet_name + ".json")))
    order = ["ESPESOR", "MATERIAL Y MEDIDAS", "CANTIDAD TOTAL"]
    title = "Stock Chapa"
    
    return render_template('tabla.html', data=data, order=order, title=title)
