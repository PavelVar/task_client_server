from client import MessangerClient


server_ip = '192.168.1.104'

port_num = 11111

if __name__ == '__main__':
    client = MessangerClient((server_ip, port_num))
    client.start()
