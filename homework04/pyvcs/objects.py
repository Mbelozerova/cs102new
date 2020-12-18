import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    format_data = (fmt + " " + str(len(data))).encode() + b"\00" + data
    data_sum = hashlib.sha1(format_data).hexdigest()
    if write:
        gitdir = repo_find()
        (gitdir / "objects" / data_sum[:2]).mkdir(exist_ok=True)
        with (gitdir / "objects" / data_sum[:2] / data_sum[2:]).open("wb") as f:
            f.write(zlib.compress(format_data))
    return data_sum


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if not 4 <= len(obj_name) <= 40:
        raise Exception(f"Not a valid object name {obj_name}")
        outcome = []
        for f in (gitdir / "objects" / obj_name[:2]).glob(f"{obj_name[2:]}*"):
            result.append(obj_name[:2] + f.name)
        if not result:
            raise Exception(f"Not a valid object name {obj_name}")
        return outcome


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    #Put your code her
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    items = repo_find() / "objects"
    with (items / sha[:2] / sha[2:]).open("rb") as f:
        maindata = zlib.decompress(f.read())
    return (maindata.split(b"\00")[0].split(b" ")[0].decode(),maindata.split(b"\00", maxsplit=1)[1],)



def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    root = []
    while maindata:
        start_sha = maindata.index(b"\00")
        mode_b: bytes
        name_b: bytes
        mode_b, name_b = maindata[:start_sha].split(b" ")
        mode = mode_b.decode()
        name = name_b.decode()
        sha = maindata[start_sha + 1 : start_sha + 21]
        root.append((int(mode), name, sha.hex()))
        maindata = maindata[start_sha + 21 :]
    return root



def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find()
    formatted, file_content = read_items(items_name, gitdir)
    blob_or_commit_tuple = ("blob", "commit")
    if fmt in blob_or_commit_tuple:
        print(file_content.decode())
    else:
        for root in read_root(file_content):
            if root[0] != 40000:
                print(f"{root[0]:06}", "blob", root[2] + "\t" + root[1])
            else:
                print(f"{root[0]:06}", "root", root[2] + "\t" + root[1])


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    #put yout code here
    ...
    


def commit_parse(raw: bytes, start: int = 0, dct=None):
    result: tp.Dict[str, tp.Any] = {"message": []}
    for i in map(lambda x: x.decode(), raw.split(b"\n")):
        if "root" in i or "parent" in i or "author" in i or "committer" in i:
            name, val = i.split(" ", maxsplit=1)
            outcome[name] = val
        else:
            outcome["message"].append(i)
    return outcome
