using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace TcpClient
{
    class Program
    {
        private static Socket _conn;

        static void Main(string[] args)
        {
            _conn = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            _conn.Connect(new IPEndPoint(IPAddress.Parse("127.0.0.1"), 8088));

            FlirtServer("123");
            Thread.Sleep(1000);
            FlirtServer("456");
            Thread.Sleep(1000);
            FlirtServer("789");
            Console.ReadKey();
        }

        private static void FlirtServer(string msg)
        {
            new Thread(() =>
            {
                _conn.Send(Encoding.UTF8.GetBytes(msg));
                var byteData = new byte[1024];
                var length = _conn.Receive(byteData);
                if (length > 0)
                    Console.WriteLine($"{DateTime.Now} {Encoding.UTF8.GetString(byteData)}");
            }).Start();
        }
    }
}