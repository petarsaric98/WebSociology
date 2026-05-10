import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\petar\Desktop\WebSociology-main\matura_pitanja.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Build JS data structure
js_questions = []
for q in questions:
    tip = q['tip']
    pitanje = q['pitanje'].replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ').replace('\r', '')
    tocan = q['tocan'].replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ').replace('\r', '')
    ponudeni = q['ponudeni'].replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ').replace('\r', '')
    godina = q['godina'].replace("'", "\\'")
    
    # Determine rendering type
    if tip == 'Zadatci višestrukog izbora' or tip == 'Skupina zadataka':
        if ponudeni and ponudeni != '-':
            render = 'mcq'
        else:
            render = 'short'
    elif tip == 'Zadatci višestrukih kombinacija':
        render = 'multi'
    elif tip == 'Zadatci povezivanja i sređivanja':
        render = 'match'
    elif tip == 'Zadatci dopunjavanja':
        render = 'fill'
    elif tip == 'Zadatci kratkog odgovora' or tip == 'Zadatci kratkog i produženog odgovora':
        render = 'short'
    elif tip == 'Zadatci produženog odgovora':
        render = 'long'
    else:
        render = 'short'
    
    js_questions.append(f"{{p:'{pitanje}',t:'{tip}',o:'{ponudeni}',a:'{tocan}',g:'{godina}',r:'{render}'}}")

# Write JS file
with open(r'c:\Users\petar\Desktop\WebSociology-main\matura_data.js', 'w', encoding='utf-8') as f:
    f.write('const MATURA_DB = [\n')
    for i, jq in enumerate(js_questions):
        comma = ',' if i < len(js_questions)-1 else ''
        f.write(f'  {jq}{comma}\n')
    f.write('];\n')

print(f"Written {len(js_questions)} questions to matura_data.js")

# Count by render type
renders = {}
for q in js_questions:
    r = q.split("r:'")[1].split("'")[0]
    renders[r] = renders.get(r, 0) + 1
for k,v in renders.items():
    print(f"  {k}: {v}")
