CFLAGS := -I$(BOOST_ROOT)/include
TARGET := datetime

all: $(TARGET)

$(TARGET): date_time_example.cpp
	$(CXX) $(CFLAGS) -o $@ $< 

.PHONY: clean

clean:
	rm -f $(TARGET)
