#include "utils.h"

size_t WriteCallback(void *contents, size_t size, size_t nmemb, std::string *s)
{
    size_t newLength = size * nmemb;
    size_t oldLength = s->size();
    try
    {
        s->resize(oldLength + newLength);
    }
    catch (std::bad_alloc &e)
    {
        return 0;
    }
    std::copy((char *)contents, (char *)contents + newLength, s->begin() + oldLength);
    return size * nmemb;
};

// 用这个来更新 satGraph
void UpdateSats(SatGraph *satGraph, int certainTime)
{
    CURL *curl;
    CURLcode res;
    std::string readBuffer;
    curl = curl_easy_init();
    if (curl)
    {
        curl_easy_setopt(curl, CURLOPT_URL, "http://127.0.0.1:8000/communication");
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // modify the args
        int size = satGraph->GetSize();

        std::stringstream ss;
        ss << "{ \"size\": " << size << ", \"time\": " << certainTime << " }";
        std::string json = ss.str();

        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json.c_str());
        res = curl_easy_perform(curl);

        if (res != CURLE_OK)
        {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        }
        else
        {
            JSONCPP_STRING err;
            Json::Value jsonData;
            Json::CharReaderBuilder jsonReader;
            const std::unique_ptr<Json::CharReader> reader(jsonReader.newCharReader());
            bool parsingSuccessful =
                reader->parse(readBuffer.c_str(), readBuffer.c_str() + readBuffer.length(), &jsonData, &err);
            if (parsingSuccessful)
            {
                for (int i = 0; i < size; ++i)
                {
                    for (int j = i + 1; j < size; ++j)
                    {

                        bool flag = jsonData[i][j][0].asBool();
                        float dis = jsonData[i][j][1].asFloat();
                        float latency = jsonData[i][j][2].asFloat();
                        bool res = satGraph->GetSatConn(i, j)->UpdaetLinkInfo(flag, dis, latency);
                        if (res)
                        {
                            if (flag)
                            {
                                satGraph->RecoverLink(i, j, MilliSeconds(1));
                            }
                            else
                            {
                                satGraph->TearDownLink(i, j, MilliSeconds(1));
                            }
                        }
                    }
                }
                satGraph->SatGraphInfo();
            }
            curl_easy_cleanup(curl);
        }
        return;
    }
}

void compareNode(ns3::Ptr<ns3::Node> nodeA)
{
    ns3::Ptr<ns3::Ipv4> ipv4 = nodeA->GetObject<ns3::Ipv4>();
    uint32_t index = 0; // 在ns-3中，索引0通常用于回环地址，因此我们从1开始
    while (index < ipv4->GetNInterfaces())
    {
        std::cout << "[compareNode]: Time: " << ns3::Simulator::Now().GetSeconds() << ", Node-" << nodeA->GetId()
                  << ", Interface-" << index << " is up: " << ipv4->IsUp(index)
                  << ", IP address: " << ipv4->GetAddress(index, 0).GetLocal();
        index++;
    }
}

void printRoutingTable(Time printTime, const std::string &fileName, ns3::NodeContainer c)
{
    Ipv4GlobalRoutingHelper g;
    Ptr<OutputStreamWrapper> routingStream = Create<OutputStreamWrapper>(fileName, std::ios::out);
    for (uint32_t i = 0; i < c.GetN(); ++i)
    {
        g.PrintRoutingTableAt(printTime, c.Get(i), routingStream);
    }
    std::cout << "[printRoutingTable]: Print Routing Table at: " << printTime.GetInteger() << std::endl;
}

void printIpv4Address(NodeContainer c, uint32_t index)
{
    if (index >= c.GetN())
    {
        std::cout << "[printIpv4Address]: Bad index." << index << " is greater than nodes' number" << std::endl;
        return;
    }

    Ptr<Ipv4> ipv4 = c.Get(index)->GetObject<Ipv4>();
    std::cout << "[printIpv4Address]: Node-" << index << ": Interfaces number: " << ipv4->GetNInterfaces() << std::endl;

    for (uint32_t i = 0; i < ipv4->GetNInterfaces(); i++)
    {
        Ipv4Address ipAddress = ipv4->GetAddress(i, 0).GetLocal();
        std::cout << "[printIpv4Address]: Node " << c.Get(index)->GetId() << ", Interface " << i
                  << ", IP address: " << ipAddress << std::endl;
    }
    return;
}

void singleSplitLog()
{
    std::cout << "Time: " << ns3::Simulator::Now().GetSeconds()
              << "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " << std::endl;
    return;
}

void splitLog(int simluationTime)
{
    for (float time = 1.; time < simluationTime; time = time + 1)
    {
        Simulator::Schedule(Seconds(time), &singleSplitLog);
    }
}

// 这个函数用来改变的星座的拓扑图
void changeSats(SatGraph *satGraph, int timeInterval, int startTime, int endTime)
{
    for (int i = startTime; i < endTime; i = i + timeInterval)
    {
        std::cout << "[changeSats]: Time: " << i << std::endl;
        Simulator::Schedule(Seconds(i), &UpdateSats, satGraph, i);
    }

    // for single test
    satGraph->TearDownLink(0, 2, Seconds(15.0));
}
