#!/usr/bin/env python3

# yay -S discount

import os, sys, subprocess, shutil

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
    <link rel="stylesheet" href="{style_path}">
  </head>
  <body>
""".strip() + article_index_html_content + "</body></html>"

  with open(article_index_html, 'w') as fd:
    fd.write(article_index_html_content)

def main():
  www_dir = 'www'

  if 'rm' in sys.argv and os.path.exists(www_dir):
    shutil.rmtree(www_dir)

  if not os.path.exists(www_dir):
    os.makedirs(www_dir)

  # Read in music, anime, etc...

  # Read all the articles...
  article_names = []
  
  for a_dir_name in os.listdir('articles'):
    a_dir_path = os.path.join('articles', a_dir_name);
    if os.path.isdir(a_dir_path) and len(a_dir_name) > 3:
      
      print("Processing article {}".format(a_dir_name))

      article_names.append(a_dir_name)
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

            fd.write(html)

  # For each page create a tld file
  for p_file_name in os.listdir('pages'):
    if p_file_name.endswith('.md'):
      html_f = os.path.join(www_dir, os.path.splitext(p_file_name)[0]+'.html');
      markdown_to_html(html_f, os.path.join('pages', p_file_name), style_path='style.css')

    else:
      print("Ignoring page file {}".format(p_file_name))

  # Copy some files in
  shutil.copy(
    '/j/res/profiles/background-design-code-01.jpg',
    os.path.join(www_dir, 'background-design-code-01.jpg')
  )
  shutil.copy(
    '/j/res/profiles/basic-noglass-bl-02-1x1-square.small.png',
    os.path.join(www_dir, 'basic-noglass-bl-02-1x1-square.small.png')
  )

  with open(os.path.join(www_dir, 'style.css'), 'w') as fd:
    fd.write("""
body {
  min-height: 60vh;
  margin:40px auto;
  max-width: 680px;
  line-height: 1.6;
  font-size: 18px;
  
  padding: 2pt 9pt;
  padding-bottom: 300pt;
  padding-bottom: 80vh;

  text-align: left;
  margin: 0 8pt;

  border-radius: 3pt;
}
h1, h2, h3, p {
  margin: 2pt 0;
  line-height:1.2;
}
a:link { color: #268bd2; }
a:visited { color: #2aa198; }
a:hover { color: #209090; }
a:active { color: #209090; }

/** Not theme-specific, but corrections for browser defaults I dislike */

html::-webkit-scrollbar, body::-webkit-scrollbar {
  display: none; /* Chrome, Safari and Opera */
}
html, body {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
} 

/** Theme-specific stuff, we repeat the light style for old devices which error on @media queries */

html, body {
  background: #fdf6e3;
  color: #586e75;
}

@media (prefers-color-scheme: light) {
  html, body {
    background: #fdf6e3;
    color: #586e75;
  }
}

@media (prefers-color-scheme: dark) {
  html, body {
    background: #002b36;
    color: #586e75;
  }
}

""".strip()
    )

  # Generate index...
  with open(os.path.join(www_dir, 'index.html'), 'w') as fd:
    html = """
<!doctype html>
<html>
  <head>
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
    <img id="profile" src="basic-noglass-bl-02-1x1-square.small.png">
    <h1 id="name">Jeffrey McAteer</h1>
    <ul>
      <li><a href="code_projects.html">Code Projects</a></li>
      <li><a href="music_i_enjoy.html">Music I Enjoy</a></li>
      <li><a href="anime_i_enjoy.html">Anime I Enjoy</a></li>
    </ul>
    <h1 id="articles">Articles</h1>
""".strip().replace('\n', '');
    html += "<ul>"
    for a in article_names:
      html += '<li><a href="{}/index.html">{}</a></li>'.format(
        a, a.replace('_', ' ').title()
      )
    html += "</ul>"

    html += "</body></html> \n\n<!-- Congratulations you read a comment!-->\n\n "

    fd.write(html)


  # if "firefox" in args open FF
  if 'firefox' in sys.argv:
    # if I mention an article by name go directly to that...
    ff_url = www_dir+'/index.html'
    for arg in sys.argv:
      if arg in article_names:
        ff_url = www_dir+'/'+arg+'/index.html'
        break;

    subprocess.run(['firefox', ff_url])

  # if "push" in args send it to a google storage bucket
  if 'push' in sys.argv:
    rclone_storage = "blog-jmcateer-pw"
    # [blog-jmcateer-pw]
    # type = google cloud storage
    # project_number = blog-1586293022512
    # anonymous = false
    # object_acl = bucketOwnerFullControl
    # bucket_acl = publicReadWrite
    # bucket_policy_only = true
    # location = us-east4
    # storage_class = REGIONAL
    subprocess.run([
      'rclone', 'copy',
        '--update', '--verbose', '--transfers', '30', '--checkers', '8', '--contimeout', '60s',
        '--timeout', '300s', '--retries', '3', '--low-level-retries', '10', '--stats', '1s',
        www_dir, rclone_storage+':blog.jmcateer.pw/'
    ])




if __name__ == '__main__':
  os.chdir( os.path.dirname(os.path.realpath(__file__)) )
  main()
