# Compiler
CXX := arch -x86_64 /usr/local/bin/g++-14

# macOS SDK path
SDK_PATH := $(shell xcrun --show-sdk-path)

# Compiler flags
CXXFLAGS := -Wall -fopenmp -std=c++11 -O2 -m64 -isysroot $(SDK_PATH) -march=x86-64 -mtune=generic -fno-use-linker-plugin
INCLUDE := -Iinclude/ -Iinclude/smhasher/src # Added smhasher include path

# Linker flags
LDFLAGS := -m64 -static-libgcc -static-libstdc++ -fuse-ld=gold

# Build directory
BUILD := ./build

# Target executable
TARGET := program

# Source files
SRC := src/utils.cpp src/main.cpp src/insertBloomfilter.cpp \
       src/bitArray.cpp src/Rambo_construction.cpp src/MyBloom.cpp \
       src/MurmurHash3.cpp

# Object files
OBJECTS := $(SRC:%.cpp=$(BUILD)/%.o)

# Default target
all: clean build $(BUILD)/$(TARGET)

# Build target
$(BUILD)/$(TARGET): $(OBJECTS)
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) $(OBJECTS) $(LDFLAGS) -o $@

# Compile source files
$(BUILD)/%.o: %.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -o $@ -c $<

# Build directory creation
build:
	@mkdir -p $(BUILD)

# Clean target
clean:
	-@rm -rvf $(BUILD)/*

# Debug and release builds
debug: CXXFLAGS += -DDEBUG -g
debug: all

release: CXXFLAGS += -O3
release: all

.PHONY: all build clean debug release
