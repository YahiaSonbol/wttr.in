# Test Generator Instruction Manual

## Setup Instructions

1. **Create project directory**
    ```bash
    mkdir url-fuser
    ```

2. **Navigate to project directory**
    ```bash
    cd url-fuser
    ```

3. **Create Python generator file**
    ```bash
    touch urlGenerator.py
    ```

4. **Return to parent directory**
    ```bash
    cd ..
    ```

5. **Process grammar file**
    ```bash
    grammarinator-process url.g4 -o url-fuser/ --no-actions
    ```
    This command processes the ANTLR4 grammar file (`url.g4`) and generates the URL generator code in the `url-fuser/` directory without action code.

## Test Generation Instructions

6. **Navigate to project directory**
    ```bash
    cd url-fuser
    ```

7. **Create test cases output directory**
    ```bash
    mkdir test-cases
    ```

8. **Generate test cases**
    ```bash
    grammarinator-generate urlGenerator.urlGenerator -r url -d 20 -o test-cases/payload_%d.txt -n 20 --sys-path .
    ```
    
    **Parameters:**
    - `-r url`: Root rule for generation
    - `-d 20`: Maximum depth of 20 for recursive structures
    - `-o test-cases/payload_%d.txt`: Output file pattern for generated test cases
    - `-n 20`: Generate 20 test cases
    - `--sys-path .`: Add current directory to Python system path

**Result:** 20 generated URL payloads will be saved in the `test-cases/` directory as `payload_1.txt`, `payload_2.txt`, etc.