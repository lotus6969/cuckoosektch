#ifndef _CUCKOO_SKETCH_H
#define _CUCKOO_SKETCH_H

// #define TEST
#include <string>
#define CHECK_TOP
#ifndef CHECK_TOP
    #define TOP 2
#endif

#include <stdint.h>
#include <algorithm>
#include <functional>
#include <vector>
#include <limits.h>
#include <iostream>

#include "LossyStrategy.h"
#include "BaseSketch.h"
#include "BOBHASH64.h"


namespace sketch {
namespace cuckoosketch {
const int MAX_ROW = 2;
const int MAX_ENTRY = 5;

class Entry {
public:
    Entry(): ID(""), fingerprint(0), count(0), l0fp(0) {}
    Entry(const std::string &id, uint32_t fp, uint32_t cnt): ID(id), fingerprint(fp), count(cnt), l0fp(fp >> 24) {}
    uint32_t Empty();
    bool Equalfp(uint8_t fp);
    bool Equall0fp(uint32_t fp);
    void Insert();
    void Insert(uint32_t fp, const std::string &id, uint32_t cnt = 1);
    void Lossy(std::function<void(uint32_t &)> &lossy_func);

    uint8_t get_fingerprint();
    uint32_t get_l0fp();
    uint32_t get_count();
    std::string get_ID();

    bool operator<(const Entry &e) const {
        return count > e.count;
    }
private:
    std::string ID;
    uint8_t fingerprint;
    uint32_t l0fp;
    uint32_t count;
};

class Bucket {
public:
    Bucket() {
        entries.resize(MAX_ENTRY);
    }
    void Clear();
    bool Empty(int index);
    bool Full(int index);
    void Insert(int index);
    void Insert(int index, const Entry &entry);
    void Insert(int index, uint32_t fp, const std::string &id);
    void Remove(int index);
    void Lossy(int index, std::function<void(uint32_t &)> &lossy_func);
    void BucketSort(int index);
    bool Equal(int index, uint32_t fp);

    uint8_t get_fp(int index);
    Entry get_entry(int index);
    int get_col_index();
    int get_entry_count(int index);
    void down_stairs(int index);
private:
    std::vector<Entry> entries;
    int col_index;
};

class CuckooSketch: public BaseSketch {
public:
    CuckooSketch(int threshold1, int K, int MEM);
    ~CuckooSketch();
    void clear();
    void Insert(const std::string &str) override;
    std::pair<std::string, int> Query(int k);
    void work();
    std::string get_name();

private:
    uint64_t Hash(const std::string &str);
    uint64_t Hash(uint8_t fp);
    bool kickout(int kick_num, uint64_t &hash_value, Bucket &cur_bucket, 
                 int entry_index, int array_index);
    int _bucket_num;
    int _threshold1;
    BOBHash64 *_bobhash;
    std::vector<std::vector<Bucket> > _buckets;
    Lossy::BaseStrategy *_lossy;
    std::function<void(uint32_t &)> _lossy_func;
    std::vector<Entry> _ret;
    int _K;
};

const int MAX_KICK_OUT = 2;

// Entry
uint32_t Entry::Empty() {
    return count == 0;
}

bool Entry::Equalfp(uint8_t fp) {
    return fp == fingerprint;
}

bool Entry::Equall0fp(uint32_t fp) {
    return fp == l0fp;
}

void Entry::Insert() {
    ++count;
}

void Entry::Insert(uint32_t fp, const std::string &id, uint32_t cnt) {
    l0fp = fp;
    fingerprint = fp >> 24;
    this->ID = id;
    this->count = cnt;
}

void Entry::Lossy(std::function<void(uint32_t &)> &lossy_func) {
    lossy_func(count);
}

uint8_t Entry::get_fingerprint() {
    return fingerprint;
}

uint32_t Entry::get_l0fp() {
    return l0fp;
}

uint32_t Entry::get_count() {
    return count;
}

std::string Entry::get_ID() {
    return ID;
}

// Bucket:
// | entry  | FP    | count|
// | entry0 | 32bit | 32bit|
// | entry1 | 8bit  | 16bit|
// | entry2 | 8bit  | 8bit |
// | entry3 | 8bit  | 4bit |
// | entry4 | 8bit  | 4bit |
void Bucket::Clear() {
    entries.clear();
    entries.resize(MAX_ENTRY);
}

bool Bucket::Empty(int index) {
    return entries[index].Empty();
}

bool Bucket::Full(int index) {
    switch (index) {
        case 0:
            return entries[index].get_count() == 0xffffffff;
        case 1:
            return entries[index].get_count() >= 0xffff;
        case 2:
            return entries[index].get_count() >= 0xff;
        case 3:case 4:
            return entries[index].get_count() >= 0xf;
    }
    return false;
}

// for match
void Bucket::Insert(int index) {
    entries[index].Insert();
}

// for kick entry
void Bucket::Insert(int index, const Entry &entry) {
    entries[index] = entry;
}

// for empty entry
void Bucket::Insert(int index, uint32_t fp, const std::string &id) {
    entries[index].Insert(fp, id);
}

void Bucket::Remove(int index) {
    while (index + 1 < MAX_ENTRY) {
        entries[index] = std::move(entries[index + 1]);
        index++;
    }
}

void Bucket::Lossy(int index, std::function<void(uint32_t &)> &lossy_func) {
    entries[index].Lossy(lossy_func);
}

void Bucket::BucketSort(int index) {
    while (index > 0 && entries[index].get_count() > entries[index - 1].get_count()) {
        std::swap(entries[index], entries[index - 1]);
        --index;
    }
}

bool Bucket::Equal(int index, uint32_t fp) {
    if (index == 0) {
        return entries[index].Equall0fp(fp);
    } else {
        return entries[index].Equalfp(fp >> 24);
    }
    // return entries[index].Equal(fp);
}

uint8_t Bucket::get_fp(int index) {
    // if (index == 0) {
    //     return entries[0].get_l0fp();
    // }
    return entries[index].get_fingerprint();
}

Entry Bucket::get_entry(int index) {
    return entries[index];
}

int Bucket::get_col_index() {
    return col_index;
}

int Bucket::get_entry_count(int index) {
    return entries[index].get_count();
}

void Bucket::down_stairs(int index) {
    int cur_index = MAX_ENTRY - 1;
    while (cur_index > index) {
        entries[cur_index] = std::move(entries[cur_index - 1]);
        --cur_index;
    }
}

// CuckooSketch
CuckooSketch::CuckooSketch(int threshold1, int K, int MEM) {
    const int BUCKETSIZE = 128;
    _bucket_num = 0;
    for (; _bucket_num * BUCKETSIZE * MAX_ROW <= MEM * 1000 * 8; ++_bucket_num);
    --_bucket_num;
    _buckets.resize(MAX_ROW, std::vector<Bucket>(_bucket_num));

    _K = K;
    _threshold1 = threshold1;
    _bobhash = new BOBHash64(1005);
    _lossy_func = Lossy::MinusOneStrategy{};
}

CuckooSketch::~CuckooSketch() {
    // delete _bobhash;
}

void CuckooSketch::clear() {
    _buckets.clear();
    _buckets.resize(MAX_ROW, std::vector<Bucket>(_bucket_num));
}

void CuckooSketch::Insert(const std::string &str) {
    uint64_t hash_key = Hash(str);
    uint32_t fp = hash_key >> 32;
    uint64_t hash_value[2] = {hash_key, hash_key ^ Hash(static_cast<uint8_t>(fp >> 24))};

    uint64_t keys[2] = {hash_value[0] % _bucket_num, hash_value[1] % _bucket_num};

    Bucket &bucket0 = _buckets[0][keys[0]];
    Bucket &bucket1 = _buckets[1][keys[1]];

    // entry 0:
    if (bucket0.Equal(0, fp)) {
        bucket0.Insert(0);
        return;
    }
    if (bucket0.Empty(0)) {
        bucket0.Insert(0, fp, str);
        return;
    }
    if (bucket1.Equal(0, fp)) {
        bucket1.Insert(0);
        return;
    }
    if (bucket1.Empty(0)) {
        bucket1.Insert(0, fp, str);
        return;
    }

    for (int i = 1; i < MAX_ENTRY; i++) {
        if (bucket0.Equal(i, fp)) {
            bucket0.Insert(i);
            bucket0.BucketSort(i);
            if (bucket0.get_entry_count(1) > _threshold1) {
                if (kickout(MAX_KICK_OUT, hash_value[0], bucket0, 1, 0)) {
                    // std::cout << "kickout" << std::endl;
                    bucket0.Remove(1);
                }
            }
            return;
        }
        if (bucket0.Empty(i)) {
            bucket0.Insert(i, fp, str);
            return;
        }
        if (bucket1.Equal(i, fp)) {
            bucket1.Insert(i);
            bucket1.BucketSort(i);
            if (bucket1.get_entry_count(1) > _threshold1) {
                if (kickout(MAX_KICK_OUT, hash_value[1], bucket1, 1, 1)) {
                    bucket1.Remove(1);
                }
            }
            return;
        }
        if (bucket1.Empty(i)) {
            bucket1.Insert(i, fp, str);
            return;
        }
    }

    // lossy strategy
    if (bucket0.get_entry_count(MAX_ENTRY - 1) < bucket1.get_entry_count(MAX_ENTRY - 1)) {
        bucket0.Lossy(MAX_ENTRY - 1, _lossy_func);
    } else {
        bucket1.Lossy(MAX_ENTRY - 1, _lossy_func);
    }
}

std::pair<std::string, int> CuckooSketch::Query(int k) {
    return std::make_pair(_ret[k].get_ID(), _ret[k].get_count());
}

void CuckooSketch::work() {
    _ret.resize(_bucket_num * MAX_ROW);
    for (int i = 0; i < MAX_ROW; i++) {
        for (int j = 0; j < _bucket_num; j++) {
            _ret[i * _bucket_num + j] = _buckets[i][j].get_entry(0);
        }
    }
    sort(_ret.begin(), _ret.end());
}

std::string CuckooSketch::get_name() {
    return "CuckooSketch";
}

uint64_t CuckooSketch::Hash(const std::string &str) {
    return _bobhash->run(str.c_str(), str.length());
}

uint64_t CuckooSketch::Hash(uint8_t fp) {
    return _bobhash->run((char *)&fp, 1);
}

bool CuckooSketch::kickout(int kick_num, uint64_t &hash_value, Bucket &cur_bucket, 
                           int entry_index, int array_index) {
    if (kick_num == 0) {
        return false;
    }

    uint8_t fp = cur_bucket.get_fp(entry_index);
    uint64_t next_hash_value = hash_value ^ Hash(fp);
    Bucket &next_bucket = _buckets[1 - array_index][next_hash_value % _bucket_num];

    // Insert
    if (cur_bucket.get_entry_count(entry_index) > next_bucket.get_entry_count(0)) {
        next_bucket.down_stairs(0);
        next_bucket.Insert(0, cur_bucket.get_entry(entry_index));
        return true;
    }

    // Kickout and Insert
    if (kickout(kick_num - 1, next_hash_value, next_bucket, 0, 1 - array_index)) {
        next_bucket.down_stairs(0);
        next_bucket.Insert(0, cur_bucket.get_entry(entry_index));
        return true;
    }
    return false;
}

} // namespace cuckoosketch
} // namespace sketch

#endif