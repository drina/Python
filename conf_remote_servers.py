import yaml
import paramiko
from paramiko import AutoAddPolicy


def read_yaml(file):
    with open(file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)


def establish_ssh_connection(host, user, key_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    try:
        private_key = paramiko.RSAKey.from_private_key_file(key_file)
        ssh.connect(host, username=user, pkey=private_key)
        return ssh
    except Exception as e:
        print(e)
        return None


def configure_remote_server(ssh, config):
    stdin, stdout, stderr = ssh.exec_command(config)
    output = stdout.read().decode('utf-8')
    return output


def close_ssh_connection(ssh):
    ssh.close()


def main(server_config_file, ip_file, key_file, user):
    server_config = read_yaml(server_config_file)
    server_ips = read_yaml(ip_file)

    for ip in server_ips:
        ssh = establish_ssh_connection(ip, user, key_file)
        if ssh:
            for config in server_config:
                output = configure_remote_server(ssh, config)
                print(f"Configuration output for {ip}: {output}")
            close_ssh_connection(ssh)
        else:
            print(f"Failed to establish SSH connection with {ip}")


if __name__ == "__main__":
    main("server_config.yaml", "server_ips.yaml", "key_file", "ubuntu")