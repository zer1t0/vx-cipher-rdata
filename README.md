# vx-cipher-rdata

The script gen-cipher-rdata.py generates code to provide with encrypted data
stored in the rdata section. The intention is not support big chunks of data,
but little configuration options. Be aware that including many encrypted data
can increase the chance to not pass an entropy test.

The data types supported are the following:

- bytes: Array of bytes.
- strings: Regular char* strings.
- wstrings: wchar_t* strings of 2 bytes.
- integers: signed and unsigned integers of 8, 16, 32 and 64 bits. Arrays are
  supported by separated comma values.

The variables to encrypt can be passed as parameter or in a file. Each parameter
must include the name of the variable prefixed with ":", for example 
"--u16 port:80". In the strings the name is optional as it can be taken from the
string value itself.

Parameters are straigthforward but in case of file, it is a yaml file which
accepts the following sections:
- bytes or bs
- strings, string, str or strs
- wstrings, wstring, wstr or wstrs
- i8, i16, i32, i64
- u8, u16, u32, u64

Here is an example of file with strings:
```yaml
strings:
  - "Hello world"
  - "The cake is a lie"
  - ip:127.0.0.1
u16s:
  - port:443
```

