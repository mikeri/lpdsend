# lpdsend
Send print jobs (as stdin) via LPR/LPD from the command line. Does not use OS printer ports, so good for testing/diagnostics.

Does not use RFC specified source ports, but this should not be a problem for any known printers or servers.

## Usage
```
./lpdsend.py <printer ip> < <file to print>
```

### Examples
```
./lpdsend.py 192.168.0.20 < testpage.pdf
```
```
echo "This is a test" | ./lpdsend.py 10.10.10.35
```
