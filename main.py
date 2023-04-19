import subprocess
import os


def check_docker():
    try:
        ret = subprocess.run(['docker', 'version'],
                             capture_output=True,
                             check=True)
        content = ret.stdout.decode('utf-8')
        print(content)
        return True
    except subprocess.CalledProcessError:
        print('Docker is not installed or not running.')
        return False


def rm_docker_image(image_id):
    try:
        ret = subprocess.run(['docker', 'rmi', '-f', image_id],
                             shell=True,
                             capture_output=True,
                             check=True)
        print(ret)
        content = ret.stdout.decode('utf-8')
        print(content)
        return True
    except subprocess.CalledProcessError:
        print('rm docker image failed.')
        return False


def query_docker_image():
    try:
        ret = subprocess.run([
            'docker', 'images',
            '--format="{{json .Repository}}-*-{{json .ID}}"'
        ],
                             capture_output=True,
                             check=True)
        print(ret.stdout)
        content = ret.stdout.decode('utf-8')
        for line in content.splitlines():
            if 'yunjing' in line:
                print("yunjing image is found.")
                return line.split('-*-')[1].strip('"')
        return None
    except subprocess.CalledProcessError:
        print('subprocess.CalledProcessError')
        return None


def query_docker_container():
    try:
        ret = subprocess.run([
            'docker', 'ps', '-a',
            '--format="{{json .Image}}-*-{{json .ID}}-*-{{json .Names}}"'
        ],
                             capture_output=True,
                             check=True)
        #print(ret.stdout)
        content = ret.stdout.decode('utf-8')
        for line in content.splitlines():
            if 'yunjing' in line:
                print("yunjing container is created.")
                return line.split('-*-')[1].strip('"')
        return None
    except subprocess.CalledProcessError:
        print('Docker container is not running.')
        return None


def rm_docker_container(container_id):
    try:
        ret = subprocess.run(['docker', 'rm', '-f', container_id],
                             shell=True,
                             capture_output=True,
                             check=True)
        print(ret)
        content = ret.stdout.decode('utf-8')
        print(content)
        return True
    except subprocess.CalledProcessError:
        print('rm docker container failed.')
        return False


# docker run -d -p 8081:8081 -p 5005:5005  -v D:\Data\docker_local\cloud\config:/opt/cloud/config -v D:\Data\docker_local\cloud\data:/cam/onlineapp/config/  --name local yujing:latest
def run_docker_container():
    try:
        ret = subprocess.run([
            'docker', 'run', '-d', '-p', '8081:8081', '-p', '5005:5005', '-v',
            'D:\Data\docker_local\cloud\config:/opt/cloud/config', '-v',
            'D:\Data\docker_local\cloud\data:/cam/onlineapp/config/', '--name',
            'yunjing', 'yunjing:latest'
        ],
                             capture_output=True,
                             check=True)
        content = ret.stdout.decode('utf-8')
        print(content)
        return True
    except subprocess.CalledProcessError:
        print('Docker container is not running.')
        return False


def build_docker_image():
    try:
        ret = subprocess.run(['docker', 'build', '-t', 'yunjing:latest', '.'],
                             check=True)
        print(ret)
        #content = ret.stderr.decode('utf-8')
        #print(content)
        return True
    except Exception:
        print('build docker image failed.')
        return False


def mvn_package():
    try:
        ret = subprocess.run(['mvn', 'package', '-Dmaven.test.skip=true'],
                             shell=True,
                             check=True)
        if ret.returncode == 0:
            print('mvn package success.')
            return True
        return False
    except subprocess.CalledProcessError:
        print('mvn package failed.')
        return False


def run():
    if check_docker() is not True:
        print("docker is not installed or not running.")
        return

    container_id = query_docker_container()

    if container_id is not None:
        print(container_id)
        rm_docker_container(container_id)

    image_id = query_docker_image()
    if image_id is not None:
        print(image_id)
        rm_docker_image(image_id)

    work_dir = os.getcwd()

    if work_dir != 'D:\\Work\\Code\\yjweb':
        os.chdir('D:\\Work\\Code\\yjweb')

    print("begin to run mvn package")
    ret = mvn_package()
    if ret is not True:
        print("mvn package failed.")
        return

    print("begin to build docker image")

    ret = build_docker_image()
    if ret is not True:
        print("build docker image failed.")
        return

    ret = run_docker_container()
    if ret is not True:
        print("run docker container failed.")
        return


if __name__ == '__main__':
    run()