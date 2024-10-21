cmake_minimum_required(VERSION 3.0)

project(cipher-test C)

if (NOT DEFINED Python3_EXECUTABLE)
        find_package(Python3 COMPONENTS Interpreter)
endif()

execute_process(
    COMMAND
    "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/gen-cipher-rdata.py"
    -s "string param"
    -s "name_str_param:string param"
    -w "wstring param"
    -w "name_wstr_param:wstring param"
    --u8 "u8_param1:42"
    --u8 "u8_param2:42"
    --u16 "u16_param1:42"
    --u16 "u16_param2:42"
    --u32 "u32_param1:42"
    --u32 "u32_param2:42"
    --u64 "u64_param1:42"
    --u64 "u64_param2:42"
    --i8 "i8_param1:-42"
    --i8 "i8_param2:-42"
    --i16 "i16_param1:-42"
    --i16 "i16_param2:-42"
    --i32 "i32_param1:-42"
    --i32 "i32_param2:-42"
    --i64 "i64_param1:-42"
    --i64 "i64_param2:-42"
    --i64 "i64_array:-42,-41"

    --bytes "bytes_param1:0102030405060708feff"
    --bytes "bytes_param2:0102030405060708feff"
    -f "${CMAKE_CURRENT_SOURCE_DIR}/vars.yaml"
    -o cipher_data
    RESULT_VARIABLE config_result
)

if (NOT ("${config_result}" EQUAL 0))
  message(FATAL_ERROR "Error building rdata.h: ${config_result}")
endif()

list(APPEND SRC_FILES
    main.c
    
    cipher_data.c
    cipher_data.h
)

add_executable(cipher-test ${SRC_FILES})
target_include_directories(cipher-test PUBLIC "${CMAKE_CURRENT_BINARY_DIR}")

include(CTest)
add_test(NAME cipher-test COMMAND cipher-test)
