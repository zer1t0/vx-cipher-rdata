#include "cipher_data.h"
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <wchar.h>

void dump(void* x, size_t s) {
  size_t i;
  for(i = 0; i < s; i++) {
    printf("0x%x ", ((char*)x)[i]);
  }
  printf("\n");
}

void test_bytes() {
  unsigned char result[] = { 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0xfe, 0xff };

  unsigned char bytes_param1[SIZE_bytes_param1_bytes];
  assert(!memcmp(result, bytes_param1_bytes_dec(bytes_param1), sizeof(result)));

  unsigned char bytes_param2[SIZE_bytes_param2_bytes];
  assert(!memcmp(result, bytes_param2_bytes_dec(bytes_param2), sizeof(result)));

  unsigned char bytes_file1[SIZE_bytes_file1_bytes];
  assert(!memcmp(result, bytes_file1_bytes_dec(bytes_file1), sizeof(result)));

  unsigned char bytes_file2[SIZE_bytes_file2_bytes];
  assert(!memcmp(result, bytes_file2_bytes_dec(bytes_file2), sizeof(result)));
}

void test_strings() {
  char string_param[SIZE_string_param_str];
  assert(!strcmp("string param", string_param_str_dec(string_param)));

  char name_str_param[SIZE_name_str_param_str];
  assert(!strcmp("string param", name_str_param_str_dec(name_str_param)));

  char string_file[SIZE_string_file_str];
  assert(!strcmp("string file", string_file_str_dec(string_file)));

  char name_str_file[SIZE_name_str_file_str];
  assert(!strcmp("string file", name_str_file_str_dec(name_str_file)));
  
}

void test_wstrings() {
  char result[] = {
    0x77, 0x00, 0x73, 0x00, 0x74, 0x00, 0x72, 0x00,
    0x69, 0x00, 0x6e, 0x00, 0x67, 0x00, 0x20, 0x00,
    0x70, 0x00, 0x61, 0x00, 0x72, 0x00, 0x61, 0x00,
    0x6d, 0x00, 0x00, 0x00
  };
  wchar_t wstring_param[SIZE_wstring_param_wstr / sizeof(wchar_t)];
  assert(!memcmp(result, wstring_param_wstr_dec(wstring_param), sizeof(result)));

  wchar_t name_wstr_param[SIZE_name_wstr_param_wstr / sizeof(wchar_t)];
  assert(!memcmp(result, name_wstr_param_wstr_dec(name_wstr_param), sizeof(result)));

  char result_file[] = {
    0x77, 0x00, 0x73, 0x00, 0x74, 0x00, 0x72, 0x00,
    0x69, 0x00, 0x6e, 0x00, 0x67, 0x00, 0x20, 0x00,
    0x66, 0x00, 0x69, 0x00, 0x6c, 0x00, 0x65, 0x00
  };
  wchar_t wstring_file[SIZE_wstring_file_wstr / sizeof(wchar_t)];
  assert(!memcmp(result_file, wstring_file_wstr_dec(wstring_file), sizeof(result_file)));

  wchar_t name_wstr_file[SIZE_name_wstr_file_wstr / sizeof(wchar_t)];
  assert(!memcmp(result_file, name_wstr_file_wstr_dec(name_wstr_file), sizeof(result_file)));
}

void test_u8s() {
  uint8_t result = 42;

  uint8_t u8_param1;
  assert(!memcmp((uint8_t*)&result, u8_param1_u8_dec(&u8_param1), sizeof(uint8_t)));

  uint8_t u8_param2;
  assert(!memcmp((uint8_t*)&result, u8_param2_u8_dec(&u8_param2), sizeof(uint8_t)));

  uint8_t u8_file1;
  assert(!memcmp((uint8_t*)&result, u8_file1_u8_dec(&u8_file1), sizeof(uint8_t)));

  uint8_t u8_file2;
  assert(!memcmp((uint8_t*)&result, u8_file2_u8_dec(&u8_file2), sizeof(uint8_t)));
}

void test_u16s() {
  uint16_t result = 42;

  uint16_t u16_param1;
  assert(!memcmp((uint16_t*)&result, u16_param1_u16_dec(&u16_param1), sizeof(uint16_t)));

  uint16_t u16_param2;
  assert(!memcmp((uint16_t*)&result, u16_param2_u16_dec(&u16_param2), sizeof(uint16_t)));

  uint16_t u16_file1;
  assert(!memcmp((uint16_t*)&result, u16_file1_u16_dec(&u16_file1), sizeof(uint16_t)));

  uint16_t u16_file2;
  assert(!memcmp((uint16_t*)&result, u16_file2_u16_dec(&u16_file2), sizeof(uint16_t)));
}

void test_u32s() {
  uint32_t result = 42;

  uint32_t u32_param1;
  assert(!memcmp((uint32_t*)&result, u32_param1_u32_dec(&u32_param1), sizeof(uint32_t)));

  uint32_t u32_param2;
  assert(!memcmp((uint32_t*)&result, u32_param2_u32_dec(&u32_param2), sizeof(uint32_t)));

  uint32_t u32_file1;
  assert(!memcmp((uint32_t*)&result, u32_file1_u32_dec(&u32_file1), sizeof(uint32_t)));

  uint32_t u32_file2;
  assert(!memcmp((uint32_t*)&result, u32_file2_u32_dec(&u32_file2), sizeof(uint32_t)));
}

void test_u64s() {
  uint64_t result = 42;

  uint64_t u64_param1;
  assert(!memcmp((uint64_t*)&result, u64_param1_u64_dec(&u64_param1), sizeof(uint64_t)));

  uint64_t u64_param2;
  assert(!memcmp((uint64_t*)&result, u64_param2_u64_dec(&u64_param2), sizeof(uint64_t)));

  uint64_t u64_file1;
  assert(!memcmp((uint64_t*)&result, u64_file1_u64_dec(&u64_file1), sizeof(uint64_t)));

  uint64_t u64_file2;
  assert(!memcmp((uint64_t*)&result, u64_file2_u64_dec(&u64_file2), sizeof(uint64_t)));
}

void test_i8s() {
  int8_t result = -42;

  int8_t i8_param1;
  assert(!memcmp((int8_t*)&result, i8_param1_i8_dec(&i8_param1), sizeof(int8_t)));

  int8_t i8_param2;
  assert(!memcmp((int8_t*)&result, i8_param2_i8_dec(&i8_param2), sizeof(int8_t)));

  int8_t i8_file1;
  assert(!memcmp((int8_t*)&result, i8_file1_i8_dec(&i8_file1), sizeof(int8_t)));

  int8_t i8_file2;
  assert(!memcmp((int8_t*)&result, i8_file2_i8_dec(&i8_file2), sizeof(int8_t)));
}

void test_i16s() {
  int16_t result = -42;

  int16_t i16_param1;
  assert(!memcmp((int16_t*)&result, i16_param1_i16_dec(&i16_param1), sizeof(int16_t)));

  int16_t i16_param2;
  assert(!memcmp((int16_t*)&result, i16_param2_i16_dec(&i16_param2), sizeof(int16_t)));

  int16_t i16_file1;
  assert(!memcmp((int16_t*)&result, i16_file1_i16_dec(&i16_file1), sizeof(int16_t)));

  int16_t i16_file2;
  assert(!memcmp((int16_t*)&result, i16_file2_i16_dec(&i16_file2), sizeof(int16_t)));
}

void test_i32s() {
  int32_t result = -42;

  int32_t i32_param1;
  assert(!memcmp((int32_t*)&result, i32_param1_i32_dec(&i32_param1), sizeof(int32_t)));

  int32_t i32_param2;
  assert(!memcmp((int32_t*)&result, i32_param2_i32_dec(&i32_param2), sizeof(int32_t)));

  int32_t i32_file1;
  assert(!memcmp((int32_t*)&result, i32_file1_i32_dec(&i32_file1), sizeof(int32_t)));

  int32_t i32_file2;
  assert(!memcmp((int32_t*)&result, i32_file2_i32_dec(&i32_file2), sizeof(int32_t)));
}

void test_i64s() {
  int64_t result = -42;

  int64_t i64_param1;
  assert(!memcmp((int64_t*)&result, i64_param1_i64_dec(&i64_param1), sizeof(int64_t)));

  int64_t i64_param2;
  assert(!memcmp((int64_t*)&result, i64_param2_i64_dec(&i64_param2), sizeof(int64_t)));

  int64_t i64_file1;
  assert(!memcmp((int64_t*)&result, i64_file1_i64_dec(&i64_file1), sizeof(int64_t)));

  int64_t i64_file2;
  assert(!memcmp((int64_t*)&result, i64_file2_i64_dec(&i64_file2), sizeof(int64_t)));

  int64_t i64_array[SIZE_i64_array_i64];
  int64_t result_array[] = { -42, -41 };
  assert(!memcmp(result_array, i64_array_i64_dec(i64_array), sizeof(result_array)));
  
}

int main() {

  test_bytes();
  test_strings();
  test_wstrings();
  test_u8s();
  test_u16s();
  test_u32s();
  test_u64s();
  test_i8s();
  test_i16s();
  test_i32s();
  test_i64s();
  printf("Test passed\n");
  return 0;
  /*
  char hello_world[SIZE_Hello_world_str] = { 0 };
  wchar_t bye_world[SIZE_Bye_world_wstr / sizeof(wchar_t)] = { 0 };
  size_t i = 0;
  wchar_t* bye_world2 = L"ab";
  wchar_t* bye_world3 = L"aaa";
  uint16_t port;

  printf("port: %u\n", *port_u16_dec(&port));
  printf("%s\n", Hello_world_str_dec(hello_world));

  Bye_world_wstr_dec(bye_world);
  for (i = 0; i < SIZE_Bye_world_wstr; i++) {
    printf("0x%x ", ((char*)bye_world)[i]);
  }
  printf("\n");
  for (i = 0; i < sizeof(bye_world2); i++) {
    printf("0x%x ", ((char*)bye_world2)[i]);
  }
  printf("\n");
  printf("%ls\n", bye_world2);
  printf("%u\n", sizeof(wchar_t));
  */
}
