#include "SatLinks.h"
#include "utils.h"

NS_LOG_COMPONENT_DEFINE("SatLink");
SatLink::SatLink(int s, float d, float l, ns3::Ptr<ns3::Channel> c)
{
    status = s;
    bandwidth = d;
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
    status = OnStatus;
    // NS_LOG_INFO("Hello my bro");
}

void SatLink::TearDown(ns3::Time downTime)
{
    NS_LOG_DEBUG("[SatLink]: TearDown(): Try to tear down: node-" << nodeA->GetId() << " and node-" << nodeB->GetId()
                                                                  << " at " << downTime.GetSeconds());
    ns3::Simulator::Schedule(downTime, ns3::MakeEvent(&SatLink::TearDownLink, this));
}

void SatLink::Recover(ns3::Time upTime)
{
    NS_LOG_DEBUG("[SatLink]: Recover(): " << ns3::Simulator::Now().GetMilliSeconds() << ", Try to recover: node-"
                                          << nodeA->GetId() << " and node-" << nodeB->GetId() << " at "
                                          << upTime.GetMilliSeconds());
    ns3::Simulator::Schedule(upTime, ns3::MakeEvent(&SatLink::RecoverLink, this));
}

void SatLink::Info()
{
    if (status == OffStatus)
    {
        NS_LOG_INFO("[SatLink]: Info(): node-" << nodeA->GetId() << " and node-" << nodeB->GetId()
                                               << " are not connected");
    }
    else if (status == OnStatus)
    {
        ns3::Ptr<ns3::Ipv4> ipa = nodeA->GetObject<ns3::Ipv4>();
        ns3::Ptr<ns3::Ipv4> ipb = nodeB->GetObject<ns3::Ipv4>();
        NS_LOG_INFO("[SatLink]: Info(): node-" << nodeA->GetId() << " and node-" << nodeB->GetId()
                                               << " are connect at: " << ipa->GetAddress(1, 0).GetLocal() << " and "
                                               << ipb->GetAddress(1, 0).GetLocal() << " bandwidth: " << bandwidth
                                               << " latency: " << latency << " status: " << status);
    }
}

void SatLink::SetSatLinkStackInfo(ns3::NetDeviceContainer devAB)
{
    ns3::Ptr<ns3::NetDevice> deviceA = devAB.Get(0);
    ns3::Ptr<ns3::NetDevice> deviceB = devAB.Get(1);
    deviceAB = devAB;

    // we confirm the nodeA is the smaller one
    if (deviceA->GetNode()->GetId() <= deviceB->GetNode()->GetId())
    {
        nodeA = deviceA->GetNode();
        nodeB = deviceB->GetNode();
        ifceA = ifacIndex(nodeA->GetId(), nodeB->GetId());
        ifceB = ifacIndex(nodeB->GetId(), nodeA->GetId());
    }
    else
    {
        nodeB = deviceA->GetNode();
        nodeA = deviceB->GetNode();
        ifceB = ifacIndex(nodeA->GetId(), nodeB->GetId());
        ifceA = ifacIndex(nodeB->GetId(), nodeA->GetId());
    }

    channel = deviceAB.Get(0)->GetChannel();
    NS_LOG_DEBUG("[SatLink]: node-" << nodeA->GetId() << " at: " << ifceA << " and node-" << nodeB->GetId()
                                    << " at: " << ifceB << " are connected at:" << channel->GetId());
}

ns3::NetDeviceContainer SatLink::GetNetDeviceContainer()
{
    return deviceAB;
}

void SatLink::TearDownLink()
{
    // 打印此时的状态
    // PrintNodeDetails(nodeA);

    NS_LOG_INFO("[SatLink]: TearDownLink(): " << ns3::Simulator::Now().GetSeconds() << " tear down: node-"
                                              << nodeA->GetId() << " at " << ifceA << " and node-" << nodeB->GetId()
                                              << " at " << ifceB);
    status = OffStatus;
    nodeA->GetObject<ns3::Ipv4>()->SetDown(ifceA);
    nodeB->GetObject<ns3::Ipv4>()->SetDown(ifceB);
}

void SatLink::RecoverLink()
{
    NS_LOG_INFO("[SatLink]: RecoverLink():" << ns3::Simulator::Now().GetSeconds() << " recover: node-" << nodeA->GetId()
                                            << " at " << ifceA << " and node-" << nodeB->GetId() << " at " << ifceB);

    bool isAUP = nodeA->GetObject<ns3::Ipv4>()->IsUp(ifceA);
    bool isBUP = nodeB->GetObject<ns3::Ipv4>()->IsUp(ifceB);

    if (!isAUP)
    {
        nodeA->GetObject<ns3::Ipv4>()->SetUp(ifceA);
    }
    else
    {
        NS_LOG_DEBUG("[SatLink]: RecoverLink(): node-" << nodeA->GetId() << " at " << ifceA << " is already up");
    }
    if (!isBUP)
    {
        nodeB->GetObject<ns3::Ipv4>()->SetUp(ifceB);
    }
    else
    {
        NS_LOG_DEBUG("[SatLink]: RecoverLink(): node-" << nodeB->GetId() << " at " << ifceB << " is already up");
    }
    status = OnStatus;
}

bool SatLink::UpdateLinkInfo(int s, float d, float l)
{
    bool flag = false;
    if (status == OnStatus && s == OffStatus)
    {
        // if status is from OnSatus -> OffStatus, we need to tear down the link
        NS_LOG_DEBUG("[SatLink]: UpdaetLinkInfo(): Time: " << ns3::Simulator::Now().GetSeconds() << " node-"
                                                           << nodeA->GetId() << " and node-" << nodeB->GetId()
                                                           << " is down at " << ns3::Simulator::Now().GetSeconds());
        // TearDown(ns3::Simulator::Now());
        flag = true;
    }
    else if (status == OffStatus && s == OnStatus)
    {
        // if status is from OffStatus -> OnStatus, we need to recover the link
        NS_LOG_DEBUG("[SatLink]: UpdaetLinkInfo(): Time: " << ns3::Simulator::Now().GetSeconds() << " node-"
                                                           << nodeA->GetId() << " and node-" << nodeB->GetId()
                                                           << " is up at " << ns3::Simulator::Now().GetSeconds());
        // Recover(ns3::Simulator::Now());
        flag = true;
    }
    else
    {
        NS_LOG_DEBUG("[SatLink]: UpdaetLinkInfo(): Time: " << ns3::Simulator::Now().GetSeconds() << " node-"
                                                           << nodeA->GetId() << " and node-" << nodeB->GetId()
                                                           << " status is not changed " << status);
    }
    status = s;
    bandwidth = d;
    latency = l;

    // if status == OnStatus, we need to update the bandwidth and latency
    if (status == OnStatus)
    {
        ns3::Simulator::Schedule(ns3::MilliSeconds(1), ns3::MakeEvent(&SatLink::SetNewDelay, this));
    }

    return flag;
}

int SatLink::GetStatus()
{
    return status;
}

void SatLink::SetNewDelay()
{
    NS_LOG_DEBUG("[SatLink]: SetNewDelay(): Time: " << ns3::Simulator::Now().GetSeconds() << " node-" << nodeA->GetId()
                                                    << " and node-" << nodeB->GetId() << " set new delay: " << latency
                                                    << " and set new bandwidth: " << int(bandwidth));
    channel->SetAttribute("Delay", ns3::TimeValue(ns3::MilliSeconds(int(latency))));
    // channel->SetAttribute("DataRate", ns3::DataRateValue(ns3::DataRate(int(bandwidth))));
}

int ifacIndex(int src, int dst)
{
    if (src == dst)
    {
        NS_LOG_ERROR("src and dst cannot be the same");
    }
    return dst < src ? dst + 1 : dst;
}
