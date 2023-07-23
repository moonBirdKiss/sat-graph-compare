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
        NS_LOG_ERROR("dst should be larger than src");
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