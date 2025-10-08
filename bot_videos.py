# -*- coding: utf-8 -*-

import asyncio
import os
from telethon.sync import TelegramClient

# --- 1. CONFIGURAÇÃO (Variáveis de Ambiente) ---
# Lendo credenciais e o nome do grupo a partir das variáveis de ambiente
API_ID_STR = os.environ.get('API_ID') 
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
SOURCE_GROUP_ID = os.environ.get('GRUPO_USERNAME') 

# Verifica se TODAS as variáveis necessárias existem
if not all([API_ID_STR, API_HASH, BOT_TOKEN, SOURCE_GROUP_ID]):
    raise ValueError("ERRO: Configure API_ID, API_HASH, BOT_TOKEN, e GRUPO_USERNAME nos Secrets do GitHub.")

# Garante que API_ID é um número inteiro
try:
    API_ID = int(API_ID_STR)
except ValueError:
    raise ValueError("ERRO: O valor de API_ID nos Secrets do GitHub deve ser um número inteiro.")

# Se chegou até aqui, todas as credenciais estão prontas.
client = TelegramClient('bot_session', API_ID, API_HASH)

def gerar_html(videos_data):
    """
    Função para gerar o conteúdo de um arquivo HTML a partir da lista de vídeos.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lista de Vídeos do Telegram</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; margin: 0; padding: 20px; }
            .container { max-width: 800px; margin: auto; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 20px; }
            h1 { text-align: center; color: #1877f2; }
            .video-card { border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px; }
            .video-card a { text-decoration: none; font-weight: bold; color: #1877f2; font-size: 1.1em; }
            .video-card p { margin-top: 8px; color: #606770; white-space: pre-wrap; word-wrap: break-word; }
            footer { text-align: center; margin-top: 20px; font-size: 0.8em; color: #90949c; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏴‍☠ One Piece</h1>
    """

    if not videos_data:
        html_content += "<p>Nenhum vídeo encontrado com os critérios definidos.</p>"
    else:
        for video in videos_data:
            caption_safe = video['caption'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html_content += f"""
            <div class="video-card">
                <a href="{video['video_url']}" target="_blank" rel="noopener noreferrer">Assistir Vídeo (Link Direto)</a>
                <p>{caption_safe}</p>
            </div>
            """
    
    html_content += """
        <footer>Boss B</footer>
        </div>
    </body>
    </html>
    """
    return html_content

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Conexão com o Bot Telegram iniciada.")
    
    # Adicionando um tratamento de erro para garantir que a entidade existe
    try:
        entity = await client.get_entity(SOURCE_GROUP_ID)
    except Exception as e:
        print(f"ERRO: Não foi possível obter a entidade para '{SOURCE_GROUP_ID}'. Verifique o nome do canal/grupo.")
        print(f"Detalhes do erro: {e}")
        await client.disconnect()
        return

    videos_data = []
    limit_msgs = 10000 
    
    print(f"Buscando {limit_msgs} mensagens em '{getattr(entity, 'title', SOURCE_GROUP_ID)}'...")
    
    async for message in client.iter_messages(entity, limit=limit_msgs):
        
        # Filtro de Vídeo: Verifica se o objeto 'video' existe E se tem o atributo 'duration'
        if message.video and hasattr(message.video, 'duration'):
            
            video_duration = message.video.duration
            
            # NOVO FILTRO DE DURAÇÃO: Mínimo 10 minutos (600s) E Máximo 2 horas (7200s)
            if video_duration >= 600 and video_duration <= 7200:
                
                video_url = ""
                if hasattr(message.chat, 'username') and message.chat.username:
                    # Gera o link direto para a mensagem
                    video_url = f"https://t.me/{message.chat.username}/{message.id}"
                else:
                    # Pula a mensagem se o chat não tiver username (privado)
                    continue 

                caption = message.text or "Vídeo sem legenda"
                videos_data.append({"video_url": video_url, "caption": caption})

    print(f"Total de {len(videos_data)} vídeos encontrados.")
    
    print("Gerando arquivo HTML...")
    html_final = gerar_html(videos_data)
    
    # O ficheiro é 'index.html'
    with open('index.html', 'w', encoding='utf-8') as f: 
        f.write(html_final)
        
    print("Arquivo 'index.html' foi criado/atualizado com sucesso!")

    await client.disconnect()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
