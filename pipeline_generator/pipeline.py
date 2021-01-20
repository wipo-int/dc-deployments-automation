from jinja2 import Template
from pathlib import Path
import os

PIPELINE_TEMPLATE_J2_FILE = 'templates/bitbucket-pipelines.yml.j2'
ROLES_DIR = 'roles/'


def find_all_scenarios():
    scenario_dirs = []
    for root, dirs, files in os.walk(Path(os.path.join(os.path.dirname(__file__), "..", ROLES_DIR))):
        [scenario_dirs.append(Path(root)) for f in files if f.endswith("molecule.yml")]
    return scenario_dirs


def load_template():
    path = Path(os.path.join(os.path.dirname(__file__), PIPELINE_TEMPLATE_J2_FILE))
    return Template(path.read_text())


def main():
    template = load_template()

    scenario_paths = find_all_scenarios()
    generated_output = template.render(scenario_paths=scenario_paths)

    print(generated_output)


if __name__ == '__main__':
    main()
