#ifndef SENDPKTAPP_H
#define SENDPKTAPP_H

#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include "ns3/packet.h"
#include "utils.h"

using namespace ns3;

class SendPktApp : public Application
{
  public:
    SendPktApp();
    virtual ~SendPktApp();
    // void Setup(Ptr<Socket> socket, Address address, uint32_t packetSize = 1024, uint32_t nPackets = 100,
    //            DataRate dataRate = DataRate("1Mbps"));
    void Setup(Ptr<Node> node, Address sinkAddress, uint32_t packetSize = 1024, uint32_t nPackets = 100,
               DataRate dataRate = DataRate("32kb/s"));

  private:
    virtual void StartApplication(void);
    virtual void StopApplication(void);
    void RestartApplication(void);
    void ScheduleTx(void);
    void SendPacket(void);
    void ConnectionSucceeded(Ptr<Socket> socket);
    void ConnectionFailed(Ptr<Socket> socket);

    Ptr<Socket> m_socket;
    Ptr<Node> m_node;
    Address m_peer;
    uint32_t m_packetSize;
    uint32_t m_nPackets;
    DataRate m_dataRate;
    EventId m_sendEvent;
    bool m_running;
    uint32_t m_packetsSent;
};

#endif