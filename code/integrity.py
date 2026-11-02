"""Verify the sealed S1 file inventory without changing any files."""
import hashlib
import json
from pathlib import PurePosixPath


IGNORED_DIRS = {".git", "outputs", "__pycache__"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    found = []
    def visit(folder):
        for item in sorted(folder.iterdir()):
            if item.is_symlink():
                raise ValueError("Symlink is not allowed: " + str(item.relative_to(root)))
            if item.is_dir():
                if item.name not in IGNORED_DIRS:
                    visit(item)
            elif item.is_file():
                found.append(item.relative_to(root).as_posix())
            else:
                raise ValueError("Non-regular release entry")
    visit(root)
    return sorted(found)


def verify(root):
    manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1 or manifest.get("version") != "1.0.0":
        raise ValueError("Unexpected manifest schema/version")
    excluded = ["MANIFEST.json", "SHA256SUMS"]
    if manifest.get("manifest_hash_exclusions") != excluded:
        raise ValueError("Unexpected manifest exclusions")
    entries = manifest["files"]
    paths = [entry["path"] for entry in entries]
    if len(set(paths)) != len(paths) or set(paths).intersection(excluded):
        raise ValueError("Duplicate or reserved manifest path")
    for entry in entries:
        name = entry["path"]
        part = PurePosixPath(name)
        if part.is_absolute() or ".." in part.parts or "\\" in name or ":" in name:
            raise ValueError("Unsafe manifest path")
        target = root / name
        if target.stat().st_size != entry["bytes"] or digest(target) != entry["sha256"]:
            raise ValueError("Manifest checksum mismatch: " + name)
    expected = sorted(paths + excluded)
    if inventory(root) != expected:
        raise ValueError("Release inventory differs from MANIFEST.json")
    listed = (root / "FILE_LIST.txt").read_text(encoding="utf-8").splitlines()
    if listed != expected:
        raise ValueError("FILE_LIST.txt differs from actual release")
    sums = {}
    for line in (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        sha, name = line.split("  ", 1)
        if name in sums:
            raise ValueError("Duplicate checksum entry")
        sums[name] = sha
    if set(sums) != set(expected) - {"SHA256SUMS"}:
        raise ValueError("SHA256SUMS coverage mismatch")
    for name, sha in sums.items():
        if digest(root / name) != sha:
            raise ValueError("SHA256SUMS mismatch: " + name)
    return {"inventory_files": len(expected), "manifest_payload_files": len(entries),
            "sha256_entries": len(sums), "status": "PASS",
            "note": "Integrity consistency only; unsigned checksums do not establish authorship."}
