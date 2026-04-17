#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <errno.h>
#include <signal.h>

#define CMD_MAX_LEN 16
#define CMD_VAL "ls -lha ./"

typedef char * cmd_t;

#pragma pack(push, 1)
struct cred {
  char user[18];
  char passwd[6];
} cred;
#pragma pack(pop)

typedef struct cred * cred_p;

void handle_sigint(int sig) {
  if (sig == SIGINT) {
    printf("\b\b\033[K"); // remove ^C
    printf("SIGINT is ignored\n> ");
    fflush(stdout);
  }
}

void *create_obj(size_t n) {
  void *m = malloc(n);
  assert(m != NULL);
  return m;
}

cmd_t create_cmd() {
  assert(strlen(CMD_VAL) < CMD_MAX_LEN);
  cmd_t cmd = (cmd_t)create_obj(CMD_MAX_LEN);
  strcpy(cmd, CMD_VAL);
  printf("Command '%s' was created\n", cmd);
  return cmd;
}

void exec_cmd(const cmd_t cmd, const cred_p cred) {
  if (cred == NULL) {
    fprintf(stderr,
            "First of all login before executing the command\n");
    return;
  }
  if (cmd != NULL) {
    printf("Try to execute '%s'\n", cmd);
    const int res = system(cmd);
    if (res == -1)
      fprintf(stderr, "Error while calling the command '%s', "
              "description: %s\n", cmd, strerror(errno));
    else if (res != 0)
      fprintf(stderr, "Error while calling the command '%s', "
              "status code: %d\n", cmd, res);
    else
      printf("The command '%s' was executed successfully\n", cmd);
  }
  else
    fprintf(stderr, "Could not execute command (cmd is NULL)\n"
            "First of all create it\n");
}

void destroy_obj(void *obj) {
  free(obj); 
}

void destroy_cmd(cmd_t cmd) {
  if (cmd == NULL)
    fprintf(stderr, "Could not destroy cmd (cmd is NULL)\n");
  destroy_obj(cmd);
}

void print_cred(const cred_p cred) {
  if (cred != NULL)
    printf("Cred is '(%s, %s)'\n", cred->user, cred->passwd);
  else
    fprintf(stderr, "Could not print cred (cred is NULL)\n"
            "First of all login\n");
}

cred_p login(cred_p cred) {
  if (cred != NULL)
    fprintf(stderr, "You have already logged in\n");
  else {
    cred = (cred_p)create_obj(sizeof(struct cred));
    printf("Type user name: ");
    scanf(" %17[^\n]s", cred->user); // there is no overflow
    printf("Type passwd value: ");
    scanf(" %5[^\n]s", cred->passwd); // there is no overflow
  }
  print_cred(cred);
  return cred;
}

void logout(cred_p *cred) {
  assert(cred != NULL);
  if (*cred == NULL)
    fprintf(stderr, "Could not logout (cred is NULL)\n");
  destroy_obj(*cred);
  *cred = NULL;
}

int main(int argc, char *argv[]) {
  printf("Welcome to %s\n", argv[0]);
  signal(SIGINT, handle_sigint);
  unsigned char last = 0;
  cmd_t cmd = NULL;
  cred_p cred = NULL;
  unsigned char show_menu = 1;
  char input[2];
  while (!last) {
    if (show_menu) {
      printf("Type:\n");
      printf("\t- c for creating the command\n");
      if (cmd != NULL) {
        printf("\t- e for executing the command\n");
        printf("\t- d for desroying the command\n");
      }
      printf("\t- i for login\n");
      if (cred != NULL) {
        printf("\t- p for printing the cred data\n");
        printf("\t- o for logout\n");
      }
      printf("\t- m for printing the menu\n");
      printf("\t- q for interrupting and quit\n");
      show_menu = 0;
    }
    printf("> ");
    fflush(stdout);
    const int c = scanf("%1s", input);
    if (c != 1) {
      if (c == EOF)
        printf("EOF is ignored\n");
      else
        fprintf(stderr, "Could not read data from keyboard "
                "(something was wrong)\n", input);
      clearerr(stdin);
      continue;
    }
    if (strlen(input) != 1) {
      fprintf(stderr, "Unrecognized input: '%s'\nTry again\n",
              input);
      continue;
    }
    switch(input[0]) {
    case 'c':
      cmd = create_cmd();
      break;
    case 'e':
      exec_cmd(cmd, cred);
      break;
    case 'd':
      destroy_cmd(cmd);
      break;
    case 'i':
      cred = login(cred);
      break;
    case 'p':
      print_cred(cred);
      break;
    case 'o':
      logout(&cred);
      break;
    case 'm':
      show_menu = 1;
      break;
    case 'q':
      last = 1;
      break;
    case EOF:
      printf("EOF is ignored\n");
      break;
    default:
      fprintf(stderr, "Unrecognized input: '%s'\nTry again\n",
              input);
      break;
    }
  }
  return 0;
}
