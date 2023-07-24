#ifndef SATELINK
#define SATELINK

#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"

const int OffStatus = 0;
const int ConnectingStatus = 2;
const int OnStatus = 1;

int ifacIndex(int src, int dst);

class SatLink
{
  private:
    // status: OnStatus, OffStatus, ConnectingStatus
    int status;
    float bandwidth;
    float latency;
    ns3::Ptr<ns3::PointToPointChannel> channel;

    ns3::Ptr<ns3::Node> nodeA;
    ns3::Ptr<ns3::Node> nodeB;
    ns3::NetDeviceContainer deviceAB;

    uint32_t ifceA;
    uint32_t ifceB;
    void TearDownLink();
    void RecoverLink();

  public:
    SatLink();
    SatLink(int s, float d, float l, ns3::Ptr<ns3::PointToPointChannel> c);
    void TearDown(ns3::Time t);
    void Recover(ns3::Time t);
    void Info();
    void SetSatLinkStackInfo(ns3::NetDeviceContainer devAB);
    bool UpdateLinkInfo(int s, float d, float l);
    int GetStatus();

    ns3::NetDeviceContainer GetNetDeviceContainer();
};

#endif // SATELINK