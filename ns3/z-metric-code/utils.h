#ifndef UTILS
#define UTILS

#include "SatGraph.h"
#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include <curl/curl.h>
#include <iostream>
#include <jsoncpp/json/json.h>
#include <string>

using namespace ns3;

size_t WriteCallback(void *contents, size_t size, size_t nmemb, std::string *s);
void printRoutingTable(ns3::Time printTime, const std::string &fileName, ns3::NodeContainer c);
void printIpv4Address(ns3::NodeContainer c, uint32_t index);
void singleSplitLog();
void splitLog();
void UpdateSats(SatGraph *satGraph, int certainTime);
void compareNode(ns3::Ptr<ns3::Node> nodeA);
void splitLog(int simluationTime);
void changeSats(SatGraph *satGraph, int timeInterval, int startTime, int endTime);
void PrintNodeDetails(Ptr<Node> node);
void SetLoopbackAddressAndRouting(Ptr<Node> node);
#endif // UTILS