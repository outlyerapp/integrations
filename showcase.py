import pathlib
import yaml

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route('/')
def showcase():
    integrations = dict()
    top = pathlib.Path('.')
    for package in top.glob('*/package.yaml'):  # type: pathlib.Path
        package_name = package.parent.name
        package_yaml = yaml.safe_load(open(package, 'r'))
        package_yaml['name'] = package_name
        integrations[package_name] = package_yaml

    return render_template('showcase.html', integrations=integrations)


@app.route('/logo/<package>/<path:filename>')
def custom_static(package, filename):
    return send_from_directory(package, filename)

if __name__ == '__main__':
    app.run()
