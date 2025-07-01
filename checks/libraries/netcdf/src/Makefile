FFLAGS := $(shell pkg-config --cflags netcdf-fortran)
LDFLAGS := $(shell pkg-config --libs netcdf-fortran) -Wl,-rpath,$(shell pkg-config --variable=libdir netcdf-fortran)
TARGET := simple_xy_wr

all: $(TARGET)

$(TARGET): simple_xy_wr.f90
	$(FC) $(FFLAGS) -o $@ $< $(LDFLAGS)

.PHONY: clean

clean:
	rm -f $(TARGET)
