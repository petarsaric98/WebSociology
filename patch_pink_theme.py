import os
import glob
import re

html_files = glob.glob('c:/Users/petar/Desktop/WebSociology-main/*.html')

css_pink = """        /* Pink Theme Overrides */
        html.theme-pink body { background-color: #3b0728 !important; color: #f9a8d4 !important; }
        html.theme-pink .bg-white, html.theme-pink .dark\:bg-slate-800 { background-color: #500732 !important; }
        html.theme-pink .dark\:bg-slate-900 { background-color: #3b0728 !important; }
        html.theme-pink .dark\:bg-slate-700 { background-color: #700b46 !important; }
        html.theme-pink .dark\:border-slate-800, html.theme-pink .dark\:border-slate-700 { border-color: #831843 !important; }
        html.theme-pink .dark\:text-slate-200, html.theme-pink .dark\:text-white { color: #fbcfe8 !important; }
        html.theme-pink .dark\:text-slate-300, html.theme-pink .dark\:text-slate-400 { color: #f472b6 !important; }
        html.theme-pink .bg-slate-50, html.theme-pink .bg-slate-100 { background-color: #3b0728 !important; }
        html.theme-pink .text-slate-800, html.theme-pink .text-slate-700 { color: #fbcfe8 !important; }
        html.theme-pink .text-slate-500, html.theme-pink .text-slate-400 { color: #f472b6 !important; }
        html.theme-pink .border-slate-100, html.theme-pink .border-slate-200 { border-color: #831843 !important; }
        html.theme-pink .hover\:bg-slate-200:hover, html.theme-pink .dark\:hover\:bg-slate-700:hover { background-color: #700b46 !important; }
        html.theme-pink .bg-white\/90 { background-color: rgba(80, 7, 50, 0.9) !important; }
        html.theme-pink .dark\:bg-slate-900\/90 { background-color: rgba(59, 7, 40, 0.9) !important; }
        html.theme-pink .shadow-sm, html.theme-pink .shadow-md, html.theme-pink .shadow-lg, html.theme-pink .shadow-xl, html.theme-pink .shadow-2xl { box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2) !important; }
    </style>"""

svg_green = '<svg id="theme-toggle-green-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5 2a1 1 0 011 1v1h1a1 1 0 010 2H6v1a1 1 0 01-2 0V6H3a1 1 0 010-2h1V3a1 1 0 011-1zm0 10a1 1 0 011 1v1h1a1 1 0 110 2H6v1a1 1 0 11-2 0v-1H3a1 1 0 110-2h1v-1a1 1 0 011-1zM12 2a1 1 0 01.967.744L14.146 7.2 17.5 9.134a1 1 0 010 1.732l-3.354 1.935-1.18 4.455a1 1 0 01-1.933 0L9.854 12.8 6.5 10.866a1 1 0 010-1.732l3.354-1.935 1.18-4.455A1 1 0 0112 2z" clip-rule="evenodd" /></svg>'

svg_pink = svg_green + '\\n                        <svg id="theme-toggle-pink-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" /></svg>'

js_icon1 = "const themeToggleGreenIcon = document.getElementById('theme-toggle-green-icon');"
js_icon2 = js_icon1 + "\\n        const themeTogglePinkIcon = document.getElementById('theme-toggle-pink-icon');"

js_hidden1 = "themeToggleGreenIcon.classList.add('hidden');"
js_hidden2 = js_hidden1 + "\\n            if (themeTogglePinkIcon) themeTogglePinkIcon.classList.add('hidden');"

js_rm = "document.documentElement.classList.remove('dark', 'theme-green');"
js_rm2 = "document.documentElement.classList.remove('dark', 'theme-green', 'theme-pink');"

for file in html_files:
    print(f"Processing {file}")
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'theme-pink' in content:
        print(f"Already patched {file}")
        continue
    
    content = content.replace('</style>', css_pink, 1)
    content = content.replace(svg_green, svg_pink)
    content = content.replace(js_icon1, js_icon2)
    content = content.replace(js_hidden1, js_hidden2)
    content = content.replace(js_rm, js_rm2)
    
    content = re.sub(
        r"\} else if \(theme === 'green'\) \{\s*themeToggleGreenIcon\.classList\.remove\('hidden'\);\s*document\.documentElement\.classList\.add\('dark', 'theme-green'\);\s*\} else \{",
        r"} else if (theme === 'green') {\n                themeToggleGreenIcon.classList.remove('hidden');\n                document.documentElement.classList.add('dark', 'theme-green');\n            } else if (theme === 'pink') {\n                if (themeTogglePinkIcon) themeTogglePinkIcon.classList.remove('hidden');\n                document.documentElement.classList.add('dark', 'theme-pink');\n            } else {",
        content
    )

    content = re.sub(
        r"\} else if \(currentTheme === 'dark'\) \{\s*setTheme\('green'\);\s*\} else \{\s*setTheme\('light'\);\s*\}",
        r"} else if (currentTheme === 'dark') {\n                setTheme('green');\n            } else if (currentTheme === 'green') {\n                setTheme('pink');\n            } else {\n                setTheme('light');\n            }",
        content
    )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {file}")
