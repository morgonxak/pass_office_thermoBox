import paramiko

PRODUCTION_SERVER = '10.10.22.201'
PRODUCTION_USER = 'pi'
secret = 'asm123'
port = 22
def getCommand():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=PRODUCTION_SERVER, port=22, username=PRODUCTION_USER, password=secret)
    stdin, stdout, stderr = client.exec_command('ls')

    for line in stdout:
        print(line.strip('\n'))

    del stdin

    client.close()

def cp(localpath, remotepath):
    try:
        transport = paramiko.Transport((PRODUCTION_SERVER, port))
        transport.connect(username=PRODUCTION_USER, password=secret)
    except paramiko.ssh_exception.SSHException as e:
        print("error connect: {}".format(e))
        return -1

    sftp = paramiko.SFTPClient.from_transport(transport)

    sftp.put(localpath, remotepath)
    sftp.close()
    transport.close()
    return 0

cp('/home/dima/PycharmProjects/pass_office_thermoBox/rc/TEST', '/home/pi/project/recognition_service_client_simplified/TEST')