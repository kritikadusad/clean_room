# Simulation of hoover robot that cleans a room
This program `clean_room.py` takes an input file such as `input.txt` that should be in the same directory as the program.

## Requirements:
Python version 3.8  

## Directions:
Please clone this directory using the following command:  
`git clone https://github.com/kritikadusad/clean_room.git`

Once cloned, cd into the directory using the following command:  
`cd clean_room`

Once you are in the directory `clean_room`, please run the following command to run the program.  
`python3 clean_room.py`

The program uses `input.txt` file in the same directory as input.   

## Input

Program input will be received in a file with the format described here. 

Example:

```
5 5
1 2
1 0
2 2
2 3
NNESEESWNWW
```

* the first line holds the room dimensions (X Y), separated by a single space (all coordinates will be presented in this format)
* the second line holds the hoover position
* subsequent lines contain the zero or more positions of patches of dirt (one per line)
* the next line then always contains the driving instructions (at least one)

## Output
You should get the following output:  
```
1 3  
1
```

## Custom input/ loglevel

For more instructions, you can do the following:  
`python3 clean_room -h`

The program can take different input files by using the following command:  
`python3 clean_room.py -i <path_of_input_file>`  

You can also specifiy log levels as follows:  
`python3 clean_room -l INFO`  

## Tests
To run tests, please run the following command:  
`python3 test_clean_room.py`

The tests use input files from `test_inputs` directory



