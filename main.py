from flask import Flask, render_template, request, redirect
import os.path
import markdown2

app = Flask("mdiki")

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app.wsgi_app = ReverseProxied(app.wsgi_app)



def to_dict(args):
    outdict = {}
    for key, val in args.items():
        outdict[key] = val
    return outdict



@app.route('/')
def index():
    return render_template('index.html')

def make_fs_path(parts):
    """returns joined path from parts"""
    return '/'.join(parts)

def get_content(subpath, base_path=None):
    if base_path is None:
        base_path = 'diki'
    base_path = [base_path]
    # remove trailing slash
    if subpath.endswith('/'):
        subpath = subpath[:-1]
    # split subpath into its parts
    parts = subpath.split('/')
    # check if the complete path is available 
    checkpath = base_path + parts
    if os.path.isdir(make_fs_path(checkpath)):
        # the complete path is a directory, 
        # so check for index.md, load and return
        index_path = make_fs_path(checkpath + ['index.md'])
        if os.path.isfile(index_path):
            with open(index_path) as mdfile:
                content = mdfile.read()
            return content
    elif os.path.isfile(make_fs_path(checkpath[:-1] + [checkpath[-1] + '.md'])):
        # the path is a directory, but last element is a .md file
        with open('/'.join(checkpath) + '.md') as mdfile:
            content = mdfile.read()
        return content

def save_content(subpath, content, base_path=None):
    if base_path is None:
        base_path = 'diki'
    base_path = [base_path]
    # remove trailing and/or leading slash
    if subpath.endswith('/'):
        subpath = subpath[:-1]
    if subpath.startswith('/'):
        subpath = subpath[1:]
    # split path into parts
    parts = subpath.split('/')
    # check if the complete path is available 
    checkpath = base_path + parts
    if os.path.isdir(make_fs_path(checkpath)):
        # the complete path is a directory, 
        # so check for index.md, save and return
        index_path = make_fs_path(checkpath + ['index.md'])
        if os.path.isfile(index_path):
            with open(index_path, 'w') as mdfile:
                mdfile.write(content)
            return content
    elif os.path.isfile(make_fs_path(checkpath[:-1] + [checkpath[-1] + '.md'])):
        # the path is a directory, but last element is a .md file
        with open('/'.join(checkpath) + '.md', 'w') as mdfile:
            mdfile.write(content)
        return content
    else:
        # neither index.md nor path found, create path + '.md'
        create = base_path
        for elem in checkpath[:-1]:
            if not os.path.isdir(elem):
                create.append(elem)
                if not os.path.isdir('/'.join(create)):
                    os.mkdir('/'.join(create))
        with open('/'.join(create) + '/' + checkpath[-1] + '.md', 'w') as mdfile:
            mdfile.write(content)
        return content


@app.route('/<path:subpath>')
def edit(subpath):
    content = get_content(subpath)
    html_content = 'Just start typing.'
    if content is not None:
        html_content = markdown2.markdown(content)
    return render_template('editor.html', content=content, html_content=html_content)

@app.route('/<path:subpath>/save', methods=['POST'])
def save(subpath):
    content = request.form['content']
    content = save_content(subpath, content)
    return redirect(subpath)
    #return render_template('editor.html', content=content)
