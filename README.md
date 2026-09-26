# disk-cleaner

磁盘清理工具。扫描并清理临时文件、缓存、回收站等无用文件，**默认只扫描不删除**。

## 特色

- **默认安全**：只扫描并报告，不加 `--delete` 绝不删除
- 分类统计，看清每种垃圾占多少
- 支持自定义扫描目录
- 可设置最小文件大小、排除目录

## 用法

```bash
# 扫描系统常见垃圾目录（只报告）
python cleaner.py --scan

# 扫描指定目录
python cleaner.py --scan --path D:/temp

# 确认后删除（危险，需显式指定）
python cleaner.py --scan --delete

# 只处理大于 10MB 的文件
python cleaner.py --scan --min-size 10
```

## 参数

- `--scan`：执行扫描
- `--path`：指定目录（可多次）
- `--delete`：真的删除（默认关闭）
- `--min-size`：最小文件大小 MB
- `--days`：只清理 N 天前的文件
- `--exclude`：排除目录名，逗号分隔

## 警告

请**先用默认模式预览**，确认无误后再加 `--delete`。删除不可恢复。