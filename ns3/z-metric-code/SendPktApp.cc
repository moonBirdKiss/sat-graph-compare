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

// void SendPktApp::Setup(Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate
// dataRate)
// {

//     m_socket = socket;
//     m_peer = address;
//     m_packetSize = packetSize;
//     m_nPackets = nPackets;
//     m_dataRate = dataRate;
//     socket->GetNode()->AddApplication(this);
// }

void SendPktApp::Setup(Ptr<Node> node, Address sinkAddress, uint32_t packetSize, uint32_t nPackets, DataRate dataRate)
{
    m_node = node;
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
    // SendPacket();

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
    AppendToFile(Simulator::Now().GetSeconds(), m_packetsSent, m_packetSize, "0-sendPkt.log");
    Ptr<Packet> packet = Create<Packet>(m_packetSize);
    TimestampTag timestamp;
    timestamp.SetTimestamp(Simulator::Now());
    packet->AddByteTag(timestamp);
    int ret = m_socket->Send(packet);
    NS_LOG_DEBUG("[SendPktApp::SendPacket] at " << Simulator::Now().GetSeconds() << ", and have sent "
                                                << m_packetsSent * m_packetSize << " bytes"
                                                << ", ret: " << ret);

    if (ret == -1)
    {
        errno = m_socket->GetErrno();
        m_socket->Close();
        NS_LOG_DEBUG("[SendPktApp::SendPacket]: Failed to send data, error code: " << errno);

        // 重新连接
        m_socket = Socket::CreateSocket(m_node, TcpSocketFactory::GetTypeId());
        m_socket->Connect(m_peer);
        m_socket->Bind();
        m_socket->SetConnectCallback(MakeCallback(&SendPktApp::ConnectionSucceeded, this),
                                     MakeCallback(&SendPktApp::ConnectionFailed, this));
        // Simulator::Schedule(Seconds(1), &SendPktApp::SendPacket, this);
    }
    else
    {
        m_packetsSent++;
        ScheduleTx();
    }

    // 注释掉著，让其一直发送

    // if (m_packetsSent < m_nPackets)
    // {
    //     ScheduleTx();
    // }
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