from flask import Flask, render_template, request
import random
import requests

app = Flask(__name__)

# Configuração com tradução para a API buscar a foto certa
caes_config = {
    "Labrador": "labrador",
    "Pastor Alemão": "germanshepherd",
    "Golden Retriever": "retriever/golden",
    "Poodle": "poodle/standard",
    "Beagle": "beagle",
    "Pug": "pug",
    "Boxer": "boxer",
    "Chihuahua": "chihuahua",
    "Doberman": "doberman",
    "Bulldog": "bulldog",
    "Yorkshire": "yorkshire",
    "Shih Tzu": "shih",
    "Rottweiler": "rottweiler",
    "Dachshund": "dachshund",
    "Schnauzer": "schnauzer",
    "Border Collie": "collie/border"
}

gatos_config = {
    "Siamês": "siam",
    "Persa": "pers",
    "Maine Coon": "mcoo",
    "Bengal": "beng",
    "Sphynx": "sphy",
    "Ragdoll": "ragd",
    "Siberiano": "sibe",
    "Abissínio": "abys",
    "Scottish Fold": "scot",
    "British Shorthair": "bsho",
    "Norwegian Forest": "norw",
    "Devon Rex": "drex",
    "Oriental": "orie",
    "Russian Blue": "rblu",
    "Egyptian Mau": "emau",
    "Turkish Angora": "tang"
}

dados_gerais = {
    "nomes_m": ["Max", "Charlie", "Rex", "Thor", "Toby", "Oliver", "Simba", "Zeca"],
    "nomes_f": ["Luna", "Bella", "Mel", "Amora", "Mimi", "Nala", "Mia", "Nina"],
    "cores": ["Castanho", "Preto", "Branco", "Dourado", "Cinzento", "Laranja", "Manchado"],
    "personalidades": ["Muito Brincalhão", "Preguiçoso", "Um pouco assustado", "Muito protetor", "Adora mimos", "Energético"]
}

def obter_foto(tipo, raca_pt):
    try:
        if tipo == 'cao':
            raca_en = caes_config[raca_pt]
            url = f"https://dog.ceo/api/breed/{raca_en}/images/random"
            res = requests.get(url).json()
            return res.get('message')
        else:
            raca_en = gatos_config[raca_pt]
            url = f"https://api.thecatapi.com/v1/images/search?breed_ids={raca_en}"
            res = requests.get(url).json()
            if res and len(res) > 0:
                return res[0].get('url')
            return "https://placeholder.com"
    except Exception as e:
        print(f"Erro ao procurar foto: {e}")
        return "https://placeholder.com"

@app.route('/', methods=['GET', 'POST'])
def home():
    pet = None
    if request.method == 'POST':
        nome_usuario = request.form.get('nome')
        tipo_pet = request.form.get('tipo') 

        if nome_usuario:
            sexo = random.choice(["Macho", "Fêmea"])
            nome_pet = random.choice(dados_gerais["nomes_m"] if sexo == "Macho" else dados_gerais["nomes_f"])
            
            lista_racas = list(caes_config.keys()) if tipo_pet == 'cao' else list(gatos_config.keys())
            raca_escolhida = random.choice(lista_racas)
            
            # Unifiquei todos os dados aqui para não perder informações
            pet = {
                "dono": nome_usuario,
                "tipo": "Cão" if tipo_pet == "cao" else "Gato",
                "nome": nome_pet,
                "raca": raca_escolhida,
                "idade": f"{random.randint(1, 15)} anos",
                "cor": random.choice(dados_gerais["cores"]),
                "sexo": sexo,
                "personalidade": random.choice(dados_gerais["personalidades"]),
                "foto": obter_foto(tipo_pet, raca_escolhida),
                # Links filtrados do Adopta-me (type 1 para cães, 2 para gatos)
                "link_adocao": "https://adopta-me.org" if tipo_pet == "cao" else "https://adopta-me.org"
            }
            
    return render_template('index.html', pet=pet)

if __name__ == '__main__':
    app.run(debug=True)
