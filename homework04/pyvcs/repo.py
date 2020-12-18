import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    git_dir = os.environ.get("GIT_DIR", default=".pyvcs")
    dir = pathlib.Path(workdir)
    while str(dir.absolute()) != "/":
        if (dir / git_dir).exists():
            return dir / git_dir
        dir = dir.parent
    if (dir / git_dir).exists():
        return dir / git_dir
    raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    git_name = os.getenv("GIT_DIR", ".pyvcs")
    wrkpath = pathlib.Path(workdir)
    if wrkpath.is_file():
        raise Exception(f"{wrkpath} is not a directory")
    os.makedirs(wrkpath / git_name / "refs" / "heads", exist_ok=True)
    os.makedirs(wrkpath / git_name / "refs" / "tags", exist_ok=True)
    (workpath / git_name / "objects").mkdir()
    with (wrkpath / git_name / "config").open("w") as f:
        f.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
        )
    with (wrkpath / git_name / "HEAD").open("w") as f:
        f.write("ref: refs/heads/master\n")
    with (wrkpath / git_name / "description").open("w") as f:
        f.write("Unnamed pyvcs repository.\n")
    return workpath / git_name
