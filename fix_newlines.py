import glob

html_files = glob.glob('c:/Users/petar/Desktop/WebSociology-main/*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace literal \n with actual newline
    content = content.replace('\\n', '\n')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed newlines in {file}")
