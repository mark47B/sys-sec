#include <stdio.h>
#include <stdlib.h>
void foo(const char *a)
{
  printf("a: %s\n", a);
  system("/usr/bin/python3");
}
