import toml


def get_project_info():
    with open('pyproject.toml', 'r') as f:
        pyproject = toml.load(f)
        name = pyproject['tool']['poetry']['name']
        version = pyproject['tool']['poetry']['version']
        description = pyproject['tool']['poetry']['description']

        return name, version, description
