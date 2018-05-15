#!/usr/bin/env python
import subprocess

subprocess.run('big-presentation-compose')

emoji = """</body>
<style>
    img.emoji {
        height: 1em;
        width: 1em;
        margin: 0 .05em 0 .1em;
        vertical-align: -0.1em;
     }

</style>
<script src="https://twemoji.maxcdn.com/2/twemoji.min.js?2.6"></script>
  <script>
    twemoji.parse(document.getElementsByTagName('body')[0], {
        folder: 'svg',
        ext: '.svg'
    });
  </script>"""

f = open('index.html')
text = f.read()
f.close()
text = text.replace('</body>', emoji)

with open('index.html', 'w') as f:
    f.write(text)