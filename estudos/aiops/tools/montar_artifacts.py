import re
import os, sys
# Uso: python3 tools/montar_artifacts.py <pasta-de-saida>  (precisa de <pasta>/urls.json com plano, l1, l2...)
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
out=os.path.abspath(sys.argv[1])+'/'
css=open(root+'assets/estilo.css').read()
quiz=open(root+'assets/quiz.js').read()
# tema: bloco escuro guardado + data-theme
m=re.search(r'@media \(prefers-color-scheme: dark\) \{\n  :root \{(.*?)\}\n\}', css, re.S)
dark=m.group(1)
css=css.replace(m.group(0), '@media (prefers-color-scheme: dark) {\n  :root:not([data-theme="light"]) {'+dark+' color-scheme: dark; }\n}\n:root[data-theme="dark"] {'+dark+' color-scheme: dark; }')
css=css.replace('main { max-width: 42rem; margin: 0 auto; padding: 3rem 1rem 5rem; position: relative; }',
 'main { max-width: 42rem; margin: 0 auto; padding-block: 3rem 5rem; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); position: relative; }')
css=css.replace('main { padding-top: 2rem; }','main { padding-block-start: 2rem; }')
css=css.replace('main, main.wide { max-width: none; padding: 0; }','main, main.wide { max-width: none; padding-block: 0; }')
assert 'padding: 3rem' not in css
GH='https://github.com/leoporto15/slideless/blob/main/estudos/aiops/'
def build(src, dst, links):
    h=open(root+src).read()
    title=re.search(r'<title>(.*?)</title>',h).group(1)
    body=re.search(r'<body>\n(.*)</body>',h,re.S).group(1)
    for js in re.findall(r'<script src="\.\./assets/([\w-]+\.js)"></script>', body):
        body=body.replace(f'<script src="../assets/{js}"></script>','<script>\n'+open(root+'assets/'+js).read().replace('</script',r'<\/script')+'</script>')
    for a,b in links.items(): body=body.replace(a,b)
    open(out+dst,'w').write(f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n<style>\n{css}</style>\n{body}')
import json
U=json.load(open(out+'urls.json'))
L={'href="../MISSION.md"':f'href="{GH}MISSION.md"',
   'href="../reference/plano-de-estudo.html"':f'href="{U["plano"]}"',
   'href="../lessons/0001-kb-mcp-ou-instrucao.html"':f'href="{U["l1"]}"',
   'href="../lessons/0002-tokens.html"':f'href="{U["l2"]}"',
   'href="0001-kb-mcp-ou-instrucao.html"':f'href="{U["l1"]}"',
   'href="0002-tokens.html"':f'href="{U["l2"]}"'}
build('reference/plano-de-estudo.html','plano-de-estudo.html',L)
build('lessons/0001-kb-mcp-ou-instrucao.html','licao-0001.html',L)
build('lessons/0002-tokens.html','licao-0002.html',L)
