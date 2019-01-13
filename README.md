# lpdtest
Send print jobs (as stdin) via LPR/LPD from the command line. Does not use OS printer ports, so good for testing/diagnostics.

Does not use RFC specified source ports, but this should not be a problem for any known printers or servers.

## Usage
```
./lpdtest.py <printer ip> < <file to print>
```

### Examples
```
./lpdtest.py 192.168.0.20 < testpage.pdf
```
```
echo "This is a test" | ./lpdtest.py 10.10.10.35
```
