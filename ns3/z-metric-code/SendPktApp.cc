#include "SendPktApp.h"

NS_LOG_COMPONENT_DEFINE("SendPktApp");

SendPktApp::SendPktApp()
    : m_socket(0), m_peer(), m_packetSize(0), m_nPackets(0), m_dataRate(0), m_sendEvent(), m_running(false),
      m_packetsSent(0)
{
}

SendPktApp::~SendPktApp()
{
    m_socket = 0;
}

void SendPktApp::Setup(Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate)
{

    m_socket = socket;
    m_peer = address;
    m_packetSize = packetSize;
    m_nPackets = nPackets;
    m_dataRate = dataRate;
    socket->GetNode()->AddApplication(this);
}

void SendPktApp::Setup(Ptr<Node> node, Address sinkAddress, uint32_t packetSize, uint32_t nPackets, DataRate dataRate)
{
    m_socket = Socket::CreateSocket(node, TcpSocketFactory::GetTypeId());
    m_peer = sinkAddress;
    m_packetSize = packetSize;
    m_nPackets = nPackets;
    m_dataRate = dataRate;
    node->AddApplication(this);
}

void SendPktApp::StartApplication(void)
{
    NS_LOG_DEBUG("[SendPktApp::StartApplication] at " << Simulator::Now().GetSeconds());
    m_running = true;
    m_packetsSent = 0;
    m_socket->Bind();
    m_socket->Connect(m_peer);
    SendPacket();

    // Add connection successful callback
    m_socket->SetConnectCallback(MakeCallback(&SendPktApp::ConnectionSucceeded, this),
                                 MakeCallback(&SendPktApp::ConnectionFailed, this));
}

void SendPktApp::StopApplication(void)
{
    m_running = false;
    if (m_sendEvent.IsRunning())
    {
        Simulator::Cancel(m_sendEvent);
    }

    if (m_socket)
    {
        m_socket->Close();
    }
}

void SendPktApp::SendPacket(void)
{
    NS_LOG_DEBUG("[SendPktApp::SendPacket] at " << Simulator::Now().GetSeconds());
    Ptr<Packet> packet = Create<Packet>(m_packetSize);
    TimestampTag timestamp;
    timestamp.SetTimestamp(Simulator::Now());
    packet->AddByteTag(timestamp);
    m_socket->Send(packet);

    if (++m_packetsSent < m_nPackets)
    {
        ScheduleTx();
    }
}

void SendPktApp::ScheduleTx(void)
{
    if (m_running)
    {
        Time tNext(Seconds(m_packetSize * 8 / static_cast<double>(m_dataRate.GetBitRate())));
        m_sendEvent = Simulator::Schedule(tNext, &SendPktApp::SendPacket, this);
    }
}

// Add connection successful callback function
void SendPktApp::ConnectionSucceeded(Ptr<Socket> socket)
{
    NS_LOG_DEBUG("[SendPktApp::ConnectionSucceeded] at " << Simulator::Now().GetSeconds());
    SendPacket();
}

// Add connection failed callback function
void SendPktApp::ConnectionFailed(Ptr<Socket> socket)
{
    NS_LOG_DEBUG("[SendPktApp::Failer] at " << Simulator::Now().GetSeconds());
}