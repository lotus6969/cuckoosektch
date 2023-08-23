CPPFLAGS = -Wall -O3 -std=c++14 -lm -w -mcmodel=medium -g -mcmodel=small
PROGRAMS = cuckoo 

all: $(PROGRAMS)

cuckoo:main.cpp \
	BOBHASH32.h BOBHASH64.h CuckooCounter.h heavykeeper.h LossyCounting.h params.h spacesaving.h ssummary.h ASketch.h MVSketch.h NitroSketch.h ElasticSketch.h CuckooSketch.h LossyStrategy.h CuckooSketchPro.h
	g++ -o cuckoo main.cpp $(CPPFLAGS)

clean:
	rm -f *.o $(PROGRAMS)
