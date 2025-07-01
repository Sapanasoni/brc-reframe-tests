CFLAGS := $(shell pkg-config --cflags gsl)
LDFLAGS := $(shell pkg-config --libs gsl) -Wl,-rpath,$(shell pkg-config --variable=libdir gsl)
TARGET := gsl_bessel_example

all: $(TARGET)

$(TARGET): gsl_bessel_example.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

.PHONY: clean

clean:
	rm -rf $(TARGET)