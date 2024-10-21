import argparse
from collections import namedtuple
import os
import re
import yaml

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s", "--string",
        help="A char* string",
        action="append",
    )

    parser.add_argument(
        "-w", "--wstring",
        help="A wchar_t* string (sizeof(wchar_t) = 2 bytes) encoded with utf-16-le",
        action="append",
    )

    parser.add_argument(
        "--u8",
        help="An uint8_t number in form <name>:<number>",
        action="append",
        type=get_u8_name_value,
    )

    parser.add_argument(
        "--u16",
        help="An uint16_t number in form <name>:<number>",
        action="append",
        type=get_u16_name_value,
    )

    parser.add_argument(
        "--u32",
        help="An uint32_t number in form <name>:<number>",
        action="append",
        type=get_u32_name_value,
    )

    parser.add_argument(
        "--u64",
        help="An uint64_t number in form <name>:<number>",
        action="append",
        type=get_u64_name_value,
    )

    parser.add_argument(
        "--i8",
        help="An int8_t number in form <name>:<number>",
        action="append",
        type=get_i8_name_value,
    )

    parser.add_argument(
        "--i16",
        help="An int16_t number in form <name>:<number>",
        action="append",
        type=get_i16_name_value,
    )

    parser.add_argument(
        "--i32",
        help="An int32_t number in form <name>:<number>",
        action="append",
        type=get_i32_name_value,
    )

    parser.add_argument(
        "--i64",
        help="An int64_t number in form <name>:<number>",
        action="append",
        type=get_i64_name_value,
    )
    
    parser.add_argument(
        "-b", "--bytes",
        help="An array of bytes in hex. The format is <name>:<hex>",
        action="append",
        type=get_bytes_name_value,
    )

    parser.add_argument(
        "-f", "--file",
        help="A yaml file with parameters",
    )

    parser.add_argument(
        "-o", "--out",
        help="Name for the c and h files generated, without extension",
        default="rdatavars",
    )

    args = parser.parse_args()
    
    args.wstring = args.wstring or []
    args.string = args.string or []
    args.bytes = args.bytes or []
    args.u8 = args.u8 or []
    args.u16 = args.u16 or []
    args.u32 = args.u32 or []
    args.u64 = args.u64 or []
    args.i8 = args.i8 or []
    args.i16 = args.i16 or []
    args.i32 = args.i32 or []
    args.i64 = args.i64 or []
    
    return args
    
def main():
    args = parse_args()
    filename = args.out

    parameters = get_parameters(
        args.file,
        bs=args.bytes,
        strings=args.string,
        wstrings=args.wstring,
        u8s=args.u8,
        u16s=args.u16,
        u32s=args.u32,
        u64s=args.u64,
        i8s=args.i8,
        i16s=args.i16,
        i32s=args.i32,
        i64s=args.i64,
    )

    c_vars = parameters_to_variables(parameters)

    h_code, c_code = gen_code(c_vars, filename)

    with open("{}.h".format(filename), "w") as fo:
        fo.write(h_code)

    with open("{}.c".format(filename), "w") as fo:
        fo.write(c_code)

    print("Cipher variables wrote to {}.h and {}.c".format(filename, filename))

def get_parameters(
        config,
        bs, strings, wstrings,
        u8s, u16s, u32s, u64s,
        i8s, i16s, i32s, i64s
):
    parameters = Parameters(
        bytes=bs,
        strings=strings,
        wstrings=wstrings,
        u8s=u8s,
        u16s=u16s,
        u32s=u32s,
        u64s=u64s,
        i8s=i8s,
        i16s=i16s,
        i32s=i32s,
        i64s=i64s,
    )

    if config:
        content = load_params_file(config)

        parameters.bytes.extend(content.pop("bytes", []))
        parameters.bytes.extend(content.pop("bs", []))
        
        parameters.strings.extend(content.pop("string", []))
        parameters.strings.extend(content.pop("strings", []))
        parameters.strings.extend(content.pop("str", []))
        parameters.strings.extend(content.pop("strs", []))
    
        parameters.wstrings.extend(content.pop("wstring", []))
        parameters.wstrings.extend(content.pop("wstrings", []))
        parameters.wstrings.extend(content.pop("wstr", []))
        parameters.wstrings.extend(content.pop("wstrs", []))

        parameters.u8s.extend(content.pop("u8", []))
        parameters.u8s.extend(content.pop("u8s", []))

        parameters.u16s.extend(content.pop("u16", []))
        parameters.u16s.extend(content.pop("u16s", []))

        parameters.u32s.extend(content.pop("u32", []))
        parameters.u32s.extend(content.pop("u32s", []))

        parameters.u64s.extend(content.pop("u64", []))
        parameters.u64s.extend(content.pop("u64s", []))

        parameters.i8s.extend(content.pop("i8", []))
        parameters.i8s.extend(content.pop("i8s", []))
        
        parameters.i16s.extend(content.pop("i16", []))
        parameters.i16s.extend(content.pop("i16s", []))

        parameters.i32s.extend(content.pop("i32", []))
        parameters.i32s.extend(content.pop("i32s", []))

        parameters.i64s.extend(content.pop("i64", []))
        parameters.i64s.extend(content.pop("i64s", []))
        
        not_used_fields = list(content.keys())
        if not_used_fields:
            raise ValueError("{} fields of params file are not recognized".format(
                ", ".join(not_used_fields)
            ))
    
    return parameters

Parameters = namedtuple("Parameters", [
    "bytes",
    "strings",
    "wstrings",
    "u8s",
    "u16s",
    "u32s",
    "u64s",
    "i8s",
    "i16s",
    "i32s",
    "i64s",
])
    
def load_params_file(filepath):
    with open(filepath) as fi:
        content = yaml.safe_load(fi)

    return content

def parameters_to_variables(params):
    c_vars = []
    for b in params.bytes:
        name, value = get_bytes_name_value(b)
        enc, key = enc_bytes(value)
        c_vars.append(Variable(
            type="bytes",
            name=name,
            value=value,
            enc_value=enc,
            enc_key=key
        ))
    
    for s in params.strings:
        name, value = get_str_name_value(s)
        enc, key = enc_str(value)
        c_vars.append(Variable(
            type="str",
            name=name,
            value=value,
            enc_value=enc,
            enc_key=key
        ))

    for w in params.wstrings:
        name, value = get_str_name_value(w)
        enc, key = enc_wstr(value)
        c_vars.append(Variable(
            type="wstr",
            name=name,
            value=value,
            enc_value=enc,
            enc_key=key
        ))
        
    for u8 in params.u8s:
        name, values = get_u8_name_value(u8)
        enc, key = enc_u8s(values)
        c_vars.append(Variable(
            type="u8",
            name=name,
            value=values,
            enc_value=enc,
            enc_key=key,
        ))

    for u16 in params.u16s:
        name, values = get_u16_name_value(u16)
        enc, key = enc_u16s(values)
        c_vars.append(Variable(
            type="u16",
            name=name,
            value=values,
            enc_value=enc,
            enc_key=key,
        ))

    for u32 in params.u32s:
        name, values = get_u32_name_value(u32)
        enc, key = enc_u32s(values)
        c_vars.append(Variable(
            type="u32",
            name=name,
            value=values,
            enc_value=enc,
            enc_key=key,
        ))

    for u64 in params.u64s:
        name, values = get_u64_name_value(u64)
        enc, key = enc_u64s(values)
        c_vars.append(Variable(
            type="u64",
            name=name,
            value=values,
            enc_value=enc,
            enc_key=key,
        ))

    for i8 in params.i8s:
        name, values = get_i8_name_value(i8)
        enc, key = enc_i8s(values)
        c_vars.append(Variable(
            type="i8",
            name=name,
            value=values,
            enc_value=enc,
            enc_key=key,
        ))

    for i16 in params.i16s:
        name, values = get_i16_name_value(i16)
        enc, key = enc_i16s(values)
        c_vars.append(Variable(
            type="i16",
            name=name,
            value=values,
            enc_value=enc,
            enc_key=key,
        ))

    for i32 in params.i32s:
        name, values = get_i32_name_value(i32)
        enc, key = enc_i32s(values)
        c_vars.append(Variable(
            type="i32",
            name=name,
            value=values,
            enc_value=enc,
            enc_key=key,
        ))

    for i64 in params.i64s:
        name, values = get_i64_name_value(i64)
        enc, key = enc_i64s(values)
        c_vars.append(Variable(
            type="i64",
            name=name,
            value=values,
            enc_value=enc,
            enc_key=key,
        ))


    return c_vars
    
def get_str_name_value(s):
    parts = s.split(":", 1)
    if len(parts) == 2:
        return (parts[0], parts[1])
    else:
        return (str_to_name(s), s)

def get_bytes_name_value(v):
    if type(v) is tuple \
       and len(v) == 2\
       and type(v[0]) is str\
       and type(v[1]) is bytes:
        return v

    if type(v) is not str:
        raise argparse.ArgumentTypeError("bytes {} Must in form <name>:<hex>".format(v))
    
    try:
        name, value = v.split(":")
    except ValueError:
        raise argparse.ArgumentTypeError("bytes {} Must in form <name>:<hex>".format(v))

    try:
        value = bytes.fromhex(value)
    except ValueError:
        raise argparse.ArgumentTypeError("{} must be a hex string".format(value))

    return name, value

def get_u8_name_value(v):
    return get_int_name_value(v, "u8", 0, 255)
    
def get_u16_name_value(v):
    return get_int_name_value(v, "u16", 0, 2**16 - 1)

def get_u32_name_value(v):
    return get_int_name_value(v, "u32", 0, 2**32 - 1)

def get_u64_name_value(v):
    return get_int_name_value(v, "u64", 0, 2**64 - 1)

def get_i8_name_value(v):
    return get_int_name_value(v, "i8", -2**7, 2**7 - 1)

def get_i16_name_value(v):
    return get_int_name_value(v, "i16", -2**15, 2**15 - 1)

def get_i32_name_value(v):
    return get_int_name_value(v, "i32", -2**31, 2**31 - 1)

def get_i64_name_value(v):
    return get_int_name_value(v, "i64", -2**63, 2**63 - 1)

def get_int_name_value(v, type_name, min_value, max_value):
    if type(v) is tuple \
       and len(v) == 2\
       and type(v[0]) is str\
       and type(v[1]) is list:
        return v

    if type(v) is not str:
        raise argparse.ArgumentTypeError("{} {} Must in form <name>:<number>".format(type_name, v))
    
    try:
        name, values = v.split(":")
    except ValueError:
        raise argparse.ArgumentTypeError("{} {} Must in form <name>:<number>".format(type_name, v))

    int_values = []
    for value in values.split(","):
        try:
            value = int(value, base=0)
            if value < min_value or value > max_value:
                raise ValueError()
            int_values.append(value)
        except ValueError:
            raise argparse.ArgumentTypeError("{} is not an integer between {} and {}".format(value, min_value, max_value))

    return name, int_values
    
def str_to_name(s):
    return re.sub("[^0-9a-zA-Z]", "_", s)
    
def gen_key(size):
    return os.urandom(size)

def enc_u8s(u8s):
    return enc_ints(u8s, 1)

def enc_u16s(u16s):
    return enc_ints(u16s, 2)

def enc_u32s(u32s):
    return enc_ints(u32s, 4)

def enc_u64s(u64s):
    return enc_ints(u64s, 8)

def enc_i8s(i8s):
    return enc_ints(i8s, 1, signed=True)

def enc_i16s(i16s):
    return enc_ints(i16s, 2, signed=True)

def enc_i32s(i32s):
    return enc_ints(i32s, 4, signed=True)

def enc_i64s(i64s):
    return enc_ints(i64s, 8, signed=True)


def enc_ints(ints, size, signed=False):
    bytes = b""
    for i in ints:
        bytes += i.to_bytes(size, "little", signed=signed)
    return enc_bytes(bytes)

def enc_wstr(s):
    return enc_bytes(s.encode("utf-16-le") + b"\x00\x00")

def enc_str(s):
    return enc_bytes(s.encode() + b"\x00")

def enc_bytes(bs):
    k = gen_key(len(bs))
    return xor(bs, k), k

def gen_code(c_vars, filename):
    c_code = gen_c_code(c_vars, filename)
    h_code = gen_h_code(c_vars, filename)
    return h_code, c_code

def gen_h_code(c_vars, filename):
    code = []
    code.append("#ifndef _{}_H".format(filename.upper()))
    code.append("#define _{}_H".format(filename.upper()))
    code.append("#include <stddef.h>")
    code.append("#include <stdint.h>")
    code.append("")

    for v in c_vars:
        code.append(gen_var_h_code(v))
        code.append("")

    code.append("")
    code.append("#endif")
    code.append("")

    return "\n".join(code)

def gen_var_h_code(var):
    code = []
    c_type = type_to_c_type(var.type)

    code.append("#define SIZE_{}_{} {}".format(var.name, var.type, len(var.enc_value)))
    code.append("{} {}_{}_dec({} out);".format(c_type, var.name, var.type, c_type))

    return "\n".join(code)
    

def gen_c_code(c_vars, filename):
    code = []

    code.append('#include "{}.h"'.format(filename))
    code.append("\n")
    code.append(gen_xor_into_code())
    code.append("\n")
    
    for v in c_vars:
        code.append(gen_var_c_code(v))
        code.append("\n")

    return "\n".join(code)
        
    
def gen_var_c_code(var):
    lines = []
    enc_varname = "{}_{}_enc".format(var.name, var.type)
    key_varname = "{}_{}_key".format(var.name, var.type)
    c_value_array = bytes_to_c_array(var.enc_value)
    c_key_array = bytes_to_c_array(var.enc_key)
    c_type = type_to_c_type(var.type)
    
    lines.append("// {}".format(var.value))
    lines.append("const char {}[] = {};".format(enc_varname, c_value_array))
    lines.append("const char {}[] = {};".format(key_varname, c_key_array))

    lines.append("{} {}_{}_dec({} out) {{".format(c_type, var.name, var.type, c_type))
    lines.append("   return ({})xor_into((char*)out, {}, sizeof({}), {}, sizeof({}));".format(
        c_type, enc_varname, enc_varname, key_varname, key_varname
    ))
    lines.append("}")

    return "\n".join(lines)


def gen_xor_into_code():
    lines = []
    lines.append("static char* xor_into(char* out, const char* in, size_t in_size, const char* key, size_t key_size) {")
    lines.append("    size_t i = 0;")
    lines.append("    for(i = 0; i < key_size; i++) {")
    lines.append("        out[i] = in[i] ^ key[i % key_size];")
    lines.append("    }")
    lines.append("    return out;")
    lines.append("}")

    return "\n".join(lines)

def bytes_to_c_array(bs):
    return "{{{}}}".format(", ".join(["0x{:02x}".format(c) for c in bs]))

def xor(value, key):
    enc = []
    for i in range(len(value)):
        enc.append(value[i] ^ key[i % len(key)])
    return enc

c_types = {
    "bytes": "unsigned char*",
    "str": "char*",
    "wstr": "wchar_t*",
    "u8": "uint8_t*",
    "u16": "uint16_t*",
    "u32": "uint32_t*",
    "u64": "uint64_t*",
    "i8": "int8_t*",
    "i16": "int16_t*",
    "i32": "int32_t*",
    "i64": "int64_t*",
}

def type_to_c_type(t):
    try:
        return c_types[t]
    except KeyError:
        raise KeyError("Not found type {}".format(t))
    

Variable = namedtuple("Variable", [
    "type",
    "name",
    "value",
    "enc_value",
    "enc_key",
])


if __name__ == "__main__":
    exit(main())
