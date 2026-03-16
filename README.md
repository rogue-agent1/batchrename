# batchrename
Batch file renamer: regex, sequential, extension, case, date prefix.
```bash
python batchrename.py regex "IMG_" "photo_" *.jpg --dry-run
python batchrename.py sequence *.png --prefix "slide_" --pad 2
python batchrename.py ext txt md *.txt
python batchrename.py case kebab *.py
python batchrename.py date *.jpg --format "%Y-%m-%d"
```
## Zero dependencies. Python 3.6+.
