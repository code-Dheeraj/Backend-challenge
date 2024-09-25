import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('core/store.sqlite3')
cursor = conn.cursor()

# Define the query to get the number of graded assignments for each student
query = '''
    SELECT 
        student_id,
        COUNT(*) AS graded_assignments
    FROM 
        assignments
    WHERE 
        state = 'GRADED'
    GROUP BY 
        student_id;
'''

# Execute the query
cursor.execute(query)
results = cursor.fetchall()

# Output the results
print("Number of graded assignments for each student:")
for row in results:
    print(f"Student ID: {row[0]}, Graded Assignments: {row[1]}")

# Close the connection
conn.close()


"""
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('core/store.sqlite3')
cursor = conn.cursor()

# Define the query to get the number of graded assignments for each student
query = '''
    SELECT 
        student_id,
        COUNT(*) AS graded_assignments
    FROM 
        assignments
    WHERE 
        state = 'GRADED'
    GROUP BY 
        student_id;
'''

# Execute the query
cursor.execute(query)
results = cursor.fetchall()

# Output the results
print("Number of graded assignments for each student:")
for row in results:
    print(f"Student ID: {row[0]}, Graded Assignments: {row[1]}")

# Close the connection
conn.close()



"""