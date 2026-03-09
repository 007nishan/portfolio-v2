import sqlite3, os, json, re

db_path = os.path.join(r"c:\Users\NISHAN\Desktop\Test Folder\My Portfolio\portfolio", "data", "portfolio.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT fcc_py_tests, title FROM challenges WHERE date_id = '2026-03-08'")
row = c.fetchone()
if row and row[0]:
    tests = json.loads(row[0])
    print(f"--- Tests for {row[1]} ---")
    for i, t in enumerate(tests[:2]):
        print(f"Test {i}: {t.get('text')}")
        test_string = t.get("testString", "")
        print(f"Raw testString:\n{test_string[:150]}...")
        
        # Try to extract pure python
        match = re.search(r'runPython\(`(.*?)`\)', test_string, re.DOTALL)
        if match:
            print(f"Extracted Python:\n{match.group(1).strip()}")
        print("-" * 40)
conn.close()
