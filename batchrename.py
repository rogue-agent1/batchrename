#!/usr/bin/env python3
"""batchrename - Batch file renamer with patterns."""
import os, re, argparse, sys, time

def main():
    p = argparse.ArgumentParser(description='Batch file renamer')
    sub = p.add_subparsers(dest='cmd')
    
    rx = sub.add_parser('regex', help='Rename with regex')
    rx.add_argument('pattern', help='Search pattern')
    rx.add_argument('replacement', help='Replacement')
    rx.add_argument('files', nargs='+')
    rx.add_argument('--dry-run', action='store_true')
    
    seq = sub.add_parser('sequence', help='Sequential numbering')
    seq.add_argument('files', nargs='+')
    seq.add_argument('--prefix', default='')
    seq.add_argument('--start', type=int, default=1)
    seq.add_argument('--pad', type=int, default=3)
    seq.add_argument('--dry-run', action='store_true')
    
    ext = sub.add_parser('ext', help='Change extension')
    ext.add_argument('old_ext')
    ext.add_argument('new_ext')
    ext.add_argument('files', nargs='+')
    ext.add_argument('--dry-run', action='store_true')
    
    cs = sub.add_parser('case', help='Change case')
    cs.add_argument('mode', choices=['lower','upper','title','snake','kebab'])
    cs.add_argument('files', nargs='+')
    cs.add_argument('--dry-run', action='store_true')
    
    dt = sub.add_parser('date', help='Prepend date from mtime')
    dt.add_argument('files', nargs='+')
    dt.add_argument('--format', default='%Y%m%d')
    dt.add_argument('--dry-run', action='store_true')
    
    args = p.parse_args()
    if not args.cmd: p.print_help(); return
    
    renames = []
    
    if args.cmd == 'regex':
        for f in args.files:
            dirname, basename = os.path.dirname(f), os.path.basename(f)
            new_name = re.sub(args.pattern, args.replacement, basename)
            if new_name != basename:
                renames.append((f, os.path.join(dirname, new_name) if dirname else new_name))
    
    elif args.cmd == 'sequence':
        for i, f in enumerate(sorted(args.files), args.start):
            dirname, basename = os.path.dirname(f), os.path.basename(f)
            ext_part = os.path.splitext(basename)[1]
            new_name = f"{args.prefix}{str(i).zfill(args.pad)}{ext_part}"
            renames.append((f, os.path.join(dirname, new_name) if dirname else new_name))
    
    elif args.cmd == 'ext':
        for f in args.files:
            if f.endswith(f'.{args.old_ext}'):
                new = f[:-len(args.old_ext)] + args.new_ext
                renames.append((f, new))
    
    elif args.cmd == 'case':
        for f in args.files:
            dirname, basename = os.path.dirname(f), os.path.basename(f)
            name, ext = os.path.splitext(basename)
            if args.mode == 'lower': new = name.lower()
            elif args.mode == 'upper': new = name.upper()
            elif args.mode == 'title': new = name.title()
            elif args.mode == 'snake': new = re.sub(r'[\s-]+', '_', name).lower()
            elif args.mode == 'kebab': new = re.sub(r'[\s_]+', '-', name).lower()
            renames.append((f, os.path.join(dirname, new + ext) if dirname else new + ext))
    
    elif args.cmd == 'date':
        for f in args.files:
            dirname, basename = os.path.dirname(f), os.path.basename(f)
            mtime = os.path.getmtime(f)
            prefix = time.strftime(args.format, time.localtime(mtime))
            new = f"{prefix}_{basename}"
            renames.append((f, os.path.join(dirname, new) if dirname else new))
    
    if not renames:
        print("No files to rename."); return
    
    for old, new in renames:
        if args.dry_run:
            print(f"  {old} → {new}")
        else:
            os.rename(old, new)
            print(f"  {old} → {new}")
    
    print(f"\n{'Would rename' if args.dry_run else 'Renamed'} {len(renames)} files")

if __name__ == '__main__':
    main()
