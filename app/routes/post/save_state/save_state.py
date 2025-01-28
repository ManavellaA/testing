from flask import Blueprint, request, jsonify
import app.functions
from datetime import datetime

save_state_bp = Blueprint('save_state', __name__)

@save_state_bp.route('/guardar-estado', methods=['POST'])
def save_state():
    data = request.json
    tipo = data.get("ref")
    ref = ""    
    if tipo == 'Seguimiento de OC':
        ref = app.functions.INDEX_SUPPLIER_PATH
    
    elif tipo == 'Seguimiento de Presupuestos':
        ref = app.functions.INDEX_BUDGET_PATH
        
    json_index = app.functions.get_data_from_json(ref)
    
    if json_index is None:
        return jsonify({"message": "El archivo de índice no existe"}), 409
    numero = data.get('Numero')
    estado = data.get('Estado')
    Dolar_b = data.get("DolarBillete")
    Dolar_d = data.get("DolarDivisa")
    
    if Dolar_b is not None:
        # Eliminar el símbolo de moneda y los espacios
        val_b_limpio = Dolar_b.replace('$', '').replace(' ', '').replace(',', '.')
        Dolar_b = float(val_b_limpio)
    else:
        print("Error: 'DolarBillete' no proporcionado o es None")
        return jsonify({"message": "DolarBillete no proporcionado"}), 400
    
    if Dolar_d is not None:
        # Eliminar el símbolo de moneda y los espacios
        val_d_limpio = Dolar_d.replace('$', '').replace(' ', '').replace(',', '.')
        Dolar_d = float(val_d_limpio)
    else:
        print("Error: 'DolarDivisa' no proporcionado o es None")
        return jsonify({"message": "DolarDivisa no proporcionado"}), 400
    moneda_valor = Dolar_b  # Valor por defecto en caso de que no se encuentre el tipo de moneda
    
    for item in json_index:
        if item.get('Numero') == numero:
            if item.get("Moneda_tipo") == "U$DB":
                moneda_valor = Dolar_b
            elif item.get("Moneda_tipo") == "U$DD":
                moneda_valor = Dolar_d
            item['Estado'] = estado
            item['Moneda_cambio'] = moneda_valor
            item['Fecha_estado'] = datetime.now().strftime('%d/%m/%Y')
            app.functions.save_json(ref, json_index)  # Guarda el JSON actualizado
            return jsonify({"message": "Estado actualizado con éxito"}), 200
    
    return jsonify({"message": "No se encontró el número especificado"}), 404