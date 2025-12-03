import csv
import re
from datetime import datetime

# Rating mapping dictionary
rating_mapping = {
    'G': 1,
    'PG': 2,
    'PG-13': 3,
    'TV-14': 4,
    'TV-G': 5,
    'TV-PG': 6,
    'TV-Y': 7,
    'TV-Y7': 8,
    'TV-Y7-FV': 9
}

def escape_single_quotes(text):
    """Double any single quotes in the string to escape them"""
    if isinstance(text, str):
        return text.replace("'", "''")
    return text

def is_empty_value(value):
    """Check if value is empty or missing"""
    return value is None or str(value).strip() == ''

def get_formatted_tuples_from_csv(file_path, columns_config):
    """
    Select specific columns from a CSV file with data type conversion
    """
    tuples_list = []
    
    def convert_duration_to_minutes(duration_str):
        if is_empty_value(duration_str):
            return None
            
        duration_str = duration_str.lower().strip()
        
        if 'season' in duration_str:
            numbers = re.findall(r'\d+', duration_str)
            return int(numbers[0]) if numbers else None
        elif 'min' in duration_str:
            numbers = re.findall(r'\d+', duration_str)
            return int(numbers[0]) if numbers else None
        elif 'h' in duration_str or 'm' in duration_str:
            hours = 0
            minutes = 0
            hour_match = re.search(r'(\d+)h', duration_str)
            if hour_match:
                hours = int(hour_match.group(1))
            minute_match = re.search(r'(\d+)m', duration_str)
            if minute_match:
                minutes = int(minute_match.group(1))
            return hours * 60 + minutes
        else:
            numbers = re.findall(r'\d+', duration_str)
            return int(numbers[0]) if numbers else None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            columns_to_select = list(columns_config.keys())
            
            available_columns = reader.fieldnames
            missing_columns = [col for col in columns_to_select if col not in available_columns]
            
            if missing_columns:
                return tuples_list
            
            for row in reader:
                formatted_data = []
                for col in columns_to_select:
                    value = row[col]
                    data_type = columns_config[col]
                    
                    if is_empty_value(value):
                        formatted_value = None
                    else:
                        try:
                            if data_type == int:
                                if col == 'show_id':
                                    formatted_value = int(value[1:]) if value.startswith('s') else int(value)
                                elif col == 'type':
                                    if value.lower() == 'movie':
                                        formatted_value = 1
                                    elif value.lower() == 'tv show':
                                        formatted_value = 2
                                    else:
                                        formatted_value = None
                                elif col == 'release_year':
                                    formatted_value = int(value)
                                elif col == 'rating':
                                    formatted_value = rating_mapping.get(value, None)
                                elif col == 'duration':
                                    formatted_value = convert_duration_to_minutes(value)
                                else:
                                    formatted_value = int(value)
                            elif data_type == 'date':
                                date_obj = datetime.strptime(value, '%B %d, %Y')
                                formatted_value = date_obj.strftime('%Y-%m-%d')
                            elif data_type == float:
                                formatted_value = float(value)
                            else:
                                formatted_value = escape_single_quotes(str(value))
                        except (ValueError, TypeError):
                            formatted_value = escape_single_quotes(value) if data_type == str else None
                    
                    formatted_data.append(formatted_value)
                
                tuples_list.append(tuple(formatted_data))
                
        return tuples_list
                
    except FileNotFoundError:
        return []
    except Exception:
        return []

# Main execution
if __name__ == "__main__":
    columns_config = {
        'show_id': int,
        'type': int,
        'title': str,
        'release_year': int,
        'date_added': 'date',
        'rating': int,
        'duration': int,
        'description': str
    }
    
    formatted_tuples = get_formatted_tuples_from_csv('Ficheiros\\DisneyPlus.csv', columns_config)
    
    with open('content_tuples.txt', 'w', encoding='utf-8') as f:
        for data_tuple in formatted_tuples:
            # Handle NULL values in the output
            show_id = data_tuple[0] if data_tuple[0] is not None else 'NULL'
            type_val = data_tuple[1] if data_tuple[1] is not None else 'NULL'
            title = f"'{data_tuple[2]}'" if data_tuple[2] is not None else 'NULL'
            release_year = data_tuple[3] if data_tuple[3] is not None else 'NULL'
            date_added = f"'{data_tuple[4]}'" if data_tuple[4] is not None else 'NULL'
            rating = data_tuple[5] if data_tuple[5] is not None else 'NULL'
            duration = data_tuple[6] if data_tuple[6] is not None else 'NULL'
            description = f"'{data_tuple[7]}'" if data_tuple[7] is not None else 'NULL'
            
            f.write(f"({show_id}, {type_val}, {title}, {release_year}, {date_added}, {rating}, {duration}, {description}),\n")