#ifndef DATARECV
#define DATARECV

#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include "ns3/packet.h"

using namespace ns3;

class DataReceiver : public Application
{
  public:
    DataReceiver(Ptr<Node> node, Ipv4Address address, uint16_t sinkPort = 8080);
    virtual ~DataReceiver();
    uint16_t GetBindPort(void) const;
    Address GetBindAddress(void) const;

  private:
    virtual void StartApplication(void);
    virtual void StopApplication(void);
    void ReceivePacket(Ptr<Socket> socket);

    Ptr<Socket> m_socket;
    uint16_t m_port;
    Address m_localAddress;
};

#endif