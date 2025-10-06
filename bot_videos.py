# bot_videos.py (Versão Otimizada para Streaming e Bot Token)

import os
import asyncio
from telethon import TelegramClient
# NOVO: Adicionamos BOT_TOKEN, que será injetado pelo GitHub Actions
from config import API_ID, API_HASH, GRUPO_USERNAME, HTML_FILE, BOT_TOKEN 
from telethon.tl.types import MessageMediaDocument

# --- Configurações ---
VIDEO_FOLDER = 'videos' 
MESSAGE_LIMIT = 10000 

def generate_html(video_data):
    """
    Gera o conteúdo HTML da página para exibir os vídeos.
    video_data é uma lista de dicionários com 'title' e 'link' (URL temporária).
    """
    
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Black Channel</title> 
    <style>
        body {{ font-family: sans-serif; padding: 20px; background-color: #f4f4f9; }}
        h1 {{ 
            font-size: 3.5em; 
            color: #0088cc; 
            text-align: left; 
            margin-top: 20px;
            margin-bottom: 50px;
            padding-left: 15px; 
            position: relative; 
            display: inline-block; 
            cursor: pointer; 
            text-shadow: 4px 4px 6px rgba(0, 0, 0, 0.5); 
            transition: color 0.4s ease-in-out, transform 0.4s ease-in-out; 
            animation: slideIn 1.5s ease-out forwards;
        }}
        h1:hover {{
            color: #ff4500;
            transform: scale(1.02);
            text-decoration: none; 
        }}
        @keyframes slideIn {{
            0% {{
                transform: translateX(-150%);
                opacity: 0;
            }}
            100% {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px; 
            max-width: 1200px;
            margin: 0 auto;
        }}
        .video-card {{ 
            background-color: #ffffff; 
            border: 1px solid #ddd; 
            border-radius: 10px; 
            overflow: hidden; 
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        }}
        .video-card:hover {{
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); 
            transform: scale(1.005); 
        }}
        .video-card h2 {{ 
            padding: 10px; 
            font-size: 1.1em; 
            color: #333; 
            margin: 0; 
            text-align: center;
            background-color: #eee;
            border-bottom: 1px solid #ddd;
        }}
        video {{ 
            width: 100%; 
            height: auto; 
            display: block; 
            background-color: #000;
        }}
    </style>
</head>
<body>
    <h1>Black Channel</h1>
    <div class="grid-container">

"""
    # Geração dos elementos de vídeo
    for video in video_data: 
        title = video['title']
        video_url = video['link'] 

        html_content += f"""
        <div class="video-card">
            <h2>{title}</h2>
            <video controls preload="metadata">
                <source src="{video_url}" type="video/mp4">
                Seu navegador não suporta a tag de vídeo.
            </video>
        </div>

"""
    # Fim do HTML
    html_content += """
    </div> <p style="text-align: center; margin-top: 40px; color: #777;">Site atualizado automaticamente pelo Bot.</p>
</body>
</html>
"""

    return html_content


async def main():
    if not os.path.exists(VIDEO_FOLDER):
        os.makedirs(VIDEO_FOLDER)

    # Conexão com o Telegram
    # Usa API_ID e API_HASH (placeholders) e o Bot Token (real)
    client = TelegramClient('bot_session', API_ID, API_HASH)
    
    # Inicia a conexão, usando o token do bot, que é não interativo!
    await client.start(bot_token=BOT_TOKEN) 
    print("Conexão com o Bot Telegram iniciada.")

    # Tenta encontrar a entidade do grupo
    try:
        # ATENÇÃO: O bot PRECISA estar no grupo ou canal (como admin ou membro)
        entity = await client.get_entity(GRUPO_USERNAME)
    except Exception as e:
        print(f"Erro ao encontrar a entidade do grupo '{GRUPO_USERNAME}': {e}")
        await client.disconnect()
        return

    print(f"Buscando {MESSAGE_LIMIT} mensagens no grupo/canal...")
    
    videos_to_display = []

    # Itera sobre as últimas mensagens
    async for message in client.iter_messages(entity, limit=MESSAGE_LIMIT):
        if message.video:
            
            # LÓGICA DE OBTENÇÃO DO TÍTULO
            caption = message.text or message.media.caption
            
            if caption:
                safe_title = "".join(c for c in caption if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')
                title = safe_title[:50] 
            else:
                title = f"Vídeo ID {message.id}"
                
            display_title = title.replace('_', ' ')

            # CORREÇÃO: Usa o método client.get_url() para gerar o link de streaming
            video_url = await client.get_url(message)
            
            print(f"Vídeo encontrado: '{display_title}'. URL temporária gerada.")
            
            # Adiciona os dados do vídeo à lista
            videos_to_display.append({
                'title': display_title,
                'link': video_url
            })


    # --- Geração do Site ---
    print("Gerando o arquivo HTML...")

    # Gera o HTML usando a lista de dicionários
    html_content = generate_html(videos_to_display)

    # Salva o arquivo HTML
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Site atualizado! Arquivo '{HTML_FILE}' gerado com {len(videos_to_display)} vídeos.")

    # Desconecta do Telegram
    await client.disconnect()

if __name__ == '__main__':
    # Roda a função assíncrona principal
    asyncio.run(main())
