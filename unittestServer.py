import socket
import unittest
class Tests(unittest.TestCase):
        """
        Written by: Ching Loo(s3557584)
        
        Unit test for Server
        """
        
        def test_1(self):
                """
                Unlock vehicle
                """
                host = '123.208.55.187'
                port = 10400
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                s.send(str.encode("A,Ching,Testing@123"))
                self.assertEqual(s.recv(1024).decode(), 'Vehicle Unlocked!!')
                s.close()
        
        def test_2(self):
                """
                Return vehicle
                """
                host = '123.208.55.187'
                port = 10400
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                s.send(str.encode("C,1,Ching,Testing@123"))
                self.assertEqual(s.recv(1024).decode(), 'Vehicle is already returned!!')
                s.close()
        
        def test_3(self):
                """
                Return Vehicle with incorrect password
                """
                host = '123.208.55.187'
                port = 10400
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                s.send(str.encode("C,1,Ching,incorrect"))
                self.assertEqual(s.recv(1024).decode(), 'Incorrect Username or Password')
                s.close()
            
        def test_4(self):
                """
                Return Vehicle with incorrect vehicle id
                """
                host = '123.208.55.187'
                port = 10400
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                s.send(str.encode("C,0,Ching,Testing@123"))
                self.assertEqual(s.recv(1024).decode(), 'Incorrect vehicle ID')
                s.close()
        
if __name__ == '__main__':
    unittest.main()
