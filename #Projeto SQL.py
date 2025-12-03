#Projeto SQL

import sqlite3

def execute_all_queries():
    conn = sqlite3.connect('disneyplusDB.db')
    cur = conn.cursor()
    cur.row_factory = sqlite3.Row
    
    all_results = []
    
    # Query 1 - Ordenar todos os filmes de animação lançados durante 2000 e 2020, por ordem lexicográfica.
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
    data1 = res.fetchall()
    all_results.append(("Query 1 - Filmes de animação lançados entre 2000 e 2020", data1))

    # Query 2 - Contar, com base no type de conteúdo (filme ou série), quantas descrições contêm números.
    res = cur.execute(
        '''
        SELECT type.designation as type, COUNT(*) as total
        FROM content
        JOIN type ON content.type_id = type.type_id
        WHERE type.designation IN ('Movie', 'TV Show') 
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
        GROUP BY type.designation;
        '''
    )
    data2 = res.fetchall()
    all_results.append(("Query 2 - Conteúdo com descrições que contêm números, por tipo", data2))

    # Query 3 - Contar o número de filmes e o número de séries dirigidas por cada diretor.
    res = cur.execute(
        '''
        SELECT*
        FROM (
            SELECT person.name as director, type.designation as type, COUNT(*) as count
            FROM direction 
            JOIN person ON direction.person_id = person.person_id
            JOIN content ON direction.content_id = content.content_id
            JOIN type ON content.type_id = type.type_id
            WHERE type.designation = 'Movie'
            GROUP BY person.name

            UNION

            SELECT person.name as director, type.designation as type, COUNT(*) as count
            FROM direction 
            JOIN person ON direction.person_id = person.person_id
            JOIN content ON direction.content_id = content.content_id
            JOIN type ON content.type_id = type.type_id
            WHERE type.designation = 'TV Show'
            GROUP BY person.name
        );
        '''
    )
    data3 = res.fetchall()
    all_results.append(("Query 3 - Número de filmes e séries dirigidas por cada diretor", data3))

    # Query 4 - Listar todas as obras, não de ação-aventura, cujo título contém um sinal de pontuação.
    res = cur.execute(
        '''
        SELECT DISTINCT content.title
        FROM content
        JOIN classification ON content.content_id = classification.content_id
        JOIN genre ON classification.genre_id = genre.genre_id
        WHERE genre.designation <> 'Action-Adventure' 
        AND (
            content.title LIKE '%!%' OR
            content.title LIKE '%?%' OR
            content.title LIKE '%,%' OR
            content.title LIKE '%.%' OR
            content.title LIKE '%"%' OR
            content.title LIKE "%'%" OR
            content.title LIKE '%:%' OR
            content.title LIKE '%;%'
        );
        '''
    )
    data4 = res.fetchall()
    all_results.append(("Query 4 - Obras não de ação-aventura com título contendo pontuação", data4))

    # Query 5 - Listar todas as séries não realizadas nos Estados Unidos, com mais de 1 temporada.
    res = cur.execute(
        '''
        SELECT DISTINCT content.title, country.name as country, content.duration
        FROM content 
        JOIN type ON content.type_id = type.type_id
        JOIN made_in ON content.content_id = made_in.content_id
        JOIN country ON made_in.country_id = country.country_id
        WHERE country.name <> 'United States' 
        AND type.designation = 'TV Show' 
        AND content.duration > 1;
        '''
    )
    data5 = res.fetchall()
    all_results.append(("Query 5 - Séries não realizadas nos EUA com mais de 1 temporada", data5))

    # Query 6 - Todas os obras dirigidas por um diretor cujo nome começa por 'J' e com atores com nome ou apelido começado por 'S'.
    res = cur.execute(
        '''
        SELECT DISTINCT content.content_id, content.title, director.name as director, actor.name as actor
        FROM content
        JOIN direction ON content.content_id = direction.content_id
        JOIN person as director ON direction.person_id = director.person_id
        JOIN c_cast ON content.content_id = c_cast.content_id
        JOIN person as actor ON c_cast.person_id = actor.person_id
        WHERE director.name LIKE 'J%'
        AND (actor.name LIKE '% S%' OR actor.name LIKE 'S%')
        ORDER BY content.content_id;
        '''
    )
    data6 = res.fetchall()
    all_results.append(("Query 6 - Obras com diretor começando por 'J' e atores começando por 'S'", data6))

    # Query 7 - Contar todos os filmes com duração superior a 100 minutos, com base no ano no género.
    res = cur.execute(
        '''
        SELECT genre.designation as genre, content.release_date as year, COUNT(*) as total
        FROM content 
        JOIN type ON content.type_id = type.type_id
        JOIN classification ON content.content_id = classification.content_id
        JOIN genre ON classification.genre_id = genre.genre_id
        WHERE type.designation = 'Movie' 
        AND Content.duration > 100
        GROUP BY genre.designation, content.release_date
        ORDER BY content.release_date;
        '''
    )
    data7 = res.fetchall()
    all_results.append(("Query 7 - Filmes com duração > 100 minutos, por género e ano", data7))

    # Query 8 - Contar todas as obras adicionadas entre março e novembro de 2021, em função do rating.
    res = cur.execute(
        '''
        SELECT
        c.rating, 
        COUNT(d.title) as total, 
        MIN(d.date_added) as first_added, 
        MAX(d.date_added) as last_added
        FROM (
            SELECT 
                content.content_id as id, 
                content.title, 
                content.date_added as date_added
            FROM content
            WHERE content.date_added >= '2021-03-01' 
            AND content.date_added <= '2021-11-30'
        ) d
        JOIN (
            SELECT 
                content.content_id as id, 
                content.rating_id, 
                rating.designation as rating
            FROM content 
            JOIN rating ON content.rating_id = rating.rating_id
        ) c ON d.id = c.id
        GROUP BY c.rating;
        '''
    )
    data8 = res.fetchall()
    all_results.append(("Query 8 - Obras adicionadas entre março e novembro 2021, por rating", data8))

    # Query 9 - Listar todas as obras, por ordem de adição, cuja descrição contém o título ou não contém o nome de nenhum mebro do elenco.
    res = cur.execute(
        '''
        SELECT title
        FROM (
            SELECT content.content_id as id, content.title as title
            FROM content 
            JOIN c_cast ON content.content_id = c_cast.content_id
            JOIN person ON c_cast.person_id = person.person_id
            WHERE content.description NOT LIKE '%' || person.name || '%'
            GROUP BY id, title
            
            UNION
            
            SELECT content.content_id as id, content.title as title
            FROM content 
            JOIN c_cast ON content.content_id = c_cast.content_id
            JOIN person ON c_cast.person_id = person.person_id
            WHERE content.description LIKE '%' || content.title || '%'
            GROUP BY id, title
        )
        ORDER BY title;
        '''
    )
    data9 = res.fetchall()
    all_results.append(("Query 9 - Obras com descrição contendo título ou sem nomes do elenco", data9))

    # Query 10 - Listar filmes com duração entre 30 e 120 minutos, agrupados por década de lançamento.

    res = cur.execute(
        '''
        SELECT 
            (content.release_date / 10) * 10 as decade, 
            COUNT(content.content_id) as total
        FROM content 
        JOIN type ON content.type_id = type.type_id
        WHERE type.designation = 'Movie' 
        AND content.duration >= 30 
        AND content.duration <= 120
        GROUP BY decade
        ORDER BY decade;
        '''
    )

    data10 = res.fetchall()
    all_results.append(("Query 10 - Listar filmes com duração entre 30 e 120 minutos, agrupados por década de lançamento", data10))

    # Query 11 - Encontrar diretores e atores que colaboraram mais do que uma vez.
    
    res = cur.execute(
        '''
        SELECT 
            director.name as director,
            actor.name as actor,
            COUNT(*) as collaboration_count,
            GROUP_CONCAT(content.title, ', ') as movies_together
        FROM content
        JOIN direction ON content.content_id = direction.content_id
        JOIN person as director ON direction.person_id = director.person_id
        JOIN c_cast ON content.content_id = c_cast.content_id
        JOIN person as actor ON c_cast.person_id = actor.person_id
        WHERE director.person_id != actor.person_id
        GROUP BY director.person_id, actor.person_id
        HAVING COUNT(*) > 1
        ORDER BY collaboration_count DESC, director.name, actor.name;
        '''        
    )

    data11 = res.fetchall()
    all_results.append(("Query 11 - Encontrar diretores e atores que colaboraram mais do que uma vez", data11))

    # Query 12 - Identificar "clusters" de conteúdo: obras que compartilham 
    #            pelo menos 2 categorias, 1 ator em comum, e são de types diferentes

    ''' Other Queries
    Nível 1: Fácil (Consultas SELECT Simples e Filtros Básicos)
    1. Liste todos os géneros distintos presentes na tabela genre.
    2. Encontre o título e a duração de todos os conteúdos que têm a classificação etária 'G'.
    3. Conte quantos 'Movie' (Filme) e 'TV Show' (Série de TV) existem na base de dados.
    4. Qual é o título do conteúdo mais recentemente adicionado à base de dados?
    5. Liste todos os IDs e nomes de pessoas que se chamam 'Walt Disney'.

    Nível 2: Médio (Junções Múltiplas e Agregação)
    6. Liste o nome de todos os realizadores do conteúdo com o título 'Duck the Halls: A Mickey Mouse Christmas Special'.
    7. Encontre todos os títulos de conteúdo produzidos nos 'United States' (Estados Unidos).
    8. Calcule a duração média de todos os conteúdos do tipo 'Movie' (Filme).
    9. Liste os 5 atores que participaram no maior número de conteúdos, juntamente com a contagem de conteúdos.
    10. Para cada ano de lançamento (release_date), conte quantos conteúdos foram lançados. Ordene do ano mais recente para o mais antigo.
    11. Encontre o título de todos os conteúdos que estão classificados em mais de um género.
    12. Liste os nomes de todas as pessoas que atuaram (c_cast) e também realizaram (direction) algum conteúdo.

    Nível 3: Difícil (Subconsultas, Funções de Agregação Avançadas e Lógica Complexa)
    13. Liste o título de todos os conteúdos que não têm uma classificação etária (rating_id é NULL).
    14. Liste os nomes dos países que produziram mais de 50 conteúdos, juntamente com a contagem.
    15. Encontre os nomes dos atores que participaram apenas em conteúdos do tipo 'Movie' (Filme) e nunca em 'TV Show' (Série de TV).
    16. Qual é o nome do realizador que realizou o maior número de conteúdos do género 'Documentary' (Documentário)?
    17. Encontre o título do conteúdo que foi produzido em pelo menos 3 países diferentes.
    18. Identifique títulos de conteúdo que foram lançados em anos diferentes (ou seja, o mesmo título aparece com diferentes release_date).
    19. Para cada tipo de conteúdo ('Movie' e 'TV Show'), liste o título e a duração, e atribua um ranking de 1 a N com base na duração (do mais longo para o mais curto) dentro do seu respetivo tipo.
    20. Encontre o título do conteúdo que está classificado em todos os géneros que contêm a palavra 'Action' (Ação) no seu nome.
    '''

    return all_results

def write_all_results_to_file(all_results, filename='query_results.txt'):
    """Write all query results to a file at once"""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("DISNEY+ DATABASE QUERY RESULTS\n")
        file.write("=" * 80 + "\n\n")
        
        for query_title, data in all_results:
            file.write(f"{'='*80}\n")
            file.write(f"{query_title}\n")
            file.write(f"{'='*80}\n")
            
            if not data:
                file.write("No results found.\n\n")
                continue
            
            # Calculate column widths
            headers = data[0].keys()
            # Find maximum width for each column
            col_widths = []
            for i, header in enumerate(headers):
                max_width = len(str(header))
                for row in data:
                    if len(str(row[i])) > max_width:
                        max_width = len(str(row[i]))
                col_widths.append(max_width + 2)  # +2 for padding
            
            # Write headers
            header_line = ""
            for i, header in enumerate(headers):
                header_line += str(header).ljust(col_widths[i])
            file.write(header_line + "\n")
            file.write("-" * sum(col_widths) + "\n")
            
            # Write data
            for row in data:
                data_line = ""
                for i, value in enumerate(row):
                    data_line += str(value if value is not None else "").ljust(col_widths[i])
                file.write(data_line + "\n")
            
            file.write(f"\nTotal results: {len(data)}\n\n")

# Main execution
if __name__ == "__main__":
    # Execute all queries and collect results
    all_query_results = execute_all_queries()
    
    # Write all results to file at once
    write_all_results_to_file(all_query_results)
        
"""
# Query para transformar o conteúdo da BD no csv original
res = cur.execute(
'''
SELECT 
    content.content_id, 
    type.designation AS type_designation, 
    content.title, 
    d.director, 
    c.cast_member, 
    co.countries AS country_names, 
    content.date_added, 
    content.release_date, 
    content.duration, 
    rating.designation AS rating_designation, 
    g.genres AS genre_designation, 
    content.description
FROM content 
JOIN type ON content.type_id = type.type_id
LEFT JOIN rating ON content.rating_id = rating.rating_id
LEFT JOIN (
    SELECT 
        made_in.content_id,
        GROUP_CONCAT(country.name) AS countries
    FROM made_in 
    JOIN country ON made_in.country_id = country.country_id
    GROUP BY made_in.content_id
) co ON content.content_id = co.content_id
LEFT JOIN (
    SELECT 
        classification.content_id,
        GROUP_CONCAT(genre.designation) AS genres
    FROM classification 
    JOIN genre ON classification.genre_id = genre.genre_id
    GROUP BY classification.content_id
) g ON content.content_id = g.content_id
LEFT JOIN (
    SELECT 
        direction.content_id,
        GROUP_CONCAT(person.name) AS director
    FROM direction 
    JOIN person ON direction.person_id = person.person_id
    GROUP BY direction.content_id
) d ON content.content_id = d.content_id
LEFT JOIN (
    SELECT 
        c_cast.content_id,
        GROUP_CONCAT(person.name) AS cast_member
    FROM c_cast 
    JOIN person ON c_cast.person_id = person.person_id
    GROUP BY c_cast.content_id
) c ON content.content_id = c.content_id
ORDER BY content.content_id;
'''
)

data = res.fetchall()

# Write to file with tuples separated by ;
with open('disneyplus_tuples.txt', 'w', encoding='utf-8') as file:
    for row in data:
        # Convert row to tuple and join with ;
        row_tuple = tuple(row)
        line = ';'.join(str(value) if value is not None else '' for value in row_tuple)
        file.write(line + '\n')

print(f"Data successfully written to 'disneyplus_tuples.txt'")
print(f"Total records exported: {len(data)}")
"""