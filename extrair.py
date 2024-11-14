import requests
from bs4 import BeautifulSoup

def extract_links(url):
    """Extrai links de uma página HTML com a estrutura especificada e adiciona um prefixo.

    Args:
        url (str): URL da página.

    Returns:
        list: Lista de links extraídos com o prefixo.
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links_set = set()  # Usar um conjunto para evitar duplicatas
    prefix = "https://old.tjap.jus.br"
    for row_num in range(2):
        for div in soup.find_all('div', class_=lambda c: c and c.startswith('items-row cols-1 row-') and str(row_num) in c):
            for link in div.find_all('a', href=True):
                # Concatena o prefixo com o link original
                complete_link = prefix + link['href']
                links_set.add(complete_link)  # Adiciona ao conjunto

    return list(links_set)  # Converte o conjunto de volta para lista

# Exemplo de uso:
url = 'https://old.tjap.jus.br/portal/publicacoes/galeria.html'  # Substitua pela URL da página
all_links = extract_links(url)
for index, link in enumerate(all_links, start=1):
    print(f"{index}. {link}")
    
# Exibe todos os links extraídos
#print("Links extraídos:")
#for index, link in enumerate(todos_links, start=1):
 #   print(f"{index}. {link}")

