#include "DataRecver.h"
#include "SendPktApp.h"
#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include "ns3/packet.h"
#include "ns3/point-to-point-module.h"
#include "ns3/timestamp-tag.h"

using namespace ns3;

int main(int argc, char *argv[])
{
    LogComponentEnable("SendPktApp", LOG_LEVEL_DEBUG);
    LogComponentEnable("DataReceiver", LOG_LEVEL_DEBUG);
    NodeContainer nodes;
    nodes.Create(2);

    PointToPointHelper pointToPoint;
    pointToPoint.SetDeviceAttribute("DataRate", StringValue("5Mbps"));
    pointToPoint.SetChannelAttribute("Delay", StringValue("2ms"));

    NetDeviceContainer devices;
    devices = pointToPoint.Install(nodes);

    InternetStackHelper stack;
    stack.Install(nodes);

    Ipv4AddressHelper address;
    address.SetBase("10.1.1.0", "255.255.255.0");

    Ipv4InterfaceContainer interfaces = address.Assign(devices);

    // uint16_t sinkPort = 8080;
    // Address sinkAddress(InetSocketAddress(interfaces.GetAddress(1), sinkPort));
    // Ptr<Socket> recvSink = Socket::CreateSocket(nodes.Get(1), UdpSocketFactory::GetTypeId());
    // recvSink->Bind(sinkAddress);
    // recvSink->SetRecvCallback(MakeCallback(&ReceivePacket));

    // init DataRecver
    DataReceiver *dataRecver = new DataReceiver(nodes.Get(1), interfaces.GetAddress(1));
    Address sinkAddress = dataRecver->GetBindAddress();

    Ptr<Socket> source = Socket::CreateSocket(nodes.Get(0), UdpSocketFactory::GetTypeId());
    // uint32_t packetSize = 1024; // bytes
    // uint32_t maxPacketCount = 50;
    SendPktApp *app = new SendPktApp();
    app->Setup(source, sinkAddress);
    nodes.Get(0)->AddApplication(app);
    app->SetStartTime(Seconds(1.));
    app->SetStopTime(Seconds(10.));

    Simulator::Run();
    Simulator::Destroy();

    return 0;
}
