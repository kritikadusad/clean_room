import os
import io
import unittest
from unittest.mock import patch
from clean_room import Room

class TestRoom(unittest.TestCase):

    @patch("sys.stdout", new_callable=io.StringIO)
    def assert_stdout(self, input_filepath, loglevel,expected_output, mock_stdout):
        room = Room(input_filepath, loglevel)
        room.clean()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_process_input_filepath(self):
        self.assertRaises(ValueError, Room, "test_inputs/input_with_outside_start_position.txt", "CRITICAL")
        self.assertRaises(ValueError, Room, "test_inputs/input_with_incorrect_directions.txt", "CRITICAL")
        self.assertRaises(FileNotFoundError, Room, "test_inputs/file_does_not_exist", "CRITICAL")


    def test_incorrect_room_directions(self):
        self.assertRaises(ValueError, Room, "test_inputs/input_with_negative_room_directions.txt", "CRITICAL")
        self.assertRaises(ValueError, Room, "test_inputs/input_with_incorrect_room_directions.txt", "CRITICAL")
        self.assertRaises(ValueError, Room, "test_inputs/input_with_missing_room_directions.txt", "CRITICAL")

    def test_clean(self):
        self.assert_stdout("test_inputs/input_with_wall_bumping_directions.txt", "CRITICAL", "2 2\n1\n" )
        self.assert_stdout("test_inputs/input_with_wall_bumping_directions.txt", "CRITICAL", "2 2\n1\n" )
        self.assert_stdout("input.txt", "CRITICAL", "1 3\n1\n")



if __name__ == "__main__":
    unittest.main()
