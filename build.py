#!/usr/bin/env python3

# yay -S discount

import os, sys, subprocess, shutil
import pip

pyenv_f = os.path.join(os.path.dirname(__file__), '.pyenv')
os.makedirs(pyenv_f, exist_ok=True)
sys.path.append(pyenv_f)

# python3 -m pip install --user python-dateutil
try:
  from dateutil import parser
except:
  pip.main(['install', f'--target={pyenv_f}', 'python-dateutil'])
  from dateutil import parser
import datetime
import time

# python3 -m pip install --user htmlmin
try:
  import htmlmin
except:
  pip.main(['install', f'--target={pyenv_f}', 'htmlmin'])
  import htmlmin

if not shutil.which('markdown'):
  subprocess.run('yay -S discount'.split())

if not shutil.which('rclone'):
  subprocess.run('yay -S rclone'.split())


def minify(content):
  return htmlmin.minify(content, remove_comments=True, remove_empty_space=True);

def markdown_to_html(article_index_html, article_index_md, style_path='../style.css'):
  subprocess.run([
  'markdown',
    '-o', article_index_html,
    '-html5',
    article_index_md
  ])
  # Modify the generated html by adding a stylesheet..
  article_index_html_content = ""
  with open(article_index_html, 'r') as fd:
    article_index_html_content = fd.read()

  article_index_html_content = f"""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="{style_path}">
  </head>
  <body>
""".strip() + article_index_html_content + "</body></html>"

  with open(article_index_html, 'w') as fd:
    fd.write(minify(article_index_html_content))

def main():
  www_dir = 'www'

  if 'rm' in sys.argv and os.path.exists(www_dir):
    shutil.rmtree(www_dir)

  if not os.path.exists(www_dir):
    os.makedirs(www_dir)

  # Read in music, anime, etc...

  # Read in all the comics...
  www_dir_c = os.path.join(www_dir, 'c')
  if not os.path.exists(www_dir_c):
    os.makedirs(www_dir_c)

  comic_names = []
  for c_dir_name in os.listdir('comics'):
    c_dir_path = os.path.join('comics', c_dir_name);
    if os.path.isdir(c_dir_path) and len(c_dir_name) > 3:
      print("Processing comic {} (//TODO finish me)".format(c_dir_name))

      comic_src_f = os.path.join(c_dir_path, 'comic.xcf')
      # Copy in to www/c/comic_name.jpg
      comic_www_png = os.path.join(www_dir_c, c_dir_name)+'.png'
      subprocess.run([ # yay -S xcftools
        'xcf2png', '-f', comic_src_f, '-o', comic_www_png
      ])
      comic_www_jpg = os.path.join(www_dir_c, c_dir_name)+'.jpg'
      subprocess.run([ 'convert',
          comic_www_png,
            '-strip', '-interlace', 'Plane', '-gaussian-blur', '0.05', '-quality', '85%',
          comic_www_jpg
      ])
      subprocess.run(['rm', comic_www_png])



  # Read all the articles...
  article_names = []
  # map name -> article_date
  article_dates_map = {}
  
  for a_dir_name in os.listdir('articles'):
    a_dir_path = os.path.join('articles', a_dir_name);
    if os.path.isdir(a_dir_path) and len(a_dir_name) > 3:

      ignore_file = os.path.join(a_dir_path, 'ignore.txt');
      if os.path.exists(ignore_file):
        print('Ignoring {} because ignore.txt exists...'.format(a_dir_name))
        continue
      
      print("Processing article {}".format(a_dir_name))

      # try to get date, try "date.txt" first then use file name
      article_date = None
      article_date_txt = os.path.join(a_dir_path, 'date.txt');
      if os.path.exists(article_date_txt):
        with open(article_date_txt, 'r') as fd:
          article_date = parser.parse( fd.read().strip() )
      if not article_date:
        article_date = time.ctime( os.path.getctime(a_dir_path) )
        print("Warning: no {} found, creating...".format( article_date_txt, article_date ))
        with open(article_date_txt, 'w') as fd:
          fd.write('{}'.format(article_date))
        article_date = parser.parse('{}'.format(article_date))

      article_names.append(a_dir_name)
      article_dates_map[a_dir_name] = article_date

      # Copy in to www/<article name>/
      article_www_dir = os.path.join(www_dir, a_dir_name)

      if os.path.exists(article_www_dir):
        shutil.rmtree(article_www_dir)

      # if not os.path.exists(article_www_dir):
      #   os.makedirs(article_www_dir)
      
      shutil.copytree(a_dir_path, article_www_dir)
      # Inside www/<article name>/ convert markdown to html...

      article_index_html = os.path.join(article_www_dir, 'index.html')

      if not os.path.exists(article_index_html):
        # Create it from whatever we do have...
        article_index_md = os.path.join(article_www_dir, 'index.md')
        if os.path.exists(article_index_md):
          markdown_to_html(article_index_html, article_index_md, style_path='../style.css')

        else:
          # Generate directory contents html file...
          with open(article_index_html, 'w') as fd:
            file_names = [x for x in os.listdir('articles')]

            html = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>"""+a_dir_name.replace('_', ' ').title()+"""</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="../style.css">
  </head>
  <body>
""".strip()
            html += "<h2>Index of {}</h2>".format(a_dir)
            html += "<table><tr><th>File name</th></tr>"

            for f in file_names:
              html += '<tr><td><a href="{}">{}</a></td></tr>'.format(f, f)

            html += "</table>"
            html += "</body>"

            fd.write(minify(html))

  # For each page create a tld file
  for p_file_name in os.listdir('pages'):
    html_f = os.path.join(www_dir, os.path.splitext(p_file_name)[0]+'.html');
    if p_file_name.endswith('.md'):
      markdown_to_html(html_f, os.path.join('pages', p_file_name), style_path='style.css')

    elif p_file_name.endswith('.html'):
      shutil.copy(os.path.join('pages', p_file_name), html_f)

    else:
      print("Ignoring page file {}".format(p_file_name))

  # Copy index asset files in

  shutil.copy(
    'resources/background-design-code-01.jpg',
    os.path.join(www_dir, 'background-design-code-01.jpg')
  )
  # convert /j/photos/profiles/basic-noglass-bl-02-1x1-square.small.png -resize 320x320 /j/photos/profiles/basic-noglass-bl-02-1x1-square.small.jpg
  shutil.copy(
    'resources/basic-noglass-bl-02-1x1-square.small.jpg',
    os.path.join(www_dir, 'basic-noglass-bl-02-1x1-square.small.jpg')
  )

  with open(os.path.join(www_dir, 'style.css'), 'w') as fd:
    with open('style.css', 'r') as style_fd:
      fd.write(minify(style_fd.read()))

  with open(os.path.join(www_dir, 'jeff.asc'), 'w') as fd:
    with open('jeff.asc', 'r') as jeff_fd:
      fd.write(jeff_fd.read())

  # Generate index...
  with open(os.path.join(www_dir, 'index.html'), 'w') as fd:
    html = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Jeffrey McAteer</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="style.css">
    <style>
html {
  background-image: url('background-design-code-01.jpg');
  background-repeat: no-repeat;
  background-size: 100% auto;
  background-clip: padding-box;

  padding: 0;
  padding-top: 24vh;
  padding-top: max(98pt, 24vh);
}
img#profile {
  max-width: 128pt;
  position: absolute;
  top: 2pt;
  top: max(2pt, calc(24vh - 96pt));
  left: 24pt;
  border-radius: 3pt;
}
h1#name {
  padding-top: 68pt;
  padding-top: min(38pt, 38pt); /* old browsers which cannot do a min() will use the first value */
}
    </style>
  </head>
  <body>
    <img id="profile" src="basic-noglass-bl-02-1x1-square.small.jpg">
    <h1 id="name">Jeffrey McAteer</h1>
    <ul>
      <li><a href="code_projects.html">Code Projects</a></li>
      <li><a href="music_i_enjoy.html">Music I Enjoy</a></li>
      <li><a href="anime_i_enjoy.html">Anime I Enjoy</a></li>
      <li><a href="movies_i_enjoy.html">Movies I Enjoy</a></li>
      <li><a href="links.html">Misc. Links</a></li>
      <!-- <li><a href="tracker.html">Tracker App</a></li> -->
    </ul>
    <h1 id="articles">Articles</h1>
""".strip().replace('\n', '');
    html += "<ul>"
    # Sort article_names by date
    article_names = sorted(article_names, key=lambda a: article_dates_map[a], reverse=True)
    for a in article_names:
      date = article_dates_map[a]
      html += '<li><a href="{}/index.html">{}</a><em> ({})</em></li>'.format(
        a, a.replace('_', ' ').title(), date.strftime('%Y-%m-%d')
      )
    html += "</ul>"

    html += "</body></html> \n\n<!-- Congratulations you read a comment!-->\n\n "

    fd.write(minify(html))


  # if "firefox" in args open FF
  if 'firefox' in sys.argv:
    # if I mention an article by name go directly to that...
    ff_url = www_dir+'/index.html'
    for arg in sys.argv:
      if arg in article_names:
        ff_url = www_dir+'/'+arg+'/index.html'
        break;

      for file_name in os.listdir(www_dir):
        if file_name.startswith(arg) and not arg == 'firefox':
          ff_url = www_dir+'/'+file_name
          break;

    subprocess.run(['firefox', ff_url])

  # if "push" in args send it to a google storage bucket
  if 'push' in sys.argv:
    #rclone_storage = "blog-jmcateer-pw"
    # [blog-jmcateer-pw]
    # type = google cloud storage
    # project_number = blog-1586293022512
    # anonymous = false
    # object_acl = bucketOwnerFullControl
    # bucket_acl = publicReadWrite
    # bucket_policy_only = true
    # location = us-east4
    # storage_class = REGIONAL
    #subprocess.run([
    #  'rclone', 'copy',
    #    '--update', '--verbose', '--transfers', '30', '--checkers', '8', '--contimeout', '60s',
    #    '--timeout', '300s', '--retries', '3', '--low-level-retries', '10', '--stats', '1s',
    #    www_dir, rclone_storage+':blog.jmcateer.pw/'
    #])

    # Push to 'loci' / /usr/share/nginx/html
    subprocess.run(['sh', '-c', f'''
rsync -avh "{www_dir}"/. loci:/usr/share/nginx/html --delete
ssh loci sh -c "chown -r nobody:nobody /usr/share/nginx/html"
'''.strip()])





if __name__ == '__main__':
  os.chdir( os.path.dirname(os.path.realpath(__file__)) )
  main()
