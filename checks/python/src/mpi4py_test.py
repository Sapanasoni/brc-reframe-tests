import mpi4py
from mpi4py import MPI
import sys

print('mpi4py version: ', mpi4py.__version__)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
pname = MPI.Get_processor_name()



if (rank==0):
    print ("Expecting ", int(sys.argv[1]), " ranks")
    print ("======================")

    if hasattr(MPI, 'get_vendor'):
        print ("MPI Vendor is: ", MPI.get_vendor())

print ("Hello from ", pname, ", process ", rank , "of", size, ".")

MPI.Finalize()