from perfil import run_perfil
from posts import run_posts
import json

def main():
    username = input("Ingresa el username: ").strip()

    if not username:
        print("❌ Username inválido")
        return

    print("\n🔎 Obteniendo perfil...")
    perfil_data = run_perfil(username)

    print("\n📥 Obteniendo posts...")
    posts_data = run_posts(username)

    result = {
        "perfil": perfil_data,
        "posts": posts_data
    }

    filename = f"{username}_data.json"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        print(f"\n💾 Datos guardados en {filename}")

    except Exception as e:
        print("❌ Error guardando archivo:", e)


if __name__ == "__main__":
    main()