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
    # Configurações de estabilidade
    connection_retries=10,  
    retry_delay=5,          
    timeout=30              
)

def gerar_html(videos_data):
    """
    Função para gerar o conteúdo de um arquivo HTML usando MINIATURAS CLICÁVEIS 
    que apontam para o link direto do Telegram.
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
                overflow: hidden; 
                transition: transform 0.2s;
                display: flex; 
                flex-direction: column;
            }
            .video-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }

            /* --- ESTILO DA MINIATURA --- */
            .thumbnail-link {
                display: block;
                position: relative;
                width: 100%;
                /* Proporção 16:9 */
                padding-top: 56.25%; 
                overflow: hidden;
            }
            .thumbnail-link img {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                object-fit: cover;
                transition: opacity 0.3s;
            }
            .thumbnail-link:hover img {
                opacity: 0.8;
            }

            .video-content {
                padding: 15px;
                flex-grow: 1; 
            }
            .video-card p { 
                margin-top: 8px; 
                color: #606770; 
                white-space: pre-wrap; 
                word-wrap: break-word; 
                font-size: 0.9em;
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
            
            # Miniatura em Base64
            # A imagem é inserida diretamente no código HTML (sem links externos)
            thumbnail_tag = f'<img src="data:image/jpeg;base64,{video["thumbnail_b64"]}" alt="Pré-visualização do Vídeo">' if video["thumbnail_b64"] else ""
            
            # Geração do link clicável que redireciona para o Telegram
            link_tag = f"""
            <a href="{video["video_url"]}" target="_blank" class="thumbnail-link">
                {thumbnail_tag}
            </a>
            """
            
            html_content += f"""
            <div class="video-card">
                {link_tag}
                <div class="video-content">
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
        await client.disconnect()
        return

    videos_data = []
    limit_msgs = 10000 
    
    # Define o prefixo do link (username para canais públicos ou ID para privados)
    if entity.username:
        link_prefix = entity.username
        print(f"Grupo identificado como PÚBLICO: @{link_prefix}")
    else:
        chat_id_clean = str(entity.id).replace('-100', '')
        link_prefix = f"c/{chat_id_clean}"
        print(f"Grupo identificado como PRIVADO (Link via ID): {link_prefix}.")
        
    
    print(f"Buscando {limit_msgs} mensagens em '{getattr(entity, 'title', SOURCE_GROUP_ID)}'...")
    
    all_messages = []
    async for message in client.iter_messages(entity, limit=limit_msgs):
        all_messages.append(message)

    # Ordenar do Antigo (primeiro) para o Recente (último)
    all_messages.reverse()
    print(f"Ordenação invertida: {len(all_messages)} mensagens para processar (Antigo -> Recente).")
    
    for message in all_messages:
        
        if message.video:
            
            # 1. DOWNLOAD DA MINIATURA E CONVERSÃO PARA BASE64
            thumbnail_b64 = ""
            if message.video.thumbs:
                best_thumb = message.video.thumbs[-1] 
                try:
                    thumb_bytes = await client.download_media(best_thumb, file=bytes)
                    thumbnail_b64 = base64.b64encode(thumb_bytes).decode('utf-8')
                except Exception as e:
                    print(f"Aviso: Não foi possível baixar a miniatura da mensagem {message.id}. {e}")
            
            # 2. GERAÇÃO DO LINK DIRETO DO TELEGRAM
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
    
    # 3. SALVAMENTO NA PASTA 'public' PARA O GITHUB PAGES
    output_dir = 'public'
    os.makedirs(output_dir, exist_ok=True) 
    
    output_path = os.path.join(output_dir, 'index.html') 
    
    with open(output_path, 'w', encoding='utf-8') as f: 
        f.write(html_final)
        
    print(f"Arquivo '{output_path}' foi criado/atualizado com sucesso!")

    await client.disconnect()
    print("Sessão terminada.")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
