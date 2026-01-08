"""
印刷用のファイルを生成する
MarkDownの印刷はMacDownを使うと比較的まとも。

目次はどうしようかな。
印刷しないなら目次はVSCodeの拡張機能のメニューでいい。
目次はやめる。

表紙がない。
"""

import glob

for fname in sorted(glob.glob("[01]*.md")):
    with open(fname) as f:
        print(f.read())
