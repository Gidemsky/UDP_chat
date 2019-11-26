import sys
from socket import socket, AF_INET, SOCK_DGRAM


def main(args):
    s = socket(AF_INET, SOCK_DGRAM)
    # dest_ip = '127.0.0.1'
    # dest_port = 5029
    dest_ip = args[0]
    dest_port = int(args[1])
    #print "please insert message...\n"
    msg = raw_input()
#    if msg == '4':
#        s.close()
#        msg = 'quit'
    while not msg == 'quit':
        s.sendto(msg.encode(), (dest_ip, dest_port))
        data, sender_info = s.recvfrom(2048)
        if msg == '4':
            s.close()
            break
        if data != "":
            print data.encode()
            msg = raw_input()
        else:
            msg = raw_input()
    s.close()


if __name__ == "__main__":
    main(sys.argv[1:])