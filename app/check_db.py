import sqlite3

connection = sqlite3.connect("database/phishing.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM analysis_results")

rows = cursor.fetchall()
phishing_count = 0

for row in rows:
    
    print("\n========================")
    print(f"ID: {row[0]}")
    print(f"Email Text: {row[1]}")
    print(f"Prediction: {row[2]}")
    print(f"Label: {row[3]}")
    print(f"Confidence: {row[4]}")
    print(f"Number of Words: {row[5]}")
    print(f"Unique Words: {row[6]}")
    print(f"Stopwords: {row[7]}")
    print(f"Links: {row[8]}")
    print(f"Unique Domains: {row[9]}")
    print(f"Email Addresses: {row[10]}")
    print(f"Spelling Errors: {row[11]}")
    print(f"Urgent Keywords: {row[12]}")

    print("Prediction value =", row[2])
    print("Type =", type(row[2]))

    if row[2] == "phishing":
        phishing_count += 1

print("\n========================")
print(f"Total Records: {len(rows)}")
print(f"Total Phishing Attempts: {phishing_count}")
print("========================")

connection.close()