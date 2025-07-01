# Tool macros
CC ?= gcc
CXX ?= g++
CFLAGS ?= -Wall -Wextra -O2 -Iinterface
CXXFLAGS ?= -Wall -Wextra -O2 -Iinterface

# Qt support
QT_CFLAGS := $(shell pkg-config --cflags Qt5Widgets)
QT_LIBS   := $(shell pkg-config --libs Qt5Widgets)
CXXFLAGS += $(QT_CFLAGS)
LDLIBS   := $(QT_LIBS)
MOC      := moc

# Debug flags
DBGFLAGS := -g
COBJFLAGS := $(CXXFLAGS) -c

# Path macros
BUILD_PATH := build
BIN_PATH := $(BUILD_PATH)/bin
OBJ_PATH := $(BUILD_PATH)/obj
DBG_PATH := $(BUILD_PATH)/debug

SRC_PATH := src
INTERFACE_PATH := interface
TEST_PATH := tests

# Target macros
TARGET_NAME ?= myapp
ifeq ($(OS),Windows_NT)
	TARGET_NAME := $(addsuffix .exe,$(TARGET_NAME))
endif
TARGET := $(BIN_PATH)/$(TARGET_NAME)
TARGET_DEBUG := $(DBG_PATH)/$(TARGET_NAME)

# Source files
SRC_CPP := $(wildcard $(SRC_PATH)/*.cpp)
TEST_CPP := $(wildcard $(TEST_PATH)/*.cpp)
SRC := $(SRC_CPP) $(TEST_CPP)

# Header files for moc generation
HEADERS := $(wildcard $(INTERFACE_PATH)/*.h)
MOC_CPP := $(patsubst $(INTERFACE_PATH)/%.h, $(OBJ_PATH)/moc_%.cpp, $(HEADERS))
MOC_OBJ := $(patsubst %.cpp, %.o, $(MOC_CPP))

# Object files
OBJ := $(patsubst $(SRC_PATH)/%.cpp, $(OBJ_PATH)/%.o, $(SRC_CPP)) \
       $(patsubst $(TEST_PATH)/%.cpp, $(OBJ_PATH)/%.o, $(TEST_CPP)) \
       $(MOC_OBJ)

OBJ_DEBUG := $(patsubst $(SRC_PATH)/%.cpp, $(DBG_PATH)/%.o, $(SRC_CPP)) \
             $(patsubst $(TEST_PATH)/%.cpp, $(DBG_PATH)/%.o, $(TEST_CPP))

# Default rule
default: makedir all

# Linking targets
$(TARGET): $(OBJ)
	$(CXX) $(OBJ) -o $@ $(CXXFLAGS) $(LDLIBS)

$(TARGET_DEBUG): $(OBJ_DEBUG)
	$(CXX) $(OBJ_DEBUG) -o $@ $(CXXFLAGS) $(DBGFLAGS) $(LDLIBS)

# Build object files (normal)
$(OBJ_PATH)/%.o: $(SRC_PATH)/%.cpp
	$(CXX) $(COBJFLAGS) -o $@ $<

$(OBJ_PATH)/%.o: $(TEST_PATH)/%.cpp
	$(CXX) $(COBJFLAGS) -o $@ $<

# Build object files (debug)
$(DBG_PATH)/%.o: $(SRC_PATH)/%.cpp
	$(CXX) $(COBJFLAGS) $(DBGFLAGS) -o $@ $<

$(DBG_PATH)/%.o: $(TEST_PATH)/%.cpp
	$(CXX) $(COBJFLAGS) $(DBGFLAGS) -o $@ $<

# MOC rules
$(OBJ_PATH)/moc_%.cpp: $(INTERFACE_PATH)/%.h
	$(MOC) $< -o $@

$(OBJ_PATH)/moc_%.o: $(OBJ_PATH)/moc_%.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

# Directory setup
.PHONY: makedir
makedir:
	@mkdir -p $(BIN_PATH) $(OBJ_PATH) $(DBG_PATH)

# Targets
.PHONY: all
all: $(TARGET)

.PHONY: debug
debug: $(TARGET_DEBUG)

.PHONY: clean
clean:
	@echo CLEAN $(OBJ) $(OBJ_DEBUG) $(TARGET) $(TARGET_DEBUG)
	@rm -f $(OBJ) $(OBJ_DEBUG) $(TARGET) $(TARGET_DEBUG)

.PHONY: distclean
distclean: clean
