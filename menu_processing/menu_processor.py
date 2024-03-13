import pdfplumber
import csv

# Define the path to your PDF file
pdf_path = 'menu_processing\monthly_menu_2.pdf'


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

days=[[]]*15
if all_tables:
    merged_tables=[]
    for i,table in enumerate(all_tables):
        if len(table)>10:
            merged_tables.append(table)
        elif i!=(len(all_tables)-1):#not breakfast
            merged_tables[-1]=merged_tables[-1]+table
        else:
            merged_tables.append(table)

    #print(merged_tables[-1])



    for i,table in enumerate(merged_tables[0:-1]): #ignore breakfast
       
        table_filtered=[]#table[4:7]+[table[8],]+table[10:12]+table[15:18]+[table[19]]+[table[21]]
        filter_rows_list=[]
        for j,row in enumerate(table):
            for k,cell in enumerate(row):
                if cell ==None:
                    continue
                if cell.strip() in ["ΓΕΥΜΑ","Μπουφές Σαλάτα","Επιδόρπιο","ΔΕΙΠΝΟ","ΕΠΙΔΟΡΠΙO","Δείπνο","Γεύμα"] or "/" in cell.strip():
                    filter_rows_list.append(j)

        for j,row in enumerate(table):
            if j not in filter_rows_list:
                table_filtered.append(row[1:])
        table_filtered=remove_rows_columns(table_filtered,is_bad)
        table_filtered=table_filtered
        for j,row in enumerate(table_filtered):
            days[j]=days[j]+row
        
        #save_2d_list_to_csv(table_filtered, "menu_processing/table_"+str(i)+".csv")

    i+=1
    #save_2d_list_to_csv(merged_tables[-1], "menu_processing/table_"+str(i)+".csv") #save breakfast too


    #fix half empty columns and shifts 
    from itertools import zip_longest
    

    def is_column_valid(column):
        non_empty_count = sum(1 for cell in column if cell.strip())
        return non_empty_count >= 3

    #remove none values
    days=[[x if (x is not None and x.strip()!="") else '' for x in row] for row in days]
    # Transpose the 2D list to iterate over columns
    transposed_days = list(map(list, zip_longest(*days, fillvalue="")))

    # Filter out invalid columns
    filtered_columns = [column for column in transposed_days if is_column_valid(column)]

    # Transpose the list back to the original format
    filtered_days = list(map(list, zip(*filtered_columns)))

    #remove empty rows again 
    filtered_days=remove_rows_columns(filtered_days,is_bad)

    #combine last 2 rows of supper unless they are identical 
            
    def combine_last_two_rows(lst):
        if not lst or len(lst) < 2:  # Check if the list is too short to combine
            return lst
        
        # Get the last two rows
        last_row = lst[-1]
        second_last_row = lst[-2]
        
        # Combined new row
        new_row = []
        
        for item1, item2 in zip(second_last_row, last_row):
            if item1 == item2 :  # If items are the same, use only one
                new_row.append(item1)
            elif item1.strip()!="" and item2.strip()!="":  # Otherwise, combine with a comma
                new_row.append(item1 + ", " + item2)
            else: #combine without comma if one or both are empty
                new_row.append(item1.strip() + item2.strip())
        
        # Replace the last two rows with the new combined row
        lst[-2:] = [new_row]
        return lst

    # Combine the last two rows of your list
    filtered_days = combine_last_two_rows(filtered_days)
    # again lol
    filtered_days = combine_last_two_rows(filtered_days)

    #shifts
    def fix_gaps(data):
        num_rows = len(data)
        num_cols = len(data[0]) if data else 0

        # Function to check and fix gaps in a specific column
        def fix_column(col_index):
            for row_index in range(num_rows):
                if row_index < num_rows - 2 and data[row_index][col_index] == "" and \
                data[row_index + 1][col_index] == "" and data[row_index + 2][col_index] == "":
                    # Found a gap, now shift values from the right for this row
                    for shift_index in range(col_index, num_cols - 1):
                        data[row_index][shift_index] = data[row_index][shift_index + 1]
                        data[row_index + 1][shift_index] = data[row_index + 1][shift_index + 1]
                        data[row_index + 2][shift_index] = data[row_index + 2][shift_index + 1]
                    # Set the last cell in the row to empty since we've shifted left
                    data[row_index][num_cols - 1] = ""
                    data[row_index + 1][num_cols - 1] = ""
                    data[row_index + 2][num_cols - 1] = ""

        # Check all columns except the last one, as there's no next column to shift from
        for col_index in range(num_cols - 1):
            fix_column(col_index)

        return data
    filtered_days=fix_gaps(filtered_days)

    

    #final empty column removal
    filtered_days=remove_rows_columns(filtered_days,is_bad)

    #combine lunch last rows 
    def combine_specific_rows(lst, index1, index2):
        if not lst or index1 >= len(lst) or index2 >= len(lst):  # Check if the indices are in range
            return lst
        
        # Get the specific rows
        first_row = lst[index1]
        second_row = lst[index2]
        
        # Combined new row
        new_row = []
        
        for item1, item2 in zip(first_row, second_row):
            if item1 == item2:  # If items are the same, use only one
                new_row.append(item1)
            else:  # Otherwise, combine with a comma
                new_row.append(item1 + ", " + item2)
        
        # Insert the new combined row and remove the old ones
        lst[index1:index2+1] = [new_row]
        return lst

    # Combine the rows indexed at 4 and 5 in your list
    filtered_days = combine_specific_rows(filtered_days, 4, 5)

    #it later became apparent we should deal with individual gaps too
    def fix_individual_gaps(data):
        num_rows = len(data)
        num_cols = len(data[0]) if data else 0

        # Function to check and fix gaps in a specific column
        def fix_column(col_index):
            for row_index in range(num_rows):
                if data[row_index][col_index] == "":
                    # Found a gap, now shift the value from the right for this cell
                    for shift_index in range(col_index, num_cols - 1):
                        data[row_index][shift_index] = data[row_index][shift_index + 1]
                    # Set the last cell in the row to empty since we've shifted left
                    data[row_index][num_cols - 1] = ""

        # Check all columns except the last one, as there's no next column to shift from
        for col_index in range(num_cols - 1):
            fix_column(col_index)

        return data
    filtered_days=fix_individual_gaps(filtered_days)


    #final final empty column removal
    filtered_days=remove_rows_columns(filtered_days,is_bad)


    #again remove half columns
    # Transpose the 2D list to iterate over columns
    transposed_days = list(map(list, zip_longest(*filtered_days, fillvalue="")))

    # Filter out invalid columns
    filtered_columns = [column for column in transposed_days if is_column_valid(column)]

    # Transpose the list back to the original format
    filtered_days = list(map(list, zip(*filtered_columns)))

    #remove empty rows again 
    filtered_days=remove_rows_columns(filtered_days,is_bad)

    save_2d_list_to_csv(filtered_days, "menu_processing/month_days.csv")
    print(len(filtered_days[0]))
    


else:
    print("No tables found.")
