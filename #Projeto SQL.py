#Projeto SQL

import sqlite3
conn = sqlite3.connect('disneyplusDB.db')

cur = conn.cursor()
cur.row_factory = sqlite3.Row

#Query 1 - Ordenar todos os filmes de animação lançados durante 2000 e 2020, por ordem lexicográfica.

res = cur.execute(
    '''
    SELECT title, release_date
    FROM genre JOIN classification ON genre.genre_id = classification.genre_id
                JOIN content ON classification.content_id = content.content_id
                JOIN type ON content.type_id = type.type_id
    WHERE type.designation = 'Movie' AND genre.designation = 'Animation' AND release_date >= 2000 AND release_date <= 2020
    ORDER BY release_date;
    '''
)

data = res.fetchall()

print("Animation Movies released between 2000 and 2020:")
print("Title | Release Date")
print("-" * 40)
for row in data:
    title, release_date = row
    print(f"{title} | {release_date}")

print(f"\nTotal results: {len(data)}")

# Query 2 - Contar, com base no type de conteúdo (filme ou série), quantas descrições contêm números.

res = cur.execute(
    '''
    SELECT type_id, COUNT(*) as total
    FROM content
    WHERE type_id IN ('filme', 'serie') 
    AND (
    description LIKE '%0%' OR
    description LIKE '%1%' OR
    description LIKE '%2%' OR
    description LIKE '%3%' OR
    description LIKE '%4%' OR
    description LIKE '%5%' OR
    description LIKE '%6%' OR
    description LIKE '%7%' OR
    description LIKE '%8%' OR
    description LIKE '%9%'
    )
    GROUP BY type_id;
    '''
)

# Query 3 - Contar o número de filmes e o número de séries dirigidas por cada diretor.

res = cur.execute(
    '''
    SELECT pessoa.nome as nome, count(content_id) as directed
    FROM direcao JOIN pessoa on direcao.id_pessoa = pessoa.id_pessoa
                 JOIN content on content.content_id = direcao.content_id
    WHERE content.type_id IN = ('filme''serie')
    GROUP BY pessoa.nome, content.type_id
    ORDER BY pessoa.nome;
    '''
)

data = res.fetchall()

# Query 4 - Listar todas as obras, não de ação-aventura, cujo título contém um sinal de pontuação.

res = cur.execute(
    '''
    SELECT title
    FROM classification JOIN genre ON classification.genre_id = genre.genre_id
                      JOIN content ON classification.content_id = content.content_id
    WHERE genre.genre_name <> 'Action-Adventure' AND (
          content.title LIKE '%!%' OR
          content.title LIKE '%?%' OR
          content.title LIKE '%,%' OR
          content.title LIKE '%.%' OR
          content.title LIKE '%"%' OR
          content.title LIKE "%'%" OR
          content.title LIKE '%:%' OR
          content.title LIKE '%;%' OR
    );
    '''
)

# Query 5 - Listar todas as séries não realizadas nos Estados Unidos, com mais de 1 temporada.

# Query 6 - Todas os obras dirigidas por um diretor cujo nome começa por 'J' e com atores com nomes ou apelido começados por 'S'.

# Query 7 - Contar todos os filmes com duração superior a 100 minutos, com base no ano e type.

# Query 8 - Contar todas as obras adicionadas entre março e novembro de 2021, em função do rating.

# Query 9 - Listar todas as obras, por ordem de adição, cuja descrição contém o título ou não contém o nome de nenhum mebro do elenco.

# Query 10 - Listar filmes com duração entre 30 e 120 minutos, agrupados por década de lançamento.

# Query 11 - Encontrar diretores que dirigiram tanto filmes quanto séries, 
#            onde pelo menos um ator apareceu em ambos os types.

# Query 12 - Identificar "clusters" de conteúdo: obras que compartilham 
#            pelo menos 2 categorias, 1 ator em comum, e são de types diferentes