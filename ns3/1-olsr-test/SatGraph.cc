#include "SatGraph.h"

NS_LOG_COMPONENT_DEFINE("SatGraph");

SatGraph::SatGraph(int s)
{
    size = s;
    // 声明一个二维矩阵
    ptr = new SatLink *[s];
    for (int i = 0; i < s; i++)
    {
        ptr[i] = new SatLink[size];
    }
}

SatGraph::~SatGraph()
{
    for (int i = 0; i < size; i++)
    {
        delete[] ptr[i];
    }
    delete[] ptr;
}

SatLink *SatGraph::GetSatConn(int src, int dst)
{
    if (dst <= src)
    {
        NS_LOG_ERROR("[SatGraph]: GetSatConn(): dst should be larger than src, "
                     << "dst: " << dst << ", src: " << src);
        return nullptr;
    }
    return &ptr[src][dst];
}

void SatGraph::SatGraphInfo(void)
{
    for (int i = 0; i < size; i++)
    {
        for (int j = i + 1; j < size; j++)
        {
            GetSatConn(i, j)->Info();
        }
    }
}

void SatGraph::RecoverLink(int a, int b, ns3::Time t)
{
    int max_index = a > b ? a : b;
    int min_index = a > b ? b : a;
    NS_LOG_DEBUG("[SatGraph]: RecoverLink(): Try to recover link: " << min_index << " " << max_index << " " << t);
    GetSatConn(min_index, max_index)->Recover(t);
}

void SatGraph::TearDownLink(int a, int b, ns3::Time t)
{
    int max_index = a > b ? a : b;
    int min_index = a > b ? b : a;
    NS_LOG_DEBUG("[SatGraph]: TearDownLink(): Try to tear down link: " << min_index << " " << max_index << " " << t);
    GetSatConn(min_index, max_index)->TearDown(t);
}

int SatGraph::GetSize()
{
    return size;
}