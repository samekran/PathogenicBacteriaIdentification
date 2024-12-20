#ifndef _RamboConstruction_
#define _RamboConstruction_
#include <vector>
#include <set>
#include <string>
#include <bitset>
#include "constants.h"
#include "bitArray.h"


// vector<unsigned int> hashfunc( void* key, int len, int R, int B){
// }

class RAMBO{
    public:

        RAMBO(int n, int r1, int b1, int K, double p, int k_input);
        std::vector<unsigned int> hashfunc( std::string key, int len);
        void insertion (std::string setID, std::vector<std::string> keys);
        std::set<int> takeunion(std::set<int> set1, std::set<int> set2);
        std::set<int> takeIntrsec(std::set<int>* setArray);
        std::vector <std::string> getdata(std::string filenameSet);
        bitArray query (std::string query_key, int len);
        void createMetaRambo(int K, bool verbose);
        void serializeRAMBO(std::string dir);
        void deserializeRAMBO(std::vector<std::string> dir);
        void insertion2 (std::vector<std::string> alllines);
	bitArray queryseq (std::string query_key, int len);
	void insertionRare (std::string setID, std::vector<std::string> keys);

        int R ;
        int B;
        int n;
        float p;
        int range;
        int k;
        float FPR;
        BloomFiler** Rambo_array;
        std::vector<int>* metaRambo;
};

#endif
