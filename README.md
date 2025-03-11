# Custom Shell Implementation  

This project is a custom shell implementation designed to replicate basic shell functionality while supporting additional features like command execution, built-in commands, and autocompletion.  

---

## 🖥 Running the Shell  

To start the shell locally, use the provided script:

```sh
./your_program.sh
```

### 🔧 How It Works  
- The script sets up the execution environment using `pipenv`.  
- It ensures proper error handling (`set -e`).  
- The program is executed via Python using:  

```sh
pipenv run python3 -u -m app.main "$@"
```

---

## 🛠 Example Usage  

```sh
$ echo "Hello, world!"
Hello, world!

$ pwd
/home/user

$ cd /tmp
$ pwd
/tmp

$ type ls
ls is /bin/ls

$ exit 0
```

### 🔹 Output Redirection Example  

```sh
$ ls /tmp > /tmp/listing.txt
$ cat /tmp/listing.txt
file1.txt  file2.txt
```

---

## 🚀 Features Implemented  

### ✅ Command Execution  
- Executes system commands by searching for executables in `$PATH`.  
- Supports both built-in commands and external programs.  

### ✅ Built-in Commands  
- `echo <args>` → Prints arguments to stdout.  
- `exit <code>` → Exits the shell with the given status code.  
- `pwd` → Prints the current working directory.  
- `cd <dir>` → Changes the working directory (supports `~` for home).  
- `type <cmd>` → Identifies whether a command is a built-in or an external executable.  

### ✅ Input Parsing  
- Tokenizes user input while handling special cases like quotes and escape sequences.  
- Supports redirection (`>`, `1>`, `>>`, `2>` for stdout and stderr).  

### ✅ Output Redirection  
- Redirects output to specified files using `>`, `1>`, `>>` (append mode).  
- Redirects error output using `2>`.  

### ✅ Autocompletion  
- Pressing `<TAB>` autocompletes commands from:  
  - Built-in commands.  
  - Executables found in `$PATH`.  
- Displays multiple matches when ambiguous, restoring the original prompt afterward.  

---

## 🏗 Project Structure  

```
/app
├── constants.py    # Defines command constants
├── main.py         # Entry point of the shell
├── processor.py    # Handles command execution and parsing
├── utils.py        # Helper functions
```

---