from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'CORBATAS_VIDRIO_EN_CIELOS_DE_MIEL_UN_GOLEM_REFLEJADO_EN_EL_ALEPH'

API_KEY = "1320e414b5414686ac59e14362f5a2d3"
API_BASE = "https://api.spoonacular.com"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=["POST"])
def buscar():
    ingrediente = request.form.get('ingrediente', '').strip().lower()
    
    if not ingrediente:
        flash('Ingresa un ingrediente', 'error')
        return redirect(url_for('index'))
    try:
        search_url = f"{API_BASE}/food/ingredients/search"
        params = {'apiKey': API_KEY,
                  'query': ingrediente, 
                  'number': 1}
        resp = requests.get(search_url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            if data['results']:
                ingrediente_id = data['results'][0]['id']             
                info_url = f"{API_BASE}/food/ingredients/{ingrediente_id}/information"
                info_params = {'apiKey': API_KEY,
                               'amount': 100,
                               'unit': 'grams'}
                info_resp = requests.get(info_url, params=info_params)
                if info_resp.status_code == 200:
                    info_data = info_resp.json() 
                    ingrediente_info = {
                        'nombre': info_data['name'].title(),
                        'imagen': f"https://spoonacular.com/cdn/ingredients_250x250/{info_data['image']}",
                    }    
                    nutrientes = info_data.get('nutrition', {}).get('nutrients', [])
                    ingrediente_info['nutricion'] = {
                        'calorias': next((n['amount'] for n in nutrientes if n['name'] == 'Calories'), 'N/A'),
                        'proteina': next((n['amount'] for n in nutrientes if n['name'] == 'Protein'), 'N/A'),
                        'carbohidratos': next((n['amount'] for n in nutrientes if n['name'] == 'Carbohydrates'), 'N/A'),
                        'grasas': next((n['amount'] for n in nutrientes if n['name'] == 'Fat'), 'N/A')
                    }
                    return render_template('ingrediente.html', ingrediente=ingrediente_info)
            flash('Ingrediente no encontrado', 'error')
            return redirect(url_for('index'))
        else:
            flash('Error en la búsqueda', 'error')
            return redirect(url_for('index'))          
    except Exception as e:
        flash('Error de conexión', 'error')
        return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)