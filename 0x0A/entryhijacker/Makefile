CC = gcc -Wall -Wextra -m32 -no-pie
BINS = infinite_loop hello_world simple_exit
LIBS = test_call_sh.so test_call_py.so test_call_pl.so
TARGETS = $(BINS) $(LIBS)

all: $(TARGETS)

# compile test victim files
$(BINS): %: %.c
	@echo "\033[0;31m"compiling binary $@..."\033[0m"
	$(CC) $< -o $@

# compile test injected files
test_call_%.so: test_call_%.c
	@echo "\033[0;31m"compiling library $@..."\033[0m"
	gcc -m32 -fPIC -shared $< -o $@

.PHONY: all clean

# remove generated binary files
clean:
	@echo "\033[0;33m"cleaning the binary files..."\033[0m"
	rm -f $(TARGETS)