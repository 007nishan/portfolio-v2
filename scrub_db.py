import sqlite3
import re

db_path = r"c:\Users\NISHAN\Desktop\Test Folder\My Portfolio\portfolio\data\portfolio.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

def scrub_fcc(text):
    if not text:
        return text
    # Case insensitive removal of 'freecodecamp' and 'free code camp'
    text = re.sub(r'(?i)free\s*code\s*camp', '', text)
    return text

c.execute("SELECT id, problem_text, concepts_text, quote_text, fcc_description, title FROM challenges")
rows = c.fetchall()

updates = 0
for row in rows:
    row_id, problem, concepts, quote, desc, title = row
    
    new_problem = scrub_fcc(problem)
    new_concepts = scrub_fcc(concepts)
    new_quote = scrub_fcc(quote)
    new_desc = scrub_fcc(desc)
    new_title = scrub_fcc(title)
    
    if (new_problem != problem or new_concepts != concepts or 
        new_quote != quote or new_desc != desc or new_title != title):
        
        c.execute("""
            UPDATE challenges 
            SET problem_text=?, concepts_text=?, quote_text=?, fcc_description=?, title=?
            WHERE id=?
        """, (new_problem, new_concepts, new_quote, new_desc, new_title, row_id))
        updates += 1

print(f"Scrubbed {updates} database records containing 'freecodecamp'.")

conn.commit()
conn.close()
