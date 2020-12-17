import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    for pathway in paths:
        if pathway.is_file():
            update_index(gitdir, [pathway], write=True)
        if pathway.is_dir():
            add(gitdir, list(pathway.glob('*')))


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    root = resolve_head(gitdir)
    main = write_tree(gitdir, read_index(gitdir), str(gitdir.parent))
    docommit = commit_tree(gitdir, tree, message, parent, author)
    return docommit
 


