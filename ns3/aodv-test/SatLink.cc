#include "SatLinks.h"

NS_LOG_COMPONENT_DEFINE("SatLink");
SatLink::SatLink(int s, float d, float l, ns3::Ptr<ns3::PointToPointChannel> c)
{
    status = s;
    distance = d;
    latency = l;
    channel = c;

    // 然后给其他信息赋值
    ns3::Ptr<ns3::NetDevice> deviceA = channel->GetDevice(0);
    ns3::Ptr<ns3::NetDevice> deviceB = channel->GetDevice(1);

    nodeA = deviceA->GetNode();
    nodeB = deviceB->GetNode();
}

SatLink::SatLink()
{
    // NS_LOG_INFO("Hello my bro");
}

void SatLink::TearDown(ns3::Time downTime)
{
    NS_LOG_DEBUG("Try to tear down: " << downTime);
}

void SatLink::SetUp(ns3::Time upTime)
{
    NS_LOG_DEBUG("Try to set up: " << upTime);
}

void SatLink::Info()
{
    ns3::Ptr<ns3::Ipv4> ipa = nodeA->GetObject<ns3::Ipv4>();
    ns3::Ptr<ns3::Ipv4> ipb = nodeB->GetObject<ns3::Ipv4>();
    NS_LOG_INFO("node-" << nodeA->GetId() << " and node-" << nodeB->GetId() << " are connect at: "
                        << ipa->GetAddress(1, 0).GetLocal() << " and " << ipb->GetAddress(1, 0).GetLocal()
                        << " distance: " << distance << " latency: " << latency << " status: " << status);
}

void SatLink::SetSatLinkStackInfo(ns3::NetDeviceContainer devAB)
{
    ns3::Ptr<ns3::NetDevice> deviceA = devAB.Get(0);
    ns3::Ptr<ns3::NetDevice> deviceB = devAB.Get(1);
    deviceAB = devAB;
    nodeA = deviceA->GetNode();
    nodeB = deviceB->GetNode();

    channel = deviceA->GetObject<ns3::PointToPointChannel>();
    NS_LOG_DEBUG("node-" << nodeA->GetId() << " and node-" << nodeB->GetId() << " are connected");
}

ns3::NetDeviceContainer SatLink::GetNetDeviceContainer()
{
    return deviceAB;
}