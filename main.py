import json
import time
import random
from cookies import load_cookies_playwright
from engagement import calculate_engagement
from browser import get_page, close_browser
from perfil import run_perfil
from posts import run_posts, get_comments_playwright
from followers import run_followers, run_following

cookies = load_cookies_playwright()

def mostrar_menu():
    print("\n=== MENÚ ===")
    print("1. Perfil")
    print("2. Posts")
    print("3. Seguidores")
    print("4. Seguidos")
    print("5. Engagement")
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

            if opcion == "1":
                try:
                    print("\nPerfil...")
                    data["perfil"] = run_perfil(page, username)
                except Exception as e:
                    print("Error perfil:", e)
                    data["perfil"] = None

            if opcion == "2":
                try:
                    cantidad_posts = pedir_numero("¿Cuántos posts quieres?", 12)

                    cantidad_posts = min(cantidad_posts, 100)

                    max_pages = max(1, (cantidad_posts // 12) + 1)

                    print(f"\nPosts (~{cantidad_posts})...")
                    posts = run_posts(username, max_pages=max_pages)

                    posts = posts[:cantidad_posts]

                    for i, post in enumerate(posts):
                        print(f"\n[+] ({i+1}/{len(posts)}) Comentarios de: {post['shortcode']}")

                        try:
                            comments = get_comments_playwright(post["url"])
                            post["comments_data"] = comments
                        except Exception as e:
                            print("Error comentarios:", e)
                            post["comments_data"] = []

                        time.sleep(random.uniform(3, 6))

                    data["posts"] = posts

                except Exception as e:
                    print("Error posts:", e)
                    data["posts"] = []

            if opcion == "3":
                try:
                    limite = pedir_numero("¿Cuántos seguidores quieres?", 10)

                    limite = min(limite, 50)

                    print("\nSeguidores...")
                    data["followers"] = run_followers(page, username, limit=limite)

                except Exception as e:
                    print("Error followers:", e)
                    data["followers"] = []

            if opcion == "4":
                try:
                    limite = pedir_numero("¿Cuántos seguidos quieres?", 10)

                    limite = min(limite, 50)

                    print("\nSeguidos...")
                    data["following"] = run_following(page, username, limit=limite)

                except Exception as e:
                    print("Error following:", e)
                    data["following"] = []

            if opcion == "5":
                try:

                    if "posts" not in data or not data["posts"]:
                        print("Primero debes obtener posts")
                        continue

                    followers = None

                    # 🔥 obtener followers del perfil
                    if "perfil" in data and data["perfil"]:
                        followers = data["perfil"].get("followers")

                    if not followers:
                        print("No hay datos de followers, ejecuta opción 1 (perfil)")

                    print("\nCalculando engagement...")
                    data["engagement"] = calculate_engagement(
                        data["posts"], followers=followers
                    )

                    print("Engagement calculado")

                except Exception as e:
                    print("Error engagement:", e)

            with open(f"{username}_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print("\nDatos guardados correctamente")

    finally:
        context.close()
        close_browser()


if __name__ == "__main__":
    main()