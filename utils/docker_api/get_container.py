import utils.arc_api as arc_api
import os
import json
import shutil
import asyncio
from random import choice


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)


async def get_container(archive, output_dir):
    KEY = ''.join([choice(list('abcdefghijklmnopqrstuvwxyz1234567890_')) for _ in range(16)])
    arc_api.arc_api.extract_all(archive, output_dir)

    os.system(f'pipreqs {output_dir}')

    mainfile = str(arc_api.arc_api.get_main_file(output_dir))
    mainfile = mainfile[mainfile.find('/') + 1:]

    with open('dockerfile_template.json') as dockerfile_template:
        docker_data = json.load(dockerfile_template)['dockerfile_data']
        docker_data += [f'ENTRYPOINT [ "python", "./{mainfile}"]']
        docker_data = list(map(lambda s: s + '\n', docker_data))

    with open(f'{output_dir}/Dockerfile', 'w') as dockerfile:
        dockerfile.writelines(docker_data)

    os.chdir(output_dir)
    os.system('echo %s|sudo -S %s' % ('li95ue74+', f'sudo docker build -t {KEY}:0.0 .'))
    os.chdir('../containers')
    os.system('echo %s|sudo -S %s' % ('li95ue74+', f'sudo docker save {KEY}:0.0 > {KEY}.tar'))
    os.chdir('../')
    shutil.rmtree(output_dir)
    return KEY
