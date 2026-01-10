cmake_minimum_required(VERSION 3.20)
cmake_policy(SET CMP0167 NEW)
project(lib_zenoh)

add_library(zenoh_internal SHARED IMPORTED)

set_target_properties(zenoh_internal PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/include"
    IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/lib/libzenohc.so"
)

target_compile_definitions(zenoh_internal INTERFACE ZENOHCXX_ZENOHC)
target_link_libraries(zenoh_internal INTERFACE pthread dl)

# lib ( include 디렉토리 추가 )
add_library(libzenoh INTERFACE)
target_include_directories(libzenoh INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}")
target_link_libraries(libzenoh INTERFACE zenoh_internal)

# 예제
if (PROJECT_IS_TOP_LEVEL)
    add_executable(example_publisher example/example_publisher.cpp)     # publisher
    target_link_libraries(example_publisher PRIVATE libzenoh)           # publisher
    add_executable(example_subscriber example/example_subscriber.cpp)   # subscriber
    target_link_libraries(example_subscriber PRIVATE libzenoh)          # subscriber
endif ()