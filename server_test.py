import ctypes
import unittest
import socket

from server import Server

HOST = 'localhost'
PORT = 9001


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.default_server = Server(HOST, PORT)

    def tearDown(self):
        if self.default_server.server_socket:
            self.default_server.server_socket.close()
        self.default_server = None

    # init and util ------------------------------------------------------

    def test__server_can_construct_will_no_args(self):
        self.assertTrue(Server())

    def test__server_does_not_init_with_listen_socket_object(self):
        s = Server()
        self.assertIsNone(s.server_socket)

    def test__on_init_server_value__socket_is_bound__is_false(self):
        s = Server()
        self.assertFalse(s.socket_is_bound)

    def test__on_init_server_value__socket_is_listening__is_false(self):
        s = Server()
        self.assertFalse(s.socket_is_listening)

    def test__on_init_server_value__host__is_none_if_user_supplied_no_value(self):
        s = Server()
        self.assertFalse(s.host)

    def test__on_init_server_value__port__is_none_if_user_supplied_no_value(self):
        s = Server()
        self.assertFalse(s.port)

    def test__on_init_server_value__thread_count__is_zero(self):
        s = Server()
        self.assertEqual(s.thread_count, 0)

    def test__on_init_server_value__connections__is_none(self):
        s = Server()
        self.assertIsNone(s.connections)

    def test__on_init_server_value__connection_timeout_s__is_correct(self):
        s = Server()
        self.assertEqual(s.connection_timeout_s, 0.001)

    def test__on_init_server_values__host_and_port__reflect_user_supplied_values(self):
        s = self.default_server
        self.assertEqual(s.host, HOST)
        self.assertEqual(s.port, PORT)

    def test__fn_set_bit__sets_correct_bit_on(self):
        s = self.default_server
        for i in range(32):
            bit = s.set_bit(0, i, True)
            self.assertEqual(bit, 2**i)

    def test__fn_set_bit__sets_correct_bit_off(self):
        s = self.default_server
        for i in range(32):
            bit = s.set_bit(2**i-1, i, False)
            self.assertEqual(bit, 2**i-1)

    def test__fn_bit_is_set__returns_correct_value(self):
        s = self.default_server
        for i in range(32):
            self.assertTrue(s.bit_is_set(2**i, i))

    def test__fn_bit_is_set__does_not_accept_negative_idx_value(self):
        s = self.default_server
        # a -1 gets turned into idx=0
        self.assertTrue(s.bit_is_set(2**0, -1))
        self.assertFalse(s.bit_is_set(2**1, -1))

    def test__fn_get_header__returns_correct_header_for_parameters(self):
        s = self.default_server
        for i in range(8):
            header = s.get_header(2**i, 2**i, 2**i)
            self.assertEqual(header.b.type, 2**i)
            self.assertEqual(header.b.flags, 2**i)
            self.assertEqual(header.b.data, 2**i)

    def test__fn_get_addr__returns_add_tuple(self):
        s = self.default_server
        res = s.get_addr()
        self.assertEqual(HOST, res[0])
        self.assertEqual(PORT, res[1])

    # fn prepare ---------------------------------------------------------_

    def test__fn_prepare__instantiates_connections_list(self):
        s = self.default_server
        self.assertIsNone(s.connections)
        s.prepare()
        self.assertIsNotNone(s.connections)

    def test__fn_prepare__instantiates_socket(self):
        s = self.default_server
        s.prepare()
        self.assertIsNotNone(s.server_socket)

    # def test__fn_prepare__puts_socket_in_listen_mode(self):
    #     s = self.default_server
    #     s.prepare()
    #
    #   I think we can do this in C

    # 120221018 ELLIE:  This functionality has been removed.  Now, server_socket is just
    #                   its own variable, and we do a specific thing to ensure we
    #                   poll it correctly.  self.connections, is ONLY peer connections
    # def test__fn_prepare__appends_server_socket_to_connections_list(self):
    #     s = self.default_server
    #     s.prepare()
    #     self.assertTrue(s.server_socket in s.connections)

    def test__fn_prepare__instantiates_message_queue(self):
        s = self.default_server
        s.prepare()
        self.assertIsNotNone(s.message_queues)

    def test__fn_prepare__server_socket_exists_in_message_queue(self):
        s = self.default_server
        s.prepare()
        self.assertTrue(s.server_socket.getsockname() in s.message_queues)

    # fn start -----------------------------------------------------------_

    def test__fn_start__creates_a_listening_socket_with_correct_values(self):
        s = self.default_server
        s.prepare()

        self.assertIsNotNone(s.server_socket)
        self.assertEqual(socket.AF_INET6, s.server_socket.family)

    # fn handle_add_new_connection ---------------------------------------

    # def test__fn_handle_new_connection__adds_connection_to_message_queue(self):
    #     s = self.default_server
    #     s.prepare()
    #
    #     s.handle_add_new_connection(None)

    # fn handle_socket_read ----------------------------------------------
        #

    # fn handle_socket_data ----------------------------------------------
        # gets socket
        # reads data from socket
        # routes data to it's specific processing fn


    # fn handle_socket_write ---------------------------------------------
        # attempts to get message from queue
        # calls send() and sends message

    # fn handle_exception ------------------------------------------------
        # remove socket from connections
        # close socket
        # remove socket from message queue


if __name__ == '__main__':
    unittest.main()
