import csv
from collections import Counter

def extract_unique_values(csv_file):
    # Initialize sets for unique values
    types = set()
    ratings = set()
    genres = set()
    countries = set()
    directors = set()
    cast_members = set()
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Single value columns
            if row['type']:
                types.add(row['type'])
            if row['rating']:
                ratings.add(row['rating'])
            
            # Multi-value columns
            if row['listed_in']:
                genre_list = [g.strip() for g in row['listed_in'].split(',')]
                genres.update(genre_list)
            
            if row['country']:
                country_list = [c.strip() for c in row['country'].split(',')]
                countries.update(country_list)
            
            if row['director']:
                director_list = [d.strip() for d in row['director'].split(',')]
                directors.update(director_list)
            
            if row['cast']:
                cast_list = [c.strip() for c in row['cast'].split(',')]
                cast_members.update(cast_list)
    
    # Convert sets to sorted lists
    types_list = sorted(types)
    ratings_list = sorted(ratings)
    genres_list = sorted(genres)
    countries_list = sorted(countries)
    directors_list = sorted(directors)
    cast_list = sorted(cast_members)
    
    # Combine directors and cast into people
    people_list = sorted(set(directors_list + cast_list))
    
    return {
        'types': types_list,
        'ratings': ratings_list,
        'genres': genres_list,
        'countries': countries_list,
        'people': people_list  # Combined directors and cast
    }

res = extract_unique_values('Ficheiros\\DisneyPlus.csv')

with open('unique_values_output.txt', 'w', encoding='utf-8') as f:
    for key in sorted(res.keys()):  # Sort keys alphabetically
        values = res[key]
        f.write(f"=== {key.upper()} ({len(values)} items) ===\n")
        
        # Write each value as a tuple with sequential numbering
        for i, value in enumerate(values, 1):
            f.write(f"({i}, '{value}'),\n")
        
        f.write("\n")  # Add empty line between sections