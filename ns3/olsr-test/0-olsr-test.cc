#include "SatGraph.h"
#include "SatLinks.h"
#include "ns3/aodv-module.h"
#include "ns3/applications-module.h"
#include "ns3/olsr-helper.h"
#include "utils.h"
#include <curl/curl.h>
#include <iostream>
#include <jsoncpp/json/json.h>
#include <string>
#include <vector>

NS_LOG_COMPONENT_DEFINE("OlsrStaGraph");

using namespace ns3;

const int NodeNum = 20;
const int SimluationTime = 50;
const int TimeInterval = 10;
const int StartTime = 3;
const int EndtTime = 45;

int main(int argc, char *argv[])
{
    CommandLine cmd(__FILE__);
    cmd.Parse(argc, argv);

    Time::SetResolution(Time::NS);
    // LogComponentEnable("OnOffApplication", LOG_LEVEL_INFO);
    LogComponentEnable("PacketSink", LOG_LEVEL_INFO);
    LogComponentEnable("OlsrStaGraph", LOG_LEVEL_ALL);
    LogComponentEnable("SatLink", LOG_LEVEL_ALL);
    LogComponentEnable("SatGraph", LOG_LEVEL_ALL);
    // LogComponentEnableAll(LOG_LEVEL_INFO);

    NodeContainer nodes;
    nodes.Create(NodeNum);

    // 为 onoff 单独创建一个节点用于发送数据
    NodeContainer nodeforOnOff;
    nodeforOnOff.Add(nodes.Get(0));
    nodeforOnOff.Create(1);

    // 为 packetsink 单独创建一个节点用于接收数据
    NodeContainer nodeforPacketSink;
    nodeforPacketSink.Add(nodes.Get(NodeNum - 1));
    nodeforPacketSink.Create(1);

    PointToPointHelper pointToPoint;
    pointToPoint.SetDeviceAttribute("DataRate", StringValue("1Mbps"));
    pointToPoint.SetChannelAttribute("Delay", StringValue("2ms"));

    // construct a satGraph to collect the nodeInfo
    SatGraph satGraph(NodeNum);
    // Establish P2P full connection
    for (int i = 0; i < NodeNum; i++)
    {
        for (int j = i + 1; j < NodeNum; j++)
        {
            NodeContainer nodestmp;
            ns3::Ptr<ns3::Node> node01 = nodes.Get(i);
            ns3::Ptr<ns3::Node> node02 = nodes.Get(j);
            nodestmp.Add(node01);
            nodestmp.Add(node02);
            NetDeviceContainer devices = pointToPoint.Install(nodestmp);
            satGraph.GetSatConn(i, j)->SetSatLinkStackInfo(devices);
        }
    }
    NetDeviceContainer devicesforOnOff = pointToPoint.Install(nodeforOnOff);
    NetDeviceContainer devicesforPacketSink = pointToPoint.Install(nodeforPacketSink);

    InternetStackHelper stack;
    AodvHelper olsr;
    stack.SetRoutingHelper(olsr);

    // 此处的nodes应该还要包括off和sink
    // nodes.Add(nodeforOnOff.Get(1));
    // nodes.Add(nodeforPacketSink.Get(1));

    stack.Install(nodes);
    stack.Install(nodeforOnOff.Get(1));
    stack.Install(nodeforPacketSink.Get(1));

    Ipv4AddressHelper address;

    // Assign IP address for each node
    // if node-indexA <----> node-indexB, then,
    // IP address of node-indexA is 10.indexA.indexB.1
    // IP addres of node-indexB is 10.indexA.indexB.2
    for (int i = 0; i < NodeNum; i++)
    {
        for (int j = i + 1; j < NodeNum; j++)
        {
            std::string subnetstr = "10." + std::to_string(i) + "." + std::to_string(j) + ".0";
            Ipv4Address subnet = Ipv4Address(subnetstr.c_str());
            address.SetBase(subnet, "255.255.255.0");
            address.Assign(satGraph.GetSatConn(i, j)->GetNetDeviceContainer());
        }
    }

    address.SetBase("10.111.222.0", "255.255.255.0");
    address.Assign(devicesforOnOff);
    address.SetBase("10.111.223.0", "255.255.255.0");
    address.Assign(devicesforPacketSink);

    satGraph.SatGraphInfo();

    // 取最后一个节点的最后一个interface
    Ptr<Ipv4> ipv4 = nodeforPacketSink.Get(1)->GetObject<Ipv4>();
    Ipv4Address targetIpAddress = ipv4->GetAddress(1, 0).GetLocal();

    int port = 9;
    // Configure PacketSink
    PacketSinkHelper sink("ns3::UdpSocketFactory", Address(InetSocketAddress(targetIpAddress, port)));
    ApplicationContainer apps_sink = sink.Install(nodeforPacketSink.Get(1));
    apps_sink.Start(Seconds(0.5));
    apps_sink.Stop(Seconds(SimluationTime + 0.5));

    // Configure onoff app
    OnOffHelper onoff("ns3::UdpSocketFactory", InetSocketAddress(targetIpAddress, port));
    onoff.SetConstantRate(DataRate("32kb/s"), 1024);
    onoff.SetAttribute("OnTime", StringValue("ns3::ConstantRandomVariable[Constant=1]"));
    onoff.SetAttribute("OffTime", StringValue("ns3::ConstantRandomVariable[Constant=0]"));
    onoff.SetAttribute("StartTime", TimeValue(Seconds(1.0)));
    onoff.SetAttribute("StopTime", TimeValue(Seconds(SimluationTime)));
    ApplicationContainer apps_source = onoff.Install(nodeforOnOff.Get(1));

    // 在这个函数这里修改网络的拓扑图
    changeSats(&satGraph, TimeInterval, StartTime, EndtTime);

    // printRoutingTable(Seconds(25.0), "scratch/2-olsrTest/0-olsr-test-0.routingtable", nodes);

    splitLog(SimluationTime);

    Simulator::Stop(Seconds(SimluationTime + 1.0));
    Simulator::Run();
    Simulator::Destroy();

    return 0;
}
