import os
import requests
from bs4 import BeautifulSoup
import extrair

def download_image(url, base_url, filename, save_dir="imagens02"):
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

    images = soup.find_all('li', class_='sigProThumb')

    for image in images:
        image_link = image.find('a')['href']
        filename = image_link.split('/')[-1]
        download_image(image_link, url, filename)





url = "https://old.tjap.jus.br/portal/publicacoes/galeria/13934-143%C2%AA-edi%C3%A7%C3%A3o-da-jornada-itinerante-fluvial-ao-bailique-clique-aqui.html"

#vai me retodar um links[link1, link2 ...]
link = extrair.extrair_links(url)


extract_and_download_images(link[i])