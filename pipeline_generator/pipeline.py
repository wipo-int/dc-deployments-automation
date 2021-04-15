import jinja2 as j2
from pathlib import Path
import os

PIPELINE_TEMPLATE_J2_FILE = 'templates/bitbucket-pipelines.yml.j2'
ROLES_DIR = 'roles/'


def find_all_scenarios():
    scenario_dirs = []
    for root, dirs, files in os.walk('..'):
        [scenario_dirs.append(Path(root)) for f in files if f.endswith("molecule.yml")]
    return sorted(scenario_dirs)


def load_template():
    jenv = j2.Environment(
        loader=j2.FileSystemLoader('.'),
        lstrip_blocks=True,
        trim_blocks=True)
    return jenv.get_template(PIPELINE_TEMPLATE_J2_FILE)

def main():
    scenario_paths = find_all_scenarios()

    template = load_template()
    generated_output = template.render(scenario_paths=scenario_paths)

    print(generated_output)


if __name__ == '__main__':
    main()
