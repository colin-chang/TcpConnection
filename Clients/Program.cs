using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace TcpClient
{
    class Program
    {
        static void Main(string[] args)
        {
            var connA = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            connA.Connect(new IPEndPoint(IPAddress.Parse("127.0.0.1"), 8088));

            var connB = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            connB.Connect(new IPEndPoint(IPAddress.Parse("127.0.0.1"), 8088));

            TestServer(connA, "A123");
            Thread.Sleep(1000);
            TestServer(connA, "A456");
            TestServer(connB, "B456");
            Thread.Sleep(1000);
            TestServer(connA, "A789");
            Console.ReadKey();
        }

        private static void TestServer(Socket conn, string msg)
        {
            new Thread(() =>
            {
                conn.Send(Encoding.UTF8.GetBytes(msg));
                Console.WriteLine($"[send] : {DateTime.Now.ToString("HH:mm:ss")} - {msg}");
                var byteData = new byte[1024];
                var length = conn.Receive(byteData);
                if (length > 0)
                    Console.WriteLine($"[recv] : {DateTime.Now.ToString("HH:mm:ss")} - {Encoding.UTF8.GetString(byteData)}");
            }).Start();
        }
    }
}
