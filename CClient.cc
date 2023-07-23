#include <curl/curl.h>
#include <iostream>
#include <jsoncpp/json/json.h>
#include <string>

class SatCon
{
  private:
    bool flag;
    float distance;
    float latency;
    int src;
    int dst;

  public:
    void setSatConn(int initsrc, int initdst, bool f, float d, float l)
    {
        src = initsrc;
        dst = initdst;
        flag = f;
        distance = d;
        latency = l;
    }
    void infoSatConn(void)
    {
        std::cout << "from Node-" << src << " to Node-" << dst << ", flag: " << flag << ", distance: " << distance
                  << ", latency: " << latency << std::endl;
    }
};

class SatGraph
{
  private:
    int size;
    SatCon **ptr;

  public:
    SatGraph(int s)
    {
        size = s;
        // 声明一个二维矩阵
        ptr = new SatCon *[s];
        for (int i = 0; i < s; i++)
        {
            ptr[i] = new SatCon[size];
        }
    }
    ~SatGraph()
    {
        for (int i = 0; i < size; i++)
        {
            delete[] ptr[i];
        }
        delete[] ptr;
    }
    SatCon *GetSatConn(int src, int dst)
    {
        return &ptr[src][dst];
    }

    void SatGraphInfo(void)
    {
        for (int i = 0; i < size; i++)
        {
            for (int j = 0; j < size; j++)
            {
                ptr[i][j].infoSatConn();
            }
        }
    }
};

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

int main()
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
        int size = 3;
        int second = 2;

        std::stringstream ss;
        ss << "{ \"node\": " << size << ", \"time\": " << second << " }";
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
                SatGraph *satGraph = new SatGraph(3);
                for (int i = 0; i < 3; ++i)
                {
                    for (int j = 0; j < 3; ++j)
                    {
                        satGraph->GetSatConn(i, j)->setSatConn(
                            i, j, jsonData[i][j][0].asBool(), jsonData[i][j][1].asFloat(), jsonData[i][j][2].asFloat());
                    }
                }
                satGraph->SatGraphInfo();
            }
            curl_easy_cleanup(curl);
        }
        return 0;
    }
}
