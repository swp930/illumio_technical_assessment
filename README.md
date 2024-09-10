# How to run 
```python main.py```

# How to test
```python -m unittest discover -s tests```
This test gets sample tag counts and the port protocol counts and checks if they 
match the expected output.

# High level description of the program
```main.py``` retrieves the lookup table based off a file name and protocol number to protocol string from the csv provided at https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml, and then reads through the flow logs. It then generates the tag frequency and the port combination frequency. 

# Assumptions and decisions made
The program only supports default log format and the only version that is supported is 2. It assumes that lookup csv files will have columns. For tags not found it will mark them as untagged.```main.py``` deletes the file if it exists and then writes to a newly created file. Also added a csv to go from port protocol decimal number to the string representation from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml. This program also creates separate files for the two requested output formats 