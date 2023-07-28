#include "DataRecver.h"
#include "SatGraph.h"
#include "SatLinks.h"
#include "SendPktApp.h"
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

const int NodeNum = 8;
// const int SimluationTime = 60 * 60 * 2;

const int QueryTime = 300;
const int TimeInterval = 10;
// 480初始是连接的
// 620 0->1->7会变成 0->7的路线
const int StartTime = 1208;
const int SimluationTime = StartTime + QueryTime + 2;
const int EndtTime = StartTime + QueryTime;
const int SndAppTime = StartTime - 2;
const int RecAppTime = SndAppTime - 10;

int main(int argc, char *argv[])
{

    freopen("./scratch/8-let-any/z-myfile.log", "w", stderr);
    CommandLine cmd(__FILE__);
    cmd.Parse(argc, argv);

    Time::SetResolution(Time::NS);
    // LogComponentEnable("OnOffApplication", LOG_LEVEL_INFO);
    LogComponentEnable("PacketSink", LOG_LEVEL_INFO);
    LogComponentEnable("OlsrStaGraph", LOG_LEVEL_ALL);
    LogComponentEnable("SatLink", LOG_LEVEL_INFO);
    LogComponentEnable("SatGraph", LOG_LEVEL_INFO);
    LogComponentEnable("DataReceiver", LOG_LEVEL_DEBUG);
    LogComponentEnable("SendPktApp", LOG_LEVEL_DEBUG);
    // LogComponentEnable("AodvRoutingProtocol", LOG_LEVEL_FUNCTION);
    LogComponentEnable("Utils", LOG_LEVEL_ALL);
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
    pointToPoint.SetDeviceAttribute("DataRate", StringValue("10Mbps"));
    pointToPoint.SetChannelAttribute("Delay", StringValue("20ms"));

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

    // stack.SetRoutingHelper(olsr);
    // 此处的nodes应该还要包括off和sink
    nodes.Add(nodeforOnOff.Get(1));
    nodes.Add(nodeforPacketSink.Get(1));

    stack.Install(nodes);
    // stack.Install(nodeforOnOff.Get(1));
    // stack.Install(nodeforPacketSink.Get(1));

    // // 为两个应用添加默认网关
    // Ptr<Ipv4StaticRouting> staticRoutingOnOff =
    //     Ipv4RoutingHelper::GetRouting<Ipv4StaticRouting>(nodeforOnOff.Get(1)->GetObject<Ipv4>()->GetRoutingProtocol());
    // Ptr<Ipv4StaticRouting> staticRoutingPacketSink = Ipv4RoutingHelper::GetRouting<Ipv4StaticRouting>(
    //     nodeforPacketSink.Get(1)->GetObject<Ipv4>()->GetRoutingProtocol());

    // staticRoutingOnOff->SetDefaultRoute("10.111.222.1", 1);
    // staticRoutingPacketSink->SetDefaultRoute("10.111.223.1", 1);

    // stack.Install();

    // InternetStackHelper testStack;
    // testStack.Install(nodes.Get(0));
    // testStack.Install(nodes.Get(NodeNum - 1));
    // testStack.Install(nodeforOnOff.Get(1));
    // testStack.Install(nodeforPacketSink.Get(1));

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
    Ipv4InterfaceContainer packSinkIfac = address.Assign(devicesforPacketSink);

    int port = 9;
    // Configure PacketSink
    DataReceiver *dataRecver = new DataReceiver(nodeforPacketSink.Get(1), packSinkIfac.GetAddress(1), port);
    Address targetAddress = dataRecver->GetBindAddress();
    dataRecver->SetStartTime(Seconds(RecAppTime));
    dataRecver->SetStopTime(Seconds(SimluationTime - 1));

    // Configure onoff app
    SendPktApp *sendApp = new SendPktApp();
    sendApp->Setup(nodeforOnOff.Get(1), targetAddress, 1024, 57600000, DataRate("1Mbps"));
    // sendApp->Setup(nodeforOnOff.Get(1), targetAddress, 1024, 57600000, DataRate("32kbps"));
    sendApp->SetStartTime(Seconds(SndAppTime));
    sendApp->SetStopTime(Seconds(SimluationTime - 1));

    // 在这个函数这里修改网络的拓扑图
    changeSats(&satGraph, TimeInterval, StartTime, EndtTime);
    // changeSatsForTest(&satGraph, TimeInterval, StartTime, EndtTime);

    // printRoutingTable(Seconds(610), "./test-aodv-610.log", nodes);
    // printRoutingTable(Seconds(605), "./test-aodv-605.log", nodes);
    // printRoutingTable(Seconds(615), "./test-aodv-615.log", nodes);
    // printRoutingTable(Seconds(625), "./test-aodv-625.log", nodes);
    // printRoutingTable(Seconds(635), "./test-aodv-635.log", nodes);
    // printRoutingTable(Seconds(645), "./test-aodv-645.log", nodes);
    // printRoutingTable(Seconds(655), "./test-aodv-655.log", nodes);

    splitLog(SimluationTime);

    Simulator::Stop(Seconds(SimluationTime + 1.0));
    Simulator::Run();
    Simulator::Destroy();

    return 0;
}
