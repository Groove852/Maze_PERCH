import socket
import subprocess
import random

class Server(object):
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _value = '0'
    _topic = '0'
    _cmd = '0'
    __port = random.randint(1000, 9999)

    def __init__(self, ip, listeners=5):
        self._socket.bind((ip, self.__port))
        print("IP: ", ip)
        print("PORT: ", self.__port)
        self._socket.listen(listeners)
        self.__client, self.__adr = self._socket.accept()

    def start(self):
        while 1:
            self._value = self.__client.recv(1024).decode()
            
            if self._value == '1':
                self.command()
                
            elif self._value == '2':
                self.getDiagnostic()

            elif self._value == '3':
                if self._topic == '0':
                    self._topic = str(input("Enter topic"))
                self.getTopics(self._topic)

        self.__client.close()

    """def getDiagnostic(self):
        return
    def getTopics(self, topic):
        try:
            self.__client.send(topic.encode())
            result_output = self.__client.recv(1024).decode()
            print(result_output)
        finally:
            pass"""

    def command(self):
        try:
            command = self.__client.recv(1024).decode()
            result_output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            self.__client.send(str(result_output.stdout.read()).encode())
        finally:
            pass
            
server = Server('10.10.50.52')
server.start()
