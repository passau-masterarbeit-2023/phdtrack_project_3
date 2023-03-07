# echo -e colors
# WARN : don't put " and use the echo command, not echo -e
LIGHT_ORANGE_COLOR=\e[38;5;216m
TURQUOISE_COLOR=\e[38;5;43m
LIGHT_BLUE_COLOR=\e[38;5;153m
RED_COLOR=\e[38;5;196m
NO_COLOR=\e[0m

# paths
BIN_MAIN=bin/main
INC_MAIN=inc/main

BIN_TEST=bin/test
INC_TEST=inc/test

BIN_PERF=bin/perf
INC_PERF=inc/perf

BINS=$(BIN_MAIN) $(BIN_TEST) $(BIN_PERF)

# vars
ECHO = @echo # @echo hides this command in terminal, not its output

CC=g++
GDB_DEBUGGER_FLAGS=-g
PERSONAL_COMPIL_FLAGS=-D DEBUG -D COLORS # use own flags, see util.hpp
CFLAGS=-I $(INC_MAIN) -march=native -O3 $(PERSONAL_COMPIL_FLAGS) $(GDB_DEBUGGER_FLAGS)
LDLIBS=
LDFLAGS=--ansi --pedantic -Wall --std=c++11

SRCS_MAIN=$(wildcard src/main/**/*.cpp) $(wildcard src/main/*.cpp)
SRCS_TEST=$(wildcard src/test/**/*.cpp) $(wildcard src/test/*.cpp)
SRCS_PERF=$(wildcard src/perf/**/*.cpp) $(wildcard src/perf/*.cpp)
OBJS_MAIN=$(SRCS_MAIN:src/%.cpp=obj/%.o)
OBJS_TEST=$(SRCS_TEST:src/%.cpp=obj/%.o)
OBJS_PERF=$(SRCS_PERF:src/%.cpp=obj/%.o)

# at linking, give access to main/ to test files excluding the main main.
OBJ_MAIN_MAIN=obj/main/main.o
OBJS_MAIN_WITHOUT_MAIN=$(filter-out $(OBJ_MAIN_MAIN),$(OBJS_MAIN))


# targets
# set default target : https://stackoverflow.com/questions/2057689/how-does-make-app-know-default-target-to-build-if-no-target-is-specified
.DEFAULT_GOAL := default
.PHONY: default build build_test all clean run run_test rebuild rebuild_all rr ww dirs clear

default: build

build: $(BIN_MAIN)

build_test: $(BIN_TEST)

all: $(BINS)

$(BIN_MAIN): $(OBJS_MAIN) # linking main
	$(CC) -o $@ $^ $(LDFLAGS) $(LDLIBS)

obj/%.o: src/%.cpp # compiling main
	mkdir -p $(dir $@)
	$(CC) -o $@ -c $^ $(CFLAGS)

$(BIN_TEST): $(OBJS_TEST) $(OBJS_MAIN_WITHOUT_MAIN) # linking test
	$(CC) -o $@ $^ $(LDFLAGS) $(LDLIBS)

obj/test/%.o: src/test/%.cpp # compiling test
	mkdir -p $(dir $@)
	$(CC) -o $@ -c $^ $(CFLAGS) -I $(INC_TEST)

$(BIN_PERF): $(OBJS_PERF) $(OBJS_MAIN_WITHOUT_MAIN) # linking perf
	$(CC) -o $@ $^ $(LDFLAGS) $(LDLIBS)

obj/perf/%.o: src/perf/%.cpp # compiling perf
	mkdir -p $(dir $@)
	$(CC) -o $@ -c $^ $(CFLAGS) -I $(INC_PERF)

clean:
	rm -rf bin/* obj/*

run: $(BIN_MAIN)
	$(ECHO) "$(TURQUOISE_COLOR)*** Executing main *** $(NO_COLOR)"
	./$(BIN_MAIN)

run_test: $(BIN_TEST)
	$(ECHO) "$(TURQUOISE_COLOR)*** Executing test *** $(NO_COLOR)"
	./$(BIN_TEST)

run_perf: $(BIN_PERF)
	$(ECHO) "$(TURQUOISE_COLOR)*** Executing perf *** $(NO_COLOR)"
	./$(BIN_PERF)

valgrind:
	valgrind --leak-check=full --show-leak-kinds=all ./$(BIN_MAIN)

# Determine this makefile's path.
# Be sure to place this BEFORE `include` directives, if any.
THIS_FILE := $(lastword $(MAKEFILE_LIST))

rebuild:
	@$(MAKE) -f $(THIS_FILE) clean
	@$(MAKE) -f $(THIS_FILE) build

rebuild_all:
	@$(MAKE) -f $(THIS_FILE) clean
	@$(MAKE) -f $(THIS_FILE) build_all

rr: # rebuild and rerun (main)
	@$(MAKE) -f $(THIS_FILE) clean
	@$(MAKE) -f $(THIS_FILE) build
	@$(MAKE) -f $(THIS_FILE) run

clear: # alias of clean
	@$(MAKE) -f $(THIS_FILE) clean

ww: # where and what
	pwd
	ls -alt

dirs:
	mkdir -p bin/
	mkdir -p obj/
