import sys
sys.stdout.reconfigure(encoding='utf-8')
import openpyxl
import json

wb = openpyxl.load_workbook('pitanja matur.xlsx')
ws = wb.active

questions = []
for row in ws.iter_rows(min_row=2, max_col=5, values_only=True):
    pitanje, tip, ponudeni, tocan, godina = row
    if not pitanje or not tip:
        continue
    
    q = {
        'pitanje': str(pitanje).strip(),
        'tip': str(tip).strip(),
        'ponudeni': str(ponudeni).strip() if ponudeni else '',
        'tocan': str(tocan).strip() if tocan else '',
        'godina': str(godina).strip() if godina else ''
    }
    questions.append(q)

# Write as JSON
with open('matura_pitanja.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Exported {len(questions)} questions to matura_pitanja.json")

# Also print stats
tips = {}
for q in questions:
    tips[q['tip']] = tips.get(q['tip'], 0) + 1
print("\nStats:")
for k, v in sorted(tips.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

# Check some edge cases for ponudeni format
print("\n=== Checking ponudeni format consistency ===")
for q in questions[:5]:
    if q['tip'] == 'Zadatci višestrukog izbora':
        print(f"  Format: {q['ponudeni'][:100]}")
        break

# Check if '-' means no options
no_opts = sum(1 for q in questions if q['ponudeni'] in ['-', 'None', ''])
print(f"\nQuestions with no options: {no_opts}")
