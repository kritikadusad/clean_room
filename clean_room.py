import os
import sys
import argparse
import logging
from collections import namedtuple

# Named tuple
Coordinate = namedtuple("Coordinate", "x, y")

# Hashmap of cardinal directions as keys
# and tuples of direction coordinates as values
DIRECTION_COORDINATES = {
    "N": Coordinate(0, 1),
    "S": Coordinate(0, -1),
    "E": Coordinate(1, 0),
    "W": Coordinate(-1, 0),
}


class Room:
    """
    A class to represent a session of cleaning the room using 
    a text file as input. 

    Args:
        input_filepath (str): filepath of a text file with input 
    
    """

    def __init__(self, input_filepath, log_level):

        """
        Updates attributes and raises error if 
        if input_filepath does not exist.

        Attributes:
            dust_coordinates (set): set with tuples of dust positions
            room_size (namedtuple): x and y coordinates of room
            (top right corner)
            directions (array): cardinal directions converted to coordinates
            num_dust_removed (int): initialized to zero. 
            current_position (namedtuple): x and y coordinates of the robot
            when it begins cleaning and during the exercise.
        """
        # 
        logging.basicConfig(format="%(levelname)s:%(message)s", level=log_level)

        if not os.path.exists(input_filepath):
            logging.error(
                f"{input_filepath} is incorrect. Please provide correct filepath"
            )
            raise FileNotFoundError(f"{input_filepath} is incorrect.") 

        self.dust_coordinates = set()
        self.directions = []
        self.num_dust_removed = 0
        self.process_input_file(input_filepath)
        logging.info(f"Input file - {input_filepath} has been processed")

    def process_input_file(self, input_filepath):

        """
        Processes the input in the text file 
        and updates class attributes:
        room_size, dust_set, directions, and start_position.

        Args:
            input_filepath (str): filepath of a text file with input 
        
        """

        with open(input_filepath) as f:
            count = 0
            lines = [line.strip() for line in f.readlines()]

            # first line should have room coordinates
            self.room_size = self.get_coordinates(lines[0])
            logging.info(f"Room coordinates are: {self.room_size}")

            # second line should have current position of robot
            self.current_position = self.get_coordinates(lines[1])
            if not self.is_valid_position(self.current_position):
                raise ValueError("Invalid start position")
            logging.info(
                f"Current position of roomba robot is: {self.current_position}"
            )

            # last line should have directions for the robot
            cardinal_directions = lines.pop().upper()
            for direction in cardinal_directions:
                try:
                    self.directions.append(DIRECTION_COORDINATES[direction])
                except KeyError:
                    logging.error(
                        f"Incorrect directions provided. Please check direction {direction} provided"
                    )
                    raise ValueError(f"Incorrect format of input")

            # remaining lines should have positions of dust
            dust_positions = lines[2:]
            for line_count, position in enumerate(dust_positions):
                dust_position = self.get_coordinates(position)
                if not self.is_valid_position(dust_position):
                    raise ValueError(
                        f"Please provide correct dust position at line - {line_count+2}"
                    )
                self.dust_coordinates.add(dust_position)

    def get_coordinates(self, line):
        """
        Processes input line by removing extra space
        and splitting into 2 ints.
        Args:
            line (str): from file
        Returns:
            Coordinate (namedtuple): with x and y as ints
        """
        line = line.split(" ")
        all_digits = all([char.isdigit() for char in line])
        if all_digits:
            if len(line) != 2:
                logging.error(f"Incorrect input provided")
                raise ValueError(f"Incorrect format of input")
        else:
            logging.error(f"Found wrong character")
            raise ValueError(f"Input should have a digit.")

        return Coordinate(x=int(line[0]), y=int(line[1]))

    def is_valid_position(self, position):
        """
        Returns boolean if position is valid
        A valid robot position is a position if it lies inside the room

        Args:
            position: namedtuple Coordinate     
        Return:
            boolean: True if position of dust is inside the room
        """
        return all(
            (0 <= position.x < self.room_size.x, 0 <= position.y < self.room_size.y)
        )

    def is_valid_dust_position(self, position):
        """
        Returns true if position of dust is valid
        Position of dust is valid if it lies inside the room
        and is not already added to set of dust particles 
        Args:
            position: tuple,     
        Return:
            boolean: True if position of dust is inside the room
        
        """
        self.is_valid_position(position) and position not in self.dust_coordinates

    def move_robot(self, direction):
        """
        New position of the robot is returned after adding the
        direction coordinates to the start position

        Args:
            direction: tuple, coordinates corresponding to cardinal direction
        Returns:
            StartPosition: namedtuple, with x and y coordinates of robot before 
            its direction is changed
        """
        new_x = self.current_position.x + direction.x
        new_y = self.current_position.y + direction.y
        if new_x < 0:
            new_x = 0
        elif new_x >= self.room_size.x:
            new_x = self.room_size.x - 1
        if new_y < 0:
            new_y = 0
        elif new_y >= self.room_size.y:
            new_y = self.room_size.y - 1
        return Coordinate(new_x, new_y)

    def clean(self):
        """
        Prints final position of robot after going through all
        directions sequentially and adding to dust removed 
        if dust present at start position.

        """
        for direction in self.directions:
            # check if dust present at start position
            # and increase number dust removed by 1.
            if self.current_position in self.dust_coordinates:
                self.num_dust_removed += 1
                self.dust_coordinates.remove(self.current_position)
                logging.info(
                    f"Found dust at position: ({self.current_position.x},{self.current_position.y}). Robot is removing it."
                )
            # update current position after robot has moved
            self.current_position = self.move_robot(direction)
            logging.info(
                f"Robot has moved to new position: ({self.current_position.x},{self.current_position.y})."
            )
        logging.info(
            f"Robot has finished following the directions and cleaning the room."
        )
        print(
            f"{self.current_position.x} {self.current_position.y}\n{self.num_dust_removed}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Program that uses an input from text file and cleans a room. The text file should include the-room dimensions, starting position of robot, positions of dust particles, and finally cardinal directions for the robot. This program returns final position of robot followed by  number of dust particles removed."
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        default="WARNING",
        help="Only output log messages of this severity or above. (default: %(default)s)",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="filepath of input text file. Default is input.txt",
        default="input.txt",
    ),
    args = parser.parse_args()

    room = Room(args.input, args.loglevel)
    room.clean()
