CC := mpicc
CFLAGS := -O2 $(shell pkg-config --cflags fftw3)
LDFLAGS := -lfftw3_mpi -lm -Wl,-rpath,$(shell pkg-config --variable=libdir fftw3) $(shell pkg-config --libs fftw3)

TARGET := FFTWTest

all: $(TARGET)

$(TARGET): fftw_benchmark.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

.PHONY: clean

clean:
	rm -f $(TARGET)