#include "DataRecver.h"

NS_LOG_COMPONENT_DEFINE("DataReceiver");

DataReceiver::DataReceiver(Ptr<Node> node, Ipv4Address address, uint16_t sinkPort)
{
    m_totBytes = 0;
    m_port = sinkPort;
    m_localAddress = InetSocketAddress(address, sinkPort);
    m_socket = Socket::CreateSocket(node, TcpSocketFactory::GetTypeId());

    // set the DataReceiver to receive packet
    node->AddApplication(this);
    // StartApplication();
}

DataReceiver::~DataReceiver()
{
    m_socket = 0;
}

// 会被node自动调用，用来开始操作
void DataReceiver::StartApplication(void)
{
    NS_LOG_DEBUG("[DataReceiver::StartApplication] at " << Simulator::Now().GetSeconds());
    m_socket->Bind(m_localAddress);
    m_socket->Listen();
    m_socket->SetAcceptCallback(MakeNullCallback<bool, Ptr<Socket>, const Address &>(),
                                MakeCallback(&DataReceiver::HandleAccept, this));
    // m_socket->SetRecvCallback(MakeCallback(&DataReceiver::ReceivePacket, this));
}

void DataReceiver::HandleAccept(Ptr<Socket> s, const Address &from)
{
    NS_LOG_DEBUG("[DataReceiver::HandleAccept] at " << Simulator::Now().GetSeconds());
    s->SetRecvCallback(MakeCallback(&DataReceiver::ReceivePacket, this));
}

// 会被node自动调用
void DataReceiver::StopApplication(void)
{
    if (m_socket)
    {
        m_socket->Close();
    }
}

void DataReceiver::ReceivePacket(Ptr<Socket> socket)
{
    NS_LOG_DEBUG("[DataReceiver::ReceivePacket] at " << Simulator::Now().GetSeconds());
    Ptr<Packet> packet;
    while ((packet = socket->Recv()))
    {
        TimestampTag timestamp;
        if (packet->FindFirstMatchingByteTag(timestamp))
        {
            Time tx = timestamp.GetTimestamp();
            // Calculate delay
            Time delay = Simulator::Now() - tx;
            NS_LOG_DEBUG("[DataReceiver::ReceivePacket]: Delay: " << delay.GetSeconds() << " seconds");

            // Get the size of the packet
            uint32_t pktSize = packet->GetSize();
            m_totBytes += pktSize;
            NS_LOG_DEBUG("[DataReceiver::ReceivePacket]: Packet size: " << pktSize << " bytes"
                                                                        << ", Total bytes: " << m_totBytes << " bytes");
            DataReceiverAppendToFile(Simulator::Now().GetSeconds(), delay.GetSeconds(), m_totBytes, m_totBytes,
                                     "0-recvPkt.log");
        }
        else
        {
            uint32_t pktSize = packet->GetSize();
            m_totBytes += pktSize;
            NS_LOG_DEBUG("[DataReceiver::ReceivePacket]: Packet size: " << pktSize << " bytes"
                                                                        << ", Total bytes: " << m_totBytes << " bytes");
        }
    }
}

uint16_t DataReceiver::GetBindPort(void) const
{
    return m_port;
}

Address DataReceiver::GetBindAddress(void) const
{
    return m_localAddress;
}