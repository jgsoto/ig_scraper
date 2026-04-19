import json
from browser import get_page, close_browser
from perfil import run_perfil
from posts import run_posts
from followers import run_followers, run_following


def mostrar_menu():
    print("\n=== MENÚ ===")
    print("1. Perfil")
    print("2. Posts")
    print("3. Seguidores")
    print("4. Seguidos")
    print("5. Todo")
    print("0. Salir")


def pedir_numero(mensaje, default):
    valor = input(f"{mensaje} (default {default}): ").strip()

    if not valor:
        return default

    try:
        return int(valor)
    except:
        print("Valor inválido, usando default")
        return default


def main():
    username = input("Ingresa el username: ").strip()

    page, context = get_page("https://www.instagram.com")

    data = {}

    try:
        while True:
            mostrar_menu()
            opcion = input("Selecciona una opción: ").strip()

            if opcion == "0":
                print("Saliendo...")
                break

            # =====================
            # PERFIL
            # =====================
            if opcion in ["1", "5"]:
                try:
                    print("\nPerfil...")
                    data["perfil"] = run_perfil(page, username)
                except Exception as e:
                    print("Error perfil:", e)
                    data["perfil"] = None

            # =====================
            # POSTS
            # =====================
            if opcion in ["2", "5"]:
                try:
                    cantidad_posts = pedir_numero("¿Cuántos posts quieres?", 12)

                    # 🔥 límite seguro
                    cantidad_posts = min(cantidad_posts, 100)

                    # 🔥 convertir posts → páginas
                    max_pages = max(1, (cantidad_posts // 12) + 1)

                    print(f"\nPosts (~{cantidad_posts})...")
                    posts = run_posts(username, max_pages=max_pages)

                    # 🔥 recortar exacto
                    data["posts"] = posts[:cantidad_posts]

                except Exception as e:
                    print("Error posts:", e)
                    data["posts"] = []

            # =====================
            # FOLLOWERS
            # =====================
            if opcion in ["3", "5"]:
                try:
                    limite = pedir_numero("¿Cuántos seguidores quieres?", 10)

                    # 🔥 límite seguro
                    limite = min(limite, 50)

                    print("\nSeguidores...")
                    data["followers"] = run_followers(page, username, limit=limite)

                except Exception as e:
                    print("Error followers:", e)
                    data["followers"] = []

            # =====================
            # FOLLOWING
            # =====================
            if opcion in ["4", "5"]:
                try:
                    limite = pedir_numero("¿Cuántos seguidos quieres?", 10)

                    # 🔥 límite seguro
                    limite = min(limite, 50)

                    print("\nSeguidos...")
                    data["following"] = run_following(page, username, limit=limite)

                except Exception as e:
                    print("Error following:", e)
                    data["following"] = []

            # =====================
            # GUARDAR
            # =====================
            with open(f"{username}_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print("\n✅ Datos guardados correctamente")

    finally:
        context.close()
        close_browser()


if __name__ == "__main__":
    main()