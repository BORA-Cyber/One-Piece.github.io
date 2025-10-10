# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------
# DOCUMENTAÇÃO
# ---------------------------------------------------------------------------
# Objetivo: Obter o ID de um chat (grupo ou canal) privado do Telegram 
#           a partir de um link de convite.
#
# Biblioteca Principal: Telethon
# Autor: Seu Parceiro de Programacao
#
# Descrição:
# Este script utiliza a biblioteca Telethon para se conectar à sua conta do
# Telegram e resolver um link de convite. Ao resolver o link, ele extrai
# e exibe o ID numérico do chat correspondente. Este ID é útil para
# interagir com o chat através de bots ou outros scripts.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 1. IMPORTAÇÕES
# ---------------------------------------------------------------------------
# Importamos os módulos necessários da biblioteca Telethon.
# - TelegramClient: A classe principal para interagir com a API do Telegram.
# - functions: Módulo que contém os métodos da API do Telegram (Raw API).
# - errors: Módulo para tratar erros específicos da API.
# ---------------------------------------------------------------------------
import asyncio
from telethon import TelegramClient
from telethon.tl import functions
from telethon.errors import rpcerrorlist

# ---------------------------------------------------------------------------
# 2. CONFIGURAÇÃO
# ---------------------------------------------------------------------------
# ATENÇÃO: Substitua os valores abaixo pelos seus dados.
#
# API_ID e API_HASH: Você pode obtê-los em https://my.telegram.org.
#                    Faça login, vá para "API development tools" e crie
#                    um novo aplicativo.
#
# INVITE_LINK: O link de convite para o grupo ou canal que você deseja
#              descobrir o ID.
# ---------------------------------------------------------------------------
API_ID = "16626973" 
API_HASH = "8b75ca97bee5ab5b4d7d8554283349e"
INVITE_LINK = "https://t.me/+yzaVtTH62jM1ZTI0" # Exemplo de link de convite

# ---------------------------------------------------------------------------
# 3. FUNÇÃO PRINCIPAL
# ---------------------------------------------------------------------------
# Esta função assíncrona contém a lógica principal do programa.
# ---------------------------------------------------------------------------
async def main():
    """
    Função principal que se conecta ao Telegram, resolve o link de convite
    e imprime o ID do chat.
    """
    # Usamos 'async with' para criar o cliente. Isso garante que a conexão
    # seja iniciada e devidamente encerrada no final, mesmo que ocorram erros.
    # 'session_name' é o nome do arquivo que será criado para guardar sua
    # sessão e evitar que você precise fazer login toda vez.
    async with TelegramClient("minha_sessao", API_ID, API_HASH) as client:
        print("Cliente Telegram iniciado com sucesso!")
        
        try:
            # Extrai o 'hash' do link de convite. O hash é a parte única do link.
            # Ex: Para 'https://t.me/+xzoeu7DE56M0ZTE8', o hash é 'xzoeu7DE56M0ZTE8'.
            invite_hash = INVITE_LINK.split('/')[-1].replace('+', '')

            # Usamos uma chamada direta à API do Telegram para verificar o convite.
            # Esta é a forma mais robusta e oficial de fazer isso.
            updates = await client(functions.messages.CheckChatInviteRequest(
                hash=invite_hash
            ))
            
            # O ID do chat está dentro do objeto 'chat' retornado pela chamada.
            # O ID de grupos e canais no Telegram começa com '-100'. Como o ID
            # retornado pela API não inclui esse prefixo, nós o adicionamos.
            chat_id = updates.chat.id
            full_chat_id = int(f"-100{chat_id}")

            print("-" * 30)
            print(f"Link do Co# -*- coding: utf-8 -*-

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

client = TelegramClient('my_account', API_ID, API_HASH)

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
    
    # 2. DEFINIR O PREFIXO DO LINK: 
    if entity.username:
        link_prefix = entity.username
        print(f"Grupo identificado como PÚBLICO: @{link_prefix}")
    else:
        chat_id_clean = str(entity.id).replace('-100', '')
        link_prefix = f"c/{chat_id_clean}"
        print(f"Grupo identificado como PRIVADO (Link via ID): {link_prefix}")
        
    
    print(f"Buscando {limit_msgs} mensagens em '{getattr(entity, 'title', SOURCE_GROUP_ID)}'...")
    
    # --- 🔑 NOVIDADE: 1. Coletar todas as mensagens ---
    all_messages = []
    async for message in client.iter_messages(entity, limit=limit_msgs):
        all_messages.append(message)

    # --- 🔑 NOVIDADE: 2. Inverter a lista para ordenar do Antigo (primeiro) para o Recente (último) ---
    all_messages.reverse()
    print(f"Ordenação invertida: {len(all_messages)} mensagens para processar (Antigo -> Recente).")
    
    # 3. Processar a lista invertida
    for message in all_messages:
        
        # O filtro agora só verifica se a mensagem TEM um objeto 'video'
        if message.video:
            
            # --- OBTENÇÃO DA MINIATURA ---
            thumbnail_b64 = ""
            if message.video.thumbs:
                # Obtém a miniatura de maior resolução disponível e converte para Base64
                best_thumb = message.video.thumbs[-1] 
                try:
                    # Este download é o que pode falhar localmente sem proxy, mas deve funcionar no GitHub Actions
                    thumb_bytes = await client.download_media(best_thumb, file=bytes)
                    # Codifica a imagem (bytes) para Base64, que pode ser inserida diretamente no HTML
                    thumbnail_b64 = base64.b64encode(thumb_bytes).decode('utf-8')
                except Exception as e:
                    # Deixamos o aviso de falha, mas o script continua
                    # print(f"Aviso: Não foi possível baixar a miniatura da mensagem {message.id}. {e}")
                    pass 
            
            # 4. GERAÇÃO DO LINK
            video_url = f"https://t.me/{link_prefix}/{message.id}"
            
            caption = message.text or "Vídeo sem legenda"
            videos_data.append({
                "video_url": video_url, 
                "caption": caption,
                "thumbnail_b64": thumbnail_b64 # Adiciona a miniatura à lista
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
        client.loop.run_until_complete(main())nvite: {INVITE_LINK}")
            print(f"Nome do Chat: {updates.chat.title}")
            print(f"ID do Chat: {full_chat_id}")
            print("-" * 30)

        # -------------------------------------------------------------------
        # 4. TRATAMENTO DE ERROS ESPECÍFICOS
        # -------------------------------------------------------------------
        # Capturamos erros específicos para dar um feedback mais preciso.
        # -------------------------------------------------------------------
        except rpcerrorlist.InviteHashExpiredError:
            print(f"Erro: O link de convite '{INVITE_LINK}' expirou.")
        except rpcerrorlist.InviteHashInvalidError:
            print(f"Erro: O link de convite '{INVITE_LINK}' é inválido ou não existe.")
        except TypeError:
            print(f"Erro: O link de convite '{INVITE_LINK}' parece estar mal formatado.")
        except Exception as e:
            # Captura qualquer outro erro que possa ocorrer.
            print(f"Ocorreu um erro inesperado: {e}")

# ---------------------------------------------------------------------------
# 5. EXECUÇÃO DO SCRIPT
# ---------------------------------------------------------------------------
# Esta parte do código verifica se o script está sendo executado diretamente
# e, em caso afirmativo, inicia a função principal 'main'.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # asyncio.run() é a forma moderna e recomendada para executar uma
    # função assíncrona como a nossa.
    asyncio.run(main())

