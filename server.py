
import sys

from socket import socket, AF_INET, SOCK_DGRAM


class Person:
    def __init__(self, info, name):
        self.info = info
        self.name = name
        self.msgs = []


# checking if message of the clients are valid
def msg_check(chat_input):
    words = chat_input.split(" ", 1)
    try:
        num = int(words[0])
        if 0 < num < 4:
            return [num, words[1]]
        elif num == 4 or num == 5:
            return [num, "nothing"]
        else:
            return []
    except:
        return []


# the function takes person data and prepare
# outgoing message back to the client
def message_builder(peron):
    output_msg = ""
    for msg in peron.msgs:
        output_msg += (msg + "\n")
        # get rid off the last '\n'
    output_msg = output_msg[:len(output_msg) - 1]
    # reset the message list
    peron.msgs = []
    return output_msg


# adds the out going messages per user in the chat
def add_msg(user_list, msg, cur_user_sender_info, s):
    cur_user = 0
    for p in user_list:
        if p.info == cur_user_sender_info:
            cur_user = p
            continue
        # adds the relevant message
        p.msgs.append(msg)
    if user_list.__len__() != 0 and cur_user != 0:
        s.sendto(message_builder(cur_user), cur_user_sender_info)
    else:
        s.sendto("", cur_user_sender_info)


# the main commands function.
# it executes the actions depends the user input (1 - 5)
def cmd_execute(cmd_type, user_msg, people, sender_info, s):
    if cmd_type is 1:
        exist = False
        chat_users = ""
        # creating list of other peoples names
        for p in people:
            exist = True
            p.msgs.append(user_msg + " has joined")
            chat_users += p.name
            chat_users += ", "
        if exist:
            chat_users = chat_users[:len(chat_users) - 2]
            s.sendto(chat_users, sender_info)
        else:
            s.sendto("", sender_info)
        # creating new person and adding to people dictionary
        pers = Person(sender_info, user_msg)
        people.append(pers)
    elif cmd_type is 2:
        sender_name = ""
        # finding senders name and reading his messages
        for p in people:
            if p.info == sender_info:
                sender_name = p.name
                break
        new_msg = sender_name + ": " + user_msg
        # add message to all peoples dictionary except sender
        add_msg(people, new_msg, sender_info, s)
    elif cmd_type is 3:
        # changing persons name
        prev_name = ""
        for p in people:
            if p.info == sender_info:
                prev_name = p.name
                p.name = user_msg
                break
        new_msg = prev_name + " has changed his name to " + user_msg
        # adding a user name changed for everyone else
        add_msg(people, new_msg, sender_info, s)
    elif cmd_type is 4:
        # deletes the information and closes later the its socket
        leaving_user = ""
        for p in people:
            if p.info == sender_info:
                leaving_user = p.name
                people.remove(p)
        new_msg = leaving_user + " has left the group"
        # adding a new message for everyone else
        add_msg(people, new_msg, sender_info, s)
    elif cmd_type is 5:
        # finding sender
        for p in people:
            if p.info == sender_info:
                # sending all messages and clearing msgs list
                s.sendto(message_builder(p), sender_info)
                break


def main(args):
    people = []
    s = socket(AF_INET, SOCK_DGRAM)
    src_ip = '0.0.0.0'
    src_port = int(args[0])
    s.bind((src_ip, src_port))

    while True:
        data, sender_info = s.recvfrom(2048)
        msg_list = msg_check(data)
        if msg_list:
            cmd_execute(msg_list[0], msg_list[1], people, sender_info, s)
        else:
            s.sendto("Illegal request", sender_info)


if __name__ == "__main__":
    main(sys.argv[1:])
