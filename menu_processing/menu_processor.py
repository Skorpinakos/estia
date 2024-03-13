import pdfplumber
import csv

def is_bad(x):
    # Replace this with your own condition
    # For example, to check if x is a positive number, return x > 0
    if x==None:
        return True
    elif x.strip()=="":
        return True
    else:
        return False

def remove_rows_columns(matrix, is_bad):
    # Identify rows and columns to remove
    rows_to_remove = set()
    columns_to_remove = set()

    # Check rows
    for i, row in enumerate(matrix):
        if all(is_bad(x) for x in row):
            rows_to_remove.add(i)

    # Check columns
    
        for j in range(len(matrix[0])):  # Assuming at least one row in the matrix
            try:
                if all(is_bad(matrix[i][j]) for i in range(len(matrix))):
                    columns_to_remove.add(j)
            except:
                pass

    # Remove identified rows and columns
    new_matrix = [
        [cell for j, cell in enumerate(row) if j not in columns_to_remove]
        for i, row in enumerate(matrix) if i not in rows_to_remove
    ]

    return new_matrix


def save_2d_list_to_csv(data, filename):
    """
    Saves a 2D list to a CSV file.

    :param data: The 2D list of data to save.
    :param filename: The name of the file to save the data to.
    """
    # Open the file in write mode
    with open(filename, 'w', newline='',encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write each row of the data to the CSV file
        for row in data:
            writer.writerow(row)

# Define the path to your PDF file
pdf_path = 'menu_processing\monthly_menu.pdf'

# Initialize an empty list to hold all the tables
all_tables = []

# Open the PDF and extract tables
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        # Extract tables from the current page
        tables = page.extract_tables()
        
        # For each table found, convert it into a 2D list and append to all_tables
        for table in tables:
            # Convert the table (which is a list of lists) into a 2D list
            processed_table = [row for row in table]  # This is already a 2D list, but you could add processing here
            all_tables.append(processed_table)


if all_tables:
    merged_tables=[]
    for i,table in enumerate(all_tables):
        if len(table)>10:
            merged_tables.append(table)
        elif i!=(len(all_tables)-1):#not breakfast
            merged_tables[-1]=merged_tables[-1]+table
        else:
            merged_tables.append(table)




    for i,table in enumerate(merged_tables):
       
        table_filtered=[]#table[4:7]+[table[8],]+table[10:12]+table[15:18]+[table[19]]+[table[21]]
        filter_rows_list=[]
        for j,row in enumerate(table):
            for k,cell in enumerate(row):
                if cell ==None:
                    continue
                if cell.strip() in ["ΓΕΥΜΑ","Μπουφές Σαλάτα","Επιδόρπιο","ΔΕΙΠΝΟ"] or "/" in cell.strip():
                    filter_rows_list.append(j)

        for j,row in enumerate(table):
            if j not in filter_rows_list:
                table_filtered.append(row[1:])
        table_filtered=remove_rows_columns(table_filtered,is_bad)
        save_2d_list_to_csv(table_filtered, "menu_processing/table_"+str(i)+".csv")

            
        


else:
    print("No tables found.")
