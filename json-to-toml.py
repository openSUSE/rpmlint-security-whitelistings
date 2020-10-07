#!/usr/bin/env python3

import argparse
import json
import pathlib

import toml

def convert(path):
    with path.open(encoding="utf-8") as f:
        d = json.load(f)
    out = []
    first = True

    expected_parse = {}

    for package, audits in d.items():
        if first:
            first = False
        else:
            out.append("")
            out.append("")
        out.append(f"[{package}]")

        expected_parse[package] = {}

        assert audits.keys() == {'audits'}, "unhandled keys in JSON"
        for bug, info in audits['audits'].items():
            expected_parse[package][bug] = info

            # remove comment, so that expected_parse doesn't contain comments and the next()-thing below works
            comment = info.pop('comment', None)

            assert (info.keys() == {'meta'} or info.keys() == {'digests'}), \
                    f"unhandled keys {info.keys()} in JSON"

            name, data = next(iter(info.items()))
            out.append(f'    [{package}.{repr(bug)}.{name}]')
            if comment:
                out.append(f"        # {comment}")

            for mpath, val in data.items():
                if isinstance(val, dict):
                    val = "{ " + ", ".join(f"{key} = {repr(val)}" for key, val in val.items()) + " }"
                elif isinstance(val, str):
                    val = repr(val)
                else:
                    assert False, "unknown type"
                out.append(f'        {repr(mpath)} = {val}')

    # make sure the TOML isn't invalid
    t = toml.loads("\n".join(out))
    assert expected_parse == t

    with path.with_suffix(".toml").open("w", encoding="utf-8") as f:
        f.write("\n".join(out))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description="TOML Converter")
    p.add_argument("files", metavar="FILE", nargs='+',
                   help="JSON files to convert. TOML output files will be in the same location with .toml suffix.")
    args = p.parse_args()

    for fname in args.files:
        convert(pathlib.Path(fname))
