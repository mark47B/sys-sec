#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>

char message[100];

int main(int argc, char *argv[])
{
  if (argc != 2) exit(1);
  strncpy (message, argv[1], 100);
  while (1)
  {
    sleep(10);
    puts(message);
  }
  return 0;
}