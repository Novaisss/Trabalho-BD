#Projeto SQL

import sqlite3
conn = sqlite3.connect('.db')

cur = conn.cursor()
cur.row_factory = sqlite3.Row

#Query 1 - Ordenar todos os filmes de animação lançados durante 2000 e 2020, por ordem lexicográfica.

res = cur.execute(
    '''
    SELECT title, release_date
    FROM genero JOIN classificado ON genero.genero_id = classificado.genero_id
                JOIN conteudo ON classificado.show_id = contuedo_id
                JOIN tipo ON conteudo.show_id = tipo.type_id
    WHERE tipo.type_id = 'filme' AND genero.genero_id = 'animation' AND release_date >= '2000-01-01' AND release_date <= '2020-12-31'
    ORDER BY release_date;
    '''
)

data = res.fetchall()

# Query 2 - Contar, com base no tipo de conteúdo (filme ou série), quantas descrições contêm números.

res = cur.execute(
    '''
    SELECT type_id, COUNT(*) as total
    FROM conteudo
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
    SELECT pessoa.nome as nome, count(show_id) as directed
    FROM direcao JOIN pessoa on direcao.id_pessoa = pessoa.id_pessoa
                 JOIN conteudo on conteudo.show_id = direcao.show_id
    WHERE conteudo.type_id IN = ('filme''serie')
    GROUP BY pessoa.nome, conteudo.type_id
    ORDER BY pessoa.nome;
    '''
)

data = res.fetchall()

# Query 4 - Listar todas as obras, não de ação-aventura, cujo título contém um sinal de pontuação.

res = cur.execute(
    '''
    SELECT title
    FROM classificado JOIN genero ON classificado.genero_id = genero.genero_id
                      JOIN conteudo ON classificado.show_id = conteudo.show_id
    WHERE genero.genero_name <> 'Action-Adventure' AND (
          conteudo.title LIKE '%!%' OR
          conteudo.title LIKE '%?%' OR
          conteudo.title LIKE '%,%' OR
          conteudo.title LIKE '%.%' OR
          conteudo.title LIKE '%"%' OR
          conteudo.title LIKE "%'%" OR
          conteudo.title LIKE '%:%' OR
          conteudo.title LIKE '%;%' OR
    );
    '''
)

# Query 5 - Listar todas as séries não realizadas nos Estados Unidos, com mais de 1 temporada.

# Query 6 - Todas os obras dirigidas por um diretor cujo nome começa por 'J' e com atores com nomes ou apelido começados por 'S'.

# Query 7 - Contar todos os filmes com duração superior a 100 minutos, com base no ano e tipo.

# Query 8 - Contar todas as obras adicionadas entre março e novembro de 2021, em função do rating.

# Query 9 - Listar todas as obras, por ordem de adição, cuja descrição contém o título ou não contém o nome de nenhum mebro do elenco.

# Query 10 - Listar filmes com duração entre 30 e 120 minutos, agrupados por década de lançamento.

# Query 11 - Encontrar diretores que dirigiram tanto filmes quanto séries, 
#            onde pelo menos um ator apareceu em ambos os tipos.

# Query 12 - Identificar "clusters" de conteúdo: obras que compartilham 
#            pelo menos 2 categorias, 1 ator em comum, e são de tipos diferentes