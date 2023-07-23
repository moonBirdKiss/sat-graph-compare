#ifndef SATELINK
#define SATELINK

#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"

const int OffStatus = 0;
const int ConnectingStatus = 1;
const int OnStatus = 2;

class SatLink
{
  private:
    // status: OnStatus, OffStatus, ConnectingStatus
    int status;
    float distance;
    float latency;
    ns3::Ptr<ns3::PointToPointChannel> channel;

    ns3::Ptr<ns3::Node> nodeA;
    ns3::Ptr<ns3::Node> nodeB;
    ns3::NetDeviceContainer deviceAB;

  public:
    SatLink();
    SatLink(int s, float d, float l, ns3::Ptr<ns3::PointToPointChannel> c);
    void TearDown(ns3::Time t);
    void SetUp(ns3::Time t);
    void Info();
    void SetSatLinkStackInfo(ns3::NetDeviceContainer devAB);
    ns3::NetDeviceContainer GetNetDeviceContainer();
};

#endif // SATELINK