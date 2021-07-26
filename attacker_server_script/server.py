import socket
import server_default
import os
import threading
CURRENT_TESTS = {}


def main():
    t1 = threading.Thread(target=run_tests)
    t1.start()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((server_default.HOST, server_default.PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)  # ping, test2
                print(data)
                if data == server_default.Message.ADD:
                    handle_add(conn)
                elif data == server_default.Message.STOP:
                    handle_stop(conn)
                elif data:
                    conn.send(server_default.Message.FAILAURE)


def get_test_name(conn):
    conn.send(server_default.Message.TEST_NAME)
    data = conn.recv(1024)
    name = data.decode()
    return name


def handle_check_exist(test_name, command):
    if test_name in CURRENT_TESTS.keys():
        message = server_default.Message.FAILAURE
    else:
        CURRENT_TESTS[test_name] = {"command": command, "is_running": True}
        message = server_default.Message.SUCCESS
    return message


def handle_add(conn):
    conn.send(server_default.Message.TEST_TYPE)
    test_type_data = conn.recv(1024)
    test_name = get_test_name(conn)
    if test_type_data == server_default.Message.PING_TEST:
        message = handle_check_exist(test_name, 'ping')
        conn.send(message)
    elif test_type_data == server_default.Message.WGET_TEST:
        message = handle_check_exist(test_name, 'wget')
        conn.send(message)
    else:
        conn.send(server_default.Message.FAILAURE)


def handle_stop(conn):
    test_name = get_test_name(conn)
    if test_name in CURRENT_TESTS.keys():
        CURRENT_TESTS[test_name]["is_running"] = False
        message = server_default.Message.SUCCESS
    else:
        message = server_default.Message.FAILAURE
    conn.send(message)


def run_tests():
    while True:
        for current_test in CURRENT_TESTS:
            if current_test["is_running"]:
                if current_test["command"] == "ping":
                    os.system('ping -c 1 mazebolt.com')

                elif current_test["command"] == "wget":
                    os.system('wget mazebolt.com')


if __name__ == "__main__":
    main()
