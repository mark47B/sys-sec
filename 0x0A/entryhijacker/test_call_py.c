#include <stdio.h>
#include <stdlib.h>

void __attribute__((constructor)) call_py()
{
  printf("DLL function 'call_py' was called\n");
  system("/usr/bin/python3");
}