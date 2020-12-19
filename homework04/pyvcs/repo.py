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
    workdir = pathlib.Path(workdir)
    if workdir.is_file():
        raise Exception(f"{workdir} is not a directory")
    os.makedirs(workdir / git_name / "refs" / "heads", exist_ok=True)
    os.makedirs(workdir / git_name / "refs" / "tags", exist_ok=True)
    (workdir / git_name / "objects").mkdir()
    with (workdir / git_name / "config").open("w") as f:
        f.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
        )
    with (workdir / git_name / "HEAD").open("w") as f:
        f.write("ref: refs/heads/master\n")
    with (workdir / git_name / "description").open("w") as f:
        f.write("Unnamed pyvcs repository.\n")
    return workdir / git_name
