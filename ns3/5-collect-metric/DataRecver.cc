#include "DataRecver.h"

NS_LOG_COMPONENT_DEFINE("DataReceiver");

DataReceiver::DataReceiver(Ptr<Node> node, Ipv4Address address, uint16_t sinkPort)
{
    m_port = sinkPort;
    m_localAddress = InetSocketAddress(address, sinkPort);
    m_socket = Socket::CreateSocket(node, UdpSocketFactory::GetTypeId());

    // set the DataReceiver to receive packet
    StartApplication();
}

DataReceiver::~DataReceiver()
{
    m_socket = 0;
}

void DataReceiver::StartApplication(void)
{
    m_socket->Bind(m_localAddress);
    m_socket->SetRecvCallback(MakeCallback(&DataReceiver::ReceivePacket, this));
}

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
        }
        // Get the size of the packet
        uint32_t pktSize = packet->GetSize();
        NS_LOG_DEBUG("[DataReceiver::ReceivePacket]: Packet size: " << pktSize << " bytes");
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