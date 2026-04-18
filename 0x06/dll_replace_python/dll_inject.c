#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <dlfcn.h>

char d[100];

void call_from_dll(const char *f)
{
 void *h = dlopen(d, RTLD_LOCAL|RTLD_LAZY);
 if (h == NULL)
 {
  fprintf(stderr, "Could not open lib (%s)\n",
          dlerror());
  exit(1);
 }
 void *p = dlsym(h, f);
 if (p == NULL)
 {
  fprintf(stderr, "Could not find func (%s)\n",
          dlerror());
  exit(1);
 }
 ((void (*)(const char *))p)(d);
 dlclose(h);
}

int main(int argc, char *argv[])
{
 if (argc != 2) exit(1);
 strncpy(d, argv[1], 100);
 while (1)
 {
  call_from_dll("foo");
  sleep(10);
 }
}
