#ifndef SATGRAPH
#define SATGRAPH

#include "SatLinks.h"

class SatGraph
{
  private:
    int size;
    SatLink **ptr;

  public:
    SatGraph(int s);
    ~SatGraph();
    SatLink *GetSatConn(int src, int dst);
    void SatGraphInfo(void);
};

#endif // SATGRAPH