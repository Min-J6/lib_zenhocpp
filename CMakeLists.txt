add_library(zenoh_internal SHARED IMPORTED)

set_target_properties(zenoh_internal PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/include"
    IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/bin/libzenohc.so"
)

target_compile_definitions(zenoh_internal INTERFACE ZENOHCXX_ZENOHC)
target_link_libraries(zenoh_internal INTERFACE pthread dl)

# lib
add_library(lib_zenohcpp INTERFACE)
target_include_directories(lib_zenohcpp INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}")
target_link_libraries(lib_zenohcpp INTERFACE zenoh_internal)