import requests
import re
import os
from flask import Flask, Response, render_template_string

app = Flask(__name__)

# Playlists públicas
PLAYLISTS = {
    "global": {"name": "🌍 Global (15k+ canais)", "url": "https://iptv-org.github.io/iptv/index.m3u"},
    "brazil": {"name": "🇧🇷 Brasil", "url": "https://iptv-org.github.io/iptv/countries/br.m3u"},
    "usa": {"name": "🇺🇸 EUA", "url": "https://iptv-org.github.io/iptv/countries/us.m3u"},
    "news": {"name": "📰 Notícias", "url": "https://iptv-org.github.io/iptv/categories/news.m3u"},
    "sports": {"name": "⚽ Esportes", "url": "https://iptv-org.github.io/iptv/categories/sports.m3u"},
    "movies": {"name": "🎥 Filmes e Séries", "url": "https://iptv-org.github.io/iptv/categories/movies.m3u"},
    "free_tv": {"name": "📺 Free TV (Pluto, Roku, etc)", "url": "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8"},
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YCineflix IPTV - TVimate</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f0f0f; color: #fff; margin: 0; padding: 20px; }
        h1 { color: #e50914; text-align: center; }
        .playlist-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }
        .card { background: #1f1f1f; padding: 20px; border-radius: 12px; text-align: center; transition: 0.3s; }
        .card:hover { transform: translateY(-10px); background: #2a2a2a; }
        .card h3 { margin: 10px 0; color: #fff; }
        button { background: #e50914; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 1rem; }
        button:hover { background: #f40612; }
        footer { text-align: center; margin-top: 40px; color: #666; }
    </style>
</head>
<body>
    <h1>🚀 YCineflix IPTV</h1>
    <p style="text-align:center;">Escolha uma playlist e copie o link para o <strong>TVimate</strong></p>
    
    <div class="playlist-grid">
        {% for key, data in playlists.items() %}
        <div class="card">
            <h3>{{ data['name'] }}</h3>
            <a href="/playlist/{{ key }}" target="_blank">
                <button>Copiar Link da Playlist</button>
            </a>
        </div>
        {% endfor %}
    </div>
    
    <footer>
        <p>Feito para TVimate • Playlists públicas • 2026</p>
    </footer>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, playlists=PLAYLISTS)

@app.route('/playlist/<name>')
def get_playlist(name):
    if name not in PLAYLISTS:
        return "Playlist não encontrada", 404
    
    url = PLAYLISTS[name]["url"]
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        content = r.text
    except Exception as e:
        content = f"# Erro ao carregar playlist: {str(e)}"

    content = re.sub(r'#EXTM3U.*?\n', f'#EXTM3U\n# YCineflix IPTV - {PLAYLISTS[name]["name"]}\n', content, count=1)
    
    return Response(content, mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("✅ YCineflix IPTV Server iniciado!")
    print(f"Acesse: http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port)
