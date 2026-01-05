"""Script para testar os principais endpoints da API"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    print_section("1. Testando Health Check")
    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_register():
    print_section("2. Testando Registro de Usuário")
    data = {
        "email": "novo.usuario@test.com",
        "password": "senha123",
        "name": "Novo Usuário Teste"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print(f"Usuário criado: {result['user']['email']}")
        print(f"Token: {result['token']['access_token'][:50]}...")
        return result['token']['access_token']
    elif response.status_code == 409:
        print("⚠ Usuário já existe. Tentando fazer login...")
        return None
    else:
        print(f"❌ Erro: {response.json()}")
        return None

def test_login():
    print_section("3. Testando Login")
    data = {
        "username": "teste@temvagaai.com",  # OAuth2 usa 'username' para email
        "password": "senha123"
    }
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data=data,  # OAuth2 usa form-data
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Login bem-sucedido: {result['user']['email']}")
        print(f"Token: {result['token']['access_token'][:50]}...")
        return result['token']['access_token']
    else:
        print(f"❌ Erro: {response.json()}")
        return None

def test_get_categories(token=None):
    print_section("4. Testando Listagem de Categorias")
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = requests.get(f"{BASE_URL}/categories", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        categories = response.json()
        print(f"✓ {len(categories)} categorias encontradas:")
        for cat in categories[:3]:  # Mostra apenas 3
            print(f"  - {cat['name']} (ID: {cat['id']})")
        return categories[0]['id'] if categories else None
    else:
        print(f"❌ Erro: {response.json()}")
        return None

def test_get_ads():
    print_section("5. Testando Listagem de Anúncios")
    response = requests.get(f"{BASE_URL}/ads")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        ads = response.json()
        print(f"✓ {len(ads)} anúncios encontrados:")
        for ad in ads:
            print(f"  - {ad['title']} (R$ {ad['price']})")
        return ads[0]['id'] if ads else None
    else:
        print(f"❌ Erro: {response.json()}")
        return None

def test_create_ad(token, category_id):
    print_section("6. Testando Criação de Anúncio")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Apartamento Teste via API",
        "description": "Este é um anúncio de teste criado via script Python",
        "seller": "Vendedor Teste",
        "location": "São Paulo - SP",
        "cep": "01310-100",
        "price": 2000.00,
        "category_id": category_id,
        "bedrooms": 2,
        "bathrooms": 1,
        "rules": ["Não fumante"],
        "amenities": ["Wi-Fi", "Garagem"],
        "status": "published"
    }
    
    response = requests.post(f"{BASE_URL}/ads", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        ad = response.json()
        print(f"✓ Anúncio criado com ID: {ad['id']}")
        print(f"  Título: {ad['title']}")
        print(f"  Preço: R$ {ad['price']}")
        return ad['id']
    else:
        print(f"❌ Erro: {response.json()}")
        return None

def test_get_ad_details(ad_id):
    print_section("7. Testando Detalhes do Anúncio")
    response = requests.get(f"{BASE_URL}/ads/{ad_id}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        ad = response.json()
        print(f"✓ Anúncio: {ad['title']}")
        print(f"  Vendedor: {ad['seller']}")
        print(f"  Localização: {ad['location']}")
        print(f"  Preço: R$ {ad['price']}")
        return True
    else:
        print(f"❌ Erro: {response.json()}")
        return False

def test_create_comment(token, ad_id):
    print_section("8. Testando Criação de Comentário")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "ad_id": ad_id,
        "content": "Ótimo anúncio! Estou interessado.",
        "rating": 5
    }
    
    response = requests.post(f"{BASE_URL}/comments", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        comment = response.json()
        print(f"✓ Comentário criado com ID: {comment['id']}")
        print(f"  Conteúdo: {comment['content']}")
        print(f"  Avaliação: {comment['rating']}/5")
        return comment['id']
    else:
        print(f"❌ Erro: {response.json()}")
        return None

def test_toggle_favorite(token, ad_id):
    print_section("9. Testando Adicionar aos Favoritos")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(f"{BASE_URL}/favorites/{ad_id}/toggle", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ {result['message']}")
        print(f"  Favoritado: {result['favorited']}")
        return True
    else:
        print(f"❌ Erro: {response.json()}")
        return False

def test_get_my_favorites(token):
    print_section("10. Testando Listagem de Favoritos")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/favorites", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        favorites = response.json()
        print(f"✓ {len(favorites)} favoritos encontrados:")
        for fav in favorites:
            print(f"  - {fav['title']} (R$ {fav['price']})")
        return True
    else:
        print(f"❌ Erro: {response.json()}")
        return False

def main():
    print("\n" + "🚀"*30)
    print("  TESTADOR DE API - TemVagaAi Backend FastAPI")
    print("🚀"*30)
    
    # 1. Health Check
    if not test_health():
        print("\n❌ API não está rodando! Execute: uvicorn app.main:app --reload")
        return
    
    # 2 e 3. Registrar ou fazer login
    token = test_register()
    if not token:
        token = test_login()
    
    if not token:
        print("\n❌ Não foi possível obter token de autenticação!")
        return
    
    # 4. Listar categorias
    category_id = test_get_categories(token)
    if not category_id:
        print("\n⚠ Nenhuma categoria encontrada. Execute: python init_db.py")
        return
    
    # 5. Listar anúncios
    ad_id = test_get_ads()
    
    # 6. Criar novo anúncio
    new_ad_id = test_create_ad(token, category_id)
    if new_ad_id:
        ad_id = new_ad_id
    
    if ad_id:
        # 7. Ver detalhes do anúncio
        test_get_ad_details(ad_id)
        
        # 8. Criar comentário
        test_create_comment(token, ad_id)
        
        # 9. Adicionar aos favoritos
        test_toggle_favorite(token, ad_id)
        
        # 10. Listar favoritos
        test_get_my_favorites(token)
    
    print("\n" + "✅"*30)
    print("  TESTES CONCLUÍDOS!")
    print("✅"*30)
    print("\n📚 Acesse a documentação completa em: http://localhost:8000/docs")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não foi possível conectar à API!")
        print("Execute o servidor com: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
