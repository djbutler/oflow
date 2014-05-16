**oflow**

Find code snippets on Stack Overflow with lightning speed.

```
Usage: oflow.py [options] query

Options:
  -h, --help        show this help message and exit
  -n N, --number=N  number of results to display

Searchs stackoverflow for questions matching QUERY, gets
all answers to these questions, prints code snippets 
from these answers.

Examples:

python oflow.py "how do i access mysql from python"
python oflow.py "python english dictionary"
python oflow.py "c++ lambda" -n 1
```

**Installing TextMate Bundle (OS X)**

1. Download TextMate 2 (http://macromates.com/download)
2. From the oflow directory, run "install_textmate_bundle.sh"

Now inside TextMate you can use selected text as a query to oflow by
pressing "CTRL+OPT+CMD+o"

