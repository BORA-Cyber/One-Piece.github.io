# -*- coding: utf-8 -*-

import asyncio
import os
import base64
from telethon.sync import TelegramClient
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()

# --- 1. CONFIGURAÇÃO (Variáveis de Ambiente) ---
API_ID_STR = os.environ.get('API_ID') 
API_HASH = os.environ.get('API_HASH')
SOURCE_GROUP_ID = os.environ.get('GRUPO_USERNAME') 

if not all([API_ID_STR, API_HASH, SOURCE_GROUP_ID]):
    raise ValueError("ERRO: Certifica-te que preencheste API_ID, API_HASH, e GRUPO_USERNAME no ficheiro .env.")

try:
    API_ID = int(API_ID_STR)
except ValueError:
    raise ValueError("ERRO: O valor de API_ID no ficheiro .env deve ser um número inteiro.")

# Inicializa o cliente com as configurações de estabilidade
client = TelegramClient(
    'my_account', 
    API_ID, 
    API_HASH, 
    # Configurações de estabilidade para evitar falhas no download de media no GitHub Actions
    connection_retries=10,  
    retry_delay=5,          
    timeout=30              
)

def gerar_html(videos_data):
    """
    Função para gerar o conteúdo de um arquivo HTML em formato de grelha.
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
            .container { max-width: 1200px; margin: auto; }
            h1 { text-align: center; color: #1877f2; margin-bottom: 30px; }

            /* --- ESTILO DE GRELHA (GRID) --- */
            .grid-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }
            .video-card {
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                overflow: hidden; /* Garante que a miniatura não vaze */
                transition: transform 0.2s;
            }
            .video-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }
            .video-content {
                padding: 15px;
            }
            .video-card a {
                text-decoration: none;
                font-weight: bold;
                color: #1877f2;
                font-size: 1.1em;
                display: block; /* Ocupa toda a área para ser clicável */
            }
            .video-card img {
                width: 100%;
                height: auto;
                display: block;
                object-fit: cover; /* Assegura que a imagem preenche o espaço */
                border-bottom: 1px solid #eee;
            }
            .video-card p { 
                margin-top: 8px; 
                color: #606770; 
                white-space: pre-wrap; 
                word-wrap: break-word; 
                font-size: 0.9em;
                max-height: 4.5em; /* Limita a legenda a cerca de 3 linhas */
                overflow: hidden;
            }
            footer { text-align: center; margin-top: 30px; font-size: 0.8em; color: #90949c; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎬ONE PIECE</h1>
    """

    if not videos_data:
        html_content += "<p>Nenhum vídeo encontrado com os critérios definidos.</p>"
    else:
        html_content += "<div class='grid-container'>"
        for video in videos_data:
            caption_safe = video['caption'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            # Formato do link de miniatura:
            thumbnail_tag = f'<img src="data:image/jpeg;base64,{video["thumbnail_b64"]}" alt="Miniatura do Vídeo">' if video['thumbnail_b64'] else ''
            
            html_content += f"""
            <div class="video-card">
                <a href="{video['video_url']}" target="_blank" rel="noopener noreferrer">
                    {thumbnail_tag}
                </a>
                <div class="video-content">
                    <a href="{video['video_url']}" target="_blank" rel="noopener noreferrer">Assistir Vídeo</a>
                    <p>{caption_safe}</p>
                </div>
            </div>
            """
        html_content += "</div>"
    
    html_content += """
        <footer>Página gerada automaticamente.</footer>
        </div>
    </body>
    </html>
    """
    return html_content

async def main():
    await client.start() 
    print("Sessão iniciada com sucesso na tua conta pessoal do Telegram.")
    
    try:
        entity = await client.get_entity(SOURCE_GROUP_ID)
    except Exception as e:
        print(f"ERRO: Não foi possível obter a entidade para '{SOURCE_GROUP_ID}'. Verifica o nome do canal/grupo.")
        print(f"Detalhes do erro: {e}")
        await client.disconnect()
        return

    videos_data = []
    limit_msgs = 10000 
    
    # Define o prefixo do link (username ou ID limpo para canais privados)
    if entity.username:
        link_prefix = entity.username
        print(f"Grupo identificado como PÚBLICO: @{link_prefix}")
    else:
        chat_id_clean = str(entity.id).replace('-100', '')
        link_prefix = f"c/{chat_id_clean}"
        print(f"Grupo identificado como PRIVADO (Link via ID): {link_prefix}")
        
    
    print(f"Buscando {limit_msgs} mensagens em '{getattr(entity, 'title', SOURCE_GROUP_ID)}'...")
    
    # 1. Coletar todas as mensagens
    all_messages = []
    async for message in client.iter_messages(entity, limit=limit_msgs):
        all_messages.append(message)

    # 2. Inverter a lista para ordenar do Antigo (primeiro) para o Recente (último)
    all_messages.reverse()
    print(f"Ordenação invertida: {len(all_messages)} mensagens para processar (Antigo -> Recente).")
    
    # 3. Processar a lista invertida
    for message in all_messages:
        
        # O filtro só verifica se a mensagem TEM um objeto 'video'
        if message.video:
            
            # --- OBTENÇÃO DA MINIATURA ---
            thumbnail_b64 = ""
            if message.video.thumbs:
                best_thumb = message.video.thumbs[-1] 
                try:
                    # Tenta baixar com o timeout estendido
                    thumb_bytes = await client.download_media(best_thumb, file=bytes)
                    thumbnail_b64 = base64.b64encode(thumb_bytes).decode('utf-8')
                except Exception as e:
                    # Se falhar, a miniatura fica vazia (thumbnail_b64 = "")
                    # print(f"Aviso: Falha ao baixar miniatura: {e}") 
                    pass 
            
            # 4. GERAÇÃO DO LINK
            video_url = f"https://t.me/{link_prefix}/{message.id}"
            
            caption = message.text or "Vídeo sem legenda"
            videos_data.append({
                "video_url": video_url, 
                "caption": caption,
                "thumbnail_b64": thumbnail_b64 
            })

    print(f"Total de {len(videos_data)} vídeos encontrados.")
    
    print("Gerando arquivo HTML...")
    html_final = gerar_html(videos_data)
    
    with open('index.html', 'w', encoding='utf-8') as f: 
        f.write(html_final)
        
    print("Arquivo 'index.html' foi criado/atualizado com sucesso!")

    await client.disconnect()
    print("Sessão terminada.")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
