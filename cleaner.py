#!/usr/bin/env python
"""磁盘清理工具（默认只扫描不删除）。"""

import argparse
import os
import shutil
import time
from pathlib import Path

DEFAULT_TARGETS = [
    os.path.expandvars(r"%TEMP%"),
    os.path.expandvars(r"%LOCALAPPDATA%\Temp"),
    os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\INetCache"),
    os.path.expandvars(r"%LOCALAPPDATA%\CrashDumps"),
]


def human(size: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}PB"


def scan(paths: list[str], min_size: int, days: int, excludes: set[str]) -> list[tuple[Path, int]]:
    found: list[tuple[Path, int]] = []
    cutoff = time.time() - days * 86400 if days else 0
    min_bytes = min_size * 1024 * 1024

    for base in paths:
        root = Path(base)
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root, topdown=True):
            dirnames[:] = [d for d in dirnames if d not in excludes]
            for name in filenames:
                fp = Path(dirpath) / name
                try:
                    st = fp.stat()
                except OSError:
                    continue
                if st.st_size < min_bytes:
                    continue
                if cutoff and st.st_mtime > cutoff:
                    continue
                found.append((fp, st.st_size))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description="磁盘清理（默认只扫描）")
    parser.add_argument("--scan", action="store_true", help="执行扫描")
    parser.add_argument("--path", action="append", help="指定目录，可多次")
    parser.add_argument("--delete", action="store_true", help="真的删除")
    parser.add_argument("--min-size", type=int, default=0, help="最小文件大小 MB")
    parser.add_argument("--days", type=int, default=0, help="只清理 N 天前的文件")
    parser.add_argument("--exclude", default="node_modules,.git", help="排除目录名")
    args = parser.parse_args()

    if not args.scan:
        parser.print_help()
        return 1

    paths = args.path if args.path else DEFAULT_TARGETS
    excludes = {e.strip() for e in args.exclude.split(",") if e.strip()}

    print("正在扫描...")
    files = scan(paths, args.min_size, args.days, excludes)

    if not files:
        print("没有找到需要清理的文件。")
        return 0

    total = sum(s for _, s in files)
    print(f"\n找到 {len(files)} 个文件，共 {human(total)}")
    for fp, size in sorted(files, key=lambda x: -x[1])[:20]:
        print(f"  {human(size):>10}  {fp}")
    if len(files) > 20:
        print(f"  ... 还有 {len(files) - 20} 个")

    if not args.delete:
        print("\n[预览模式] 未删除任何文件。确认后加 --delete 执行。")
        return 0

    removed = freed = 0
    for fp, size in files:
        try:
            fp.unlink()
            removed += 1
            freed += size
        except OSError:
            continue
    print(f"\n已删除 {removed} 个文件，释放 {human(freed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())