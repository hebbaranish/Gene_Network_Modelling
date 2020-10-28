Multithreaded_RACIPE - Multithreading RACIPE using OpenMP and many other improvements. Use the flag -threads [] to select the number of threads during runtime.

Multithreaded_RACIPE(Python) - Multithreading RACIPE using a python script, which splits paramter sets between different RACIPE instances and runs them at the same time, then recombines the files. Modify run.py to change values.

RACIPE-1.0_euleronly - Multithreaded racipe but compatible with older glibc versions, and so should run on Ubuntu 18.04 at least (glibc 2.28).
NOTE: This version only runs euler, and cannot run RK45. This version can also run on older glibc versions, and so can run on non-updated lab PCs too. Please include the flag "-solver 1" explicitly to avoid errors.

Standard_RACIPE - The standard version of RACIPE code with a few modifications.
