from bio_scraper import run_perfil
from scraper import run_posts

def main():
    username = input("Ingresa el username: ").strip()

    print("\n🔎 Obteniendo perfil...")
    run_perfil(username)

    print("\n📥 Obteniendo posts...")
    run_posts(username)

if __name__ == "__main__":
    main()