import csv
from collections import defaultdict

def extract_unique_values_with_show_ids(csv_file):
    # Initialize sets for unique values
    types = set()
    ratings = set()
    genres = set()
    countries = set()
    
    # Dictionaries to store people and their associated show_ids
    directors_dict = defaultdict(list)
    cast_dict = defaultdict(list)
    
    # Dictionaries to store show_id to countries and genres mapping
    show_country_dict = defaultdict(list)
    show_genre_dict = defaultdict(list)
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            show_id = row['show_id']
            # Extract just the integer part from show_id (remove 's' prefix)
            show_id_int = int(show_id[1:]) if show_id.startswith('s') else int(show_id)
            
            # Single value columns
            if row['type']:
                types.add(row['type'])
            if row['rating']:
                ratings.add(row['rating'])
            
            # Multi-value columns
            if row['listed_in']:
                genre_list = [g.strip() for g in row['listed_in'].split(',')]
                genres.update(genre_list)
                # Store genre associations for this show
                for genre in genre_list:
                    show_genre_dict[show_id_int].append(genre)
            
            if row['country']:
                country_list = [c.strip() for c in row['country'].split(',')]
                countries.update(country_list)
                # Store country associations for this show
                for country in country_list:
                    show_country_dict[show_id_int].append(country)
            
            # Store directors with their show_ids
            if row['director']:
                director_list = [d.strip() for d in row['director'].split(',')]
                for director in director_list:
                    directors_dict[director].append(show_id_int)
            
            # Store cast members with their show_ids
            if row['cast']:
                cast_list = [c.strip() for c in row['cast'].split(',')]
                for cast_member in cast_list:
                    cast_dict[cast_member].append(show_id_int)
    
    # Convert sets to sorted lists
    types_list = sorted(types)
    ratings_list = sorted(ratings)
    genres_list = sorted(genres)
    countries_list = sorted(countries)
    
    # Get sorted lists of people
    directors_list = sorted(directors_dict.keys())
    cast_list = sorted(cast_dict.keys())
    
    # Find people who appear in both directors and cast
    people_in_both = sorted(set(directors_list) & set(cast_list))
    
    # Create unified people table - people in both get added first, then others
    all_people = people_in_both + sorted(set(directors_list + cast_list) - set(people_in_both))
    
    return {
        'types': types_list,
        'ratings': ratings_list,
        'genres': genres_list,
        'countries': countries_list,
        'directors_dict': directors_dict,
        'cast_dict': cast_dict,
        'show_country_dict': show_country_dict,  # mapping of show_id to countries
        'show_genre_dict': show_genre_dict,     # mapping of show_id to genres
        'directors_list': directors_list,
        'cast_list': cast_list,
        'people': all_people,
        'people_in_both': people_in_both
    }

res = extract_unique_values_with_show_ids('Ficheiros\\DisneyPlus.csv')

with open('unique_values_output.txt', 'w', encoding='utf-8') as f:
    # Write types, ratings, genres, countries first
    for key in ['types', 'ratings', 'genres', 'countries']:
        values = res[key]
        f.write(f"=== {key.upper()} ({len(values)} items) ===\n")
        for i, value in enumerate(values, 1):
            f.write(f"({i}, '{value}'),\n")
        f.write("\n")
    
    # Write unified people table
    f.write(f"=== PEOPLE ({len(res['people'])} items) ===\n")
    for i, person in enumerate(res['people'], 1):
        f.write(f"({i}, '{person}'),\n")
    f.write("\n")
    
    # Write directors with show_ids
    f.write(f"=== DIRECTORS WITH SHOW_IDS ({len(res['directors_list'])} people, {sum(len(ids) for ids in res['directors_dict'].values())} relationships) ===\n")
    for person in res['directors_list']:
        person_id = res['people'].index(person) + 1
        show_ids = res['directors_dict'][person]
        for show_id in show_ids:
            f.write(f"({person_id}, '{person}', {show_id}),\n")
    f.write("\n")
    
    # Write cast with show_ids
    f.write(f"=== CAST WITH SHOW_IDS ({len(res['cast_list'])} people, {sum(len(ids) for ids in res['cast_dict'].values())} relationships) ===\n")
    for person in res['cast_list']:
        person_id = res['people'].index(person) + 1
        show_ids = res['cast_dict'][person]
        for show_id in show_ids:
            f.write(f"({person_id}, '{person}', {show_id}),\n")
    f.write("\n")
    
    # Write content_id to country_id mapping
    f.write(f"=== CONTENT_ID TO COUNTRY_ID MAPPING ===\n")
    total_country_relationships = sum(len(countries) for countries in res['show_country_dict'].values())
    f.write(f"# Total relationships: {total_country_relationships}\n")
    
    for show_id, countries in sorted(res['show_country_dict'].items()):
        for country in countries:
            country_id = res['countries'].index(country) + 1
            f.write(f"({show_id}, {country_id}),  # {country}\n")
    f.write("\n")
    
    # Write content_id to genre_id mapping
    f.write(f"=== CONTENT_ID TO GENRE_ID MAPPING ===\n")
    total_genre_relationships = sum(len(genres) for genres in res['show_genre_dict'].values())
    f.write(f"# Total relationships: {total_genre_relationships}\n")
    
    for show_id, genres in sorted(res['show_genre_dict'].items()):
        for genre in genres:
            genre_id = res['genres'].index(genre) + 1
            f.write(f"({show_id}, {genre_id}),\n")
    f.write("\n")