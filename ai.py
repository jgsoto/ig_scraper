import os
from openai import OpenAI
import dotenv

dotenv.load_dotenv()


class IAAnalisisPerfil:

    def __init__(self):
        self.api_key = os.environ.get("GROQCLOUD_API_KEY")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1",
        )

    def analizar(self, posts):

        texto_posts = []

        for post in posts:
            bloque = f"POST:\n{post['caption']}\nCOMENTARIOS:\n"

            for c in post.get("comments", []):
                bloque += f"- {c['text']}\n"

            texto_posts.append(bloque)

        contenido = "\n\n".join(texto_posts[:5])  # limitar

        prompt = f"""
        Analyze this Instagram profile based on posts and comments.

        Return a structured analysis in Spanish:

        - Tipo de contenido (personal, marketing, lifestyle, etc)
        - Tono (emocional, promocional, motivacional, etc)
        - Recepciòn (en base a los comentarios)
        - Audiencia (qué tipo de personas interactúan)
        - Nivel de engagement (alto, medio, bajo)
        - Temas principales
        - Insight general del perfil

        DATA:
        {contenido}
        """

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print("Error IA:", e)
            return None