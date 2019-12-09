import markdown2

md = markdown2.markdown(open('0002_TimeAPI_Kata.md').read())

with open('kata.html', 'w') as f:
  f.write(md)
