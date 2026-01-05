"""Script para inicializar o banco de dados com dados iniciais"""
from app.db.database import engine, SessionLocal
from app.db.models import Base, Category, User, Ad
from app.core.security import get_password_hash
import json

def init_db():
    """Cria as tabelas e insere dados iniciais"""
    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tabelas criadas com sucesso!")
    
    db = SessionLocal()
    
    try:
        # Verifica se já existem categorias
        existing_categories = db.query(Category).count()
        if existing_categories == 0:
            print("\nCriando categorias padrão...")
            categories = [
                Category(name="Apartamento", slug="apartamento", description="Apartamentos para alugar"),
                Category(name="Casa", slug="casa", description="Casas para alugar"),
                Category(name="Kitnet", slug="kitnet", description="Kitnets e quitinetes"),
                Category(name="Quarto", slug="quarto", description="Quartos para alugar"),
                Category(name="Residencial", slug="residencial", description="Outros imóveis residenciais"),
            ]
            
            for category in categories:
                db.add(category)
            
            db.commit()
            print(f"✓ {len(categories)} categorias criadas!")
        else:
            print(f"\n⚠ Já existem {existing_categories} categorias no banco")
        
        # Verifica se já existe usuário de teste
        existing_users = db.query(User).count()
        if existing_users == 0:
            print("\nCriando usuário de teste...")
            test_user = User(
                email="teste@temvagaai.com",
                name="Usuário Teste",
                hashed_password=get_password_hash("senha123")
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print("✓ Usuário de teste criado!")
            print("  Email: teste@temvagaai.com")
            print("  Senha: senha123")
            
            # Cria alguns anúncios de exemplo
            print("\nCriando anúncios de exemplo...")
            category_apartamento = db.query(Category).filter(Category.slug == "apartamento").first()
            category_casa = db.query(Category).filter(Category.slug == "casa").first()
            
            if category_apartamento and category_casa:
                ads = [
                    Ad(
                        title="Apartamento 2 quartos no centro",
                        description="Lindo apartamento de 2 quartos próximo ao shopping. Totalmente mobiliado com armários planejados.",
                        seller="João Silva",
                        location="Centro, São Paulo - SP",
                        cep="01310-100",
                        price=2500.00,
                        category_id=category_apartamento.id,
                        user_id=test_user.id,
                        bedrooms=2,
                        bathrooms=1,
                        rules=json.dumps(["Não fumante", "Sem animais"]),
                        amenities=json.dumps(["Wi-Fi", "Garagem", "Academia"]),
                        images=json.dumps(["https://via.placeholder.com/800x600"]),
                        status="published"
                    ),
                    Ad(
                        title="Casa espaçosa com quintal",
                        description="Casa ampla com 3 quartos, 2 banheiros e quintal grande. Ótima localização próxima a escolas e mercados.",
                        seller="Maria Santos",
                        location="Jardim América, Belo Horizonte - MG",
                        cep="30180-000",
                        price=3200.00,
                        category_id=category_casa.id,
                        user_id=test_user.id,
                        bedrooms=3,
                        bathrooms=2,
                        rules=json.dumps(["Aceita animais"]),
                        amenities=json.dumps(["Quintal", "Churrasqueira", "Garagem para 2 carros"]),
                        images=json.dumps(["https://via.placeholder.com/800x600"]),
                        status="published"
                    )
                ]
                
                for ad in ads:
                    db.add(ad)
                
                db.commit()
                print(f"✓ {len(ads)} anúncios de exemplo criados!")
        else:
            print(f"\n⚠ Já existem {existing_users} usuários no banco")
        
        print("\n✅ Banco de dados inicializado com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro ao inicializar banco: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
