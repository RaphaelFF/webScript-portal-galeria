import os
import requests
from bs4 import BeautifulSoup
import extrair_oriinal

def download_image(url, base_url, filename, save_dir):
    """Baixa uma imagem a partir de uma URL e salva em um arquivo.

    Args:
        url (str): A URL da imagem (pode ser relativa).
        base_url (str): A URL base do site.
        filename (str): O nome do arquivo para salvar a imagem.
        save_dir (str): O nome do diretório onde salvar as imagens.
    """

    # Extrair hostname do base_url (assumindo formato padrão)
    hostname = base_url.split("//")[1].split("/")[0]

    # Construir URL completa
    complete_url = f"https://{hostname}/{url}"  # Assumindo HTTPS

    try:
        response = requests.get(complete_url, verify=False)  # Desabilitar verificação de certificado (se necessário)
        response.raise_for_status()  # Verificar se a requisição foi bem-sucedida

        # Criar o diretório se não existir
        os.makedirs(save_dir, exist_ok=True)

        # Caminho completo para salvar a imagem
        file_path = os.path.join(save_dir, filename)

        with open(file_path, 'wb') as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar a imagem: {e}")

def extract_and_download_images(url):
    """Extrai as URLs das imagens de um site e as baixa.

    Args:
        url (str): A URL do site.
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title_element = soup.find('h2')
    if title_element:
        title = title_element.get_text(strip=True)
        # Remover caracteres inválidos para nome de diretório
        save_dir = ''.join(c for c in title if c.isalnum() or c in (' ', '_')).rstrip()
    else:
        save_dir = 'default_directory' 

    images = soup.find_all('li', class_='sigProThumb')

    for image in images:
        image_link = image.find('a')['href']
        filename = image_link.split('/')[-1]
        download_image(image_link, url, filename, save_dir)

base_url = 'https://old.tjap.jus.br/portal/publicacoes/galeria.html'  # URL base
todos_links = []

for start in range(0, 50, 10):
    url_with_start = f"{base_url}?start={start}"
    todos_links += extrair_oriinal.extrair_links(url_with_start)

    #url = "https://old.tjap.jus.br/portal/publicacoes/galeria.html"
    #links = extrair.extrair_links(url)

for i in range(len(todos_links)):
    #save_dir = f'imagens{contador:02d}'
    extract_and_download_images(todos_links[i])


