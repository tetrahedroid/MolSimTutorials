#!/usr/bin/env python3
"""
Markdownファイルに埋め込まれたコードブロックを抽出して、
IPython notebook (.ipynb) に変換するスクリプト
"""

import sys
import re
import json
from pathlib import Path


def parse_markdown_to_notebook(md_content):
    """
    Markdownの内容を解析して、IPython notebook形式に変換する
    
    Args:
        md_content: Markdownファイルの内容（文字列）
    
    Returns:
        IPython notebook形式の辞書
    """
    cells = []
    lines = md_content.split('\n')
    i = 0
    
    current_markdown = []
    in_code_block = False
    current_code = []
    current_language = None
    
    while i < len(lines):
        line = lines[i]
        
        # コードブロックの終了を先に検出（開始と終了が同じ行の可能性を考慮）
        if in_code_block and line.strip() == '```':
            # コードセルを保存
            code_text = '\n'.join(current_code).strip()
            if code_text:
                # 言語に応じてセルタイプを決定
                if current_language in ['python', 'py']:
                    cells.append({
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {},
                        "outputs": [],
                        "source": code_text.split('\n')
                    })
                elif current_language in ['shell', 'bash', 'sh']:
                    # shellコマンドはマークダウンセルとして保存
                    cells.append({
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": [f"```{current_language}\n{code_text}\n```"]
                    })
                else:
                    # その他の言語もマークダウンセルとして保存
                    cells.append({
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": [f"```{current_language}\n{code_text}\n```"]
                    })
            
            in_code_block = False
            current_code = []
            current_language = None
            i += 1
            continue
        
        # コードブロックの開始を検出
        code_start = re.match(r'^```(\w+)?', line)
        if code_start and not in_code_block:
            # 前のマークダウンセルを保存
            if current_markdown:
                markdown_text = '\n'.join(current_markdown).strip()
                if markdown_text:
                    cells.append({
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": markdown_text.split('\n')
                    })
                current_markdown = []
            
            # コードブロック開始
            in_code_block = True
            current_language = code_start.group(1) or 'text'
            current_code = []
            i += 1
            continue
        
        # コードブロック内の行
        if in_code_block:
            current_code.append(line)
        else:
            # マークダウンの行
            current_markdown.append(line)
        
        i += 1
    
    # 最後のマークダウンセルを保存
    if current_markdown:
        markdown_text = '\n'.join(current_markdown).strip()
        if markdown_text:
            cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": markdown_text.split('\n')
            })
    
    # IPython notebook形式の構造を作成
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    return notebook


def convert_md_to_ipynb(md_path, output_path=None):
    """
    MarkdownファイルをIPython notebookに変換する
    
    Args:
        md_path: 入力Markdownファイルのパス
        output_path: 出力notebookファイルのパス（省略時は自動生成）
    """
    md_path = Path(md_path)
    
    if not md_path.exists():
        print(f"エラー: ファイルが見つかりません: {md_path}", file=sys.stderr)
        sys.exit(1)
    
    # Markdownファイルを読み込む
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # notebookに変換
    notebook = parse_markdown_to_notebook(md_content)
    
    # 出力パスを決定
    if output_path is None:
        output_path = md_path.with_suffix('.ipynb')
    else:
        output_path = Path(output_path)
    
    # notebookファイルを保存
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=2)
    
    print(f"変換完了: {md_path} -> {output_path}")


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python md_to_ipynb.py <markdown_file> [output_file]")
        print("例: python md_to_ipynb.py 04解析.md 04解析.ipynb")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_md_to_ipynb(md_file, output_file)


if __name__ == '__main__':
    main()
