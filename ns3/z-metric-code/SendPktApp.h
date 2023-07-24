#ifndef SENDPKTAPP_H
#define SENDPKTAPP_H

#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include "ns3/packet.h"

using namespace ns3;

class SendPktApp : public Application
{
  public:
    SendPktApp();
    virtual ~SendPktApp();
    void Setup(Ptr<Socket> socket, Address address, uint32_t packetSize = 1024, uint32_t nPackets = 100,
               DataRate dataRate = DataRate("1Mbps"));
    void Setup(Ptr<Node> node, Address sinkAddress, uint32_t packetSize = 1024, uint32_t nPackets = 100,
               DataRate dataRate = DataRate("1Mbps"));

  private:
    virtual void StartApplication(void);
    virtual void StopApplication(void);
    void ScheduleTx(void);
    void SendPacket(void);

    Ptr<Socket> m_socket;
    Address m_peer;
    uint32_t m_packetSize;
    uint32_t m_nPackets;
    DataRate m_dataRate;
    EventId m_sendEvent;
    bool m_running;
    uint32_t m_packetsSent;
};

#endif