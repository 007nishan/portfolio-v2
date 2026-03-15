from app import app, db, Challenge
import json

with app.app_context():
    challenges = Challenge.query.all()
    found_any = False
    for c in challenges:
        # Check all text fields
        fields_to_check = {
            "title": c.title,
            "fcc_description": c.fcc_description,
            "problem_text": c.problem_text,
            "concepts_text": c.concepts_text,
            "solution_code": c.solution_code,
            "quote_text": c.quote_text,
            "qa_text": c.qa_text
        }
        
        for field_name, content in fields_to_check.items():
            if content and "FCC" in content.upper():
                print(f"MATCH in {c.date_id} -> Field {field_name}:")
                # print a snippet around the match
                idx = content.upper().find("FCC")
                start = max(0, idx - 20)
                end = min(len(content), idx + 20)
                print(f"  Snippet: ...{content[start:end]}...")
                found_any = True
    
    if not found_any:
        print("No matches found in Challenge table content.")
