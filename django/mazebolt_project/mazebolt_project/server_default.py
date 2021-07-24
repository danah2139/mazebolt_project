HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


class Message:
    ADD = bytes([100])
    TEST_TYPE = bytes([101])
    TEST_NAME = bytes([102])
    STOP = bytes([103])

    SUCCESS = bytes([200])
    FAILAURE = bytes([201])

    PING_TEST = bytes([250])
    WGET_TEST = bytes([251])
