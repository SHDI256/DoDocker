import utils.arc_api as arc_api
import os
import json
import shutil
from random import choice

from data.config import PASSWORD


async def get_container(archive, output_dir):
    key = ''.join([choice(list('abcdefghijklmnopqrstuvwxyz1234567890_')) for _ in range(16)])
    arc_api.arc_api.extract_all(archive, output_dir)

    os.system(f'pipreqs {output_dir}')

    mainfile = arc_api.arc_api.get_main_file(output_dir)

    if not mainfile:
        return False

    mainfile = str(mainfile)
    mainfile = mainfile[mainfile.find('/') + 1:]

    with open('dockerfile_template.json') as dockerfile_template:
        docker_data = json.load(dockerfile_template)['dockerfile_data']
        docker_data += [f'ENTRYPOINT [ "python", "./{mainfile}"]']
        docker_data = list(map(lambda s: s + '\n', docker_data))

    with open(f'{output_dir}/Dockerfile', 'w') as dockerfile:
        dockerfile.writelines(docker_data)

    os.chdir(output_dir)
    os.system('echo %s|sudo -S %s' % (PASSWORD, f'sudo docker build -t {key}:0.0 .'))
    os.chdir('../containers')
    os.system('echo %s|sudo -S %s' % (PASSWORD, f'sudo docker save {key}:0.0 > {key}.tar'))
    os.chdir('../')
    shutil.rmtree(output_dir)
    return key
