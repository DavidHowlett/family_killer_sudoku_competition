#import unittest
import pytest
import time
#import dad_solver

#rules that we follow
#ruleof1: If a value is known, it can be excluded from the row, column, xet and cage that contain it.

board=[511]*81  #given a digit count and decimal number, what bits _might_ be used to make that total?
binarytodecimal= [0, 1, 2, 3, 3, 4, 5, 6, 4, 5, 6, 7, 7, 8, 9, 10, 5, 6, 7, 8, 8, 9, 10, 11, 9, 10, 11, 12, 12, 13, 14,
                  15, 6, 7, 8, 9, 9, 10, 11, 12, 10, 11, 12, 13, 13, 14, 15, 16, 11, 12, 13, 14, 14, 15, 16, 17, 15, 16,
                  17, 18, 18, 19, 20, 21, 7, 8, 9, 10, 10, 11, 12, 13, 11, 12, 13, 14, 14, 15, 16, 17, 12, 13, 14, 15,
                  15, 16, 17, 18, 16, 17, 18, 19, 19, 20, 21, 22, 13, 14, 15, 16, 16, 17, 18, 19, 17, 18, 19, 20, 20,
                  21, 22, 23, 18, 19, 20, 21, 21, 22, 23, 24, 22, 23, 24, 25, 25, 26, 27, 28, 8, 9, 10, 11, 11, 12, 13,
                  14, 12, 13, 14, 15, 15, 16, 17, 18, 13, 14, 15, 16, 16, 17, 18, 19, 17, 18, 19, 20, 20, 21, 22, 23,
                  14, 15, 16, 17, 17, 18, 19, 20, 18, 19, 20, 21, 21, 22, 23, 24, 19, 20, 21, 22, 22, 23, 24, 25, 23,
                  24, 25, 26, 26, 27, 28, 29, 15, 16, 17, 18, 18, 19, 20, 21, 19, 20, 21, 22, 22, 23, 24, 25, 20, 21,
                  22, 23, 23, 24, 25, 26, 24, 25, 26, 27, 27, 28, 29, 30, 21, 22, 23, 24, 24, 25, 26, 27, 25, 26, 27,
                  28, 28, 29, 30, 31, 26, 27, 28, 29, 29, 30, 31, 32, 30, 31, 32, 33, 33, 34, 35, 36, 9, 10, 11, 12,
                  12, 13, 14, 15, 13, 14, 15, 16, 16, 17, 18, 19, 14, 15, 16, 17, 17, 18, 19, 20, 18, 19, 20, 21, 21,
                  22, 23, 24, 15, 16, 17, 18, 18, 19, 20, 21, 19, 20, 21, 22, 22, 23, 24, 25, 20, 21, 22, 23, 23, 24,
                  25, 26, 24, 25, 26, 27, 27, 28, 29, 30, 16, 17, 18, 19, 19, 20, 21, 22, 20, 21, 22, 23, 23, 24, 25,
                  26, 21, 22, 23, 24, 24, 25, 26, 27, 25, 26, 27, 28, 28, 29, 30, 31, 22, 23, 24, 25, 25, 26, 27, 28,
                  26, 27, 28, 29, 29, 30, 31, 32, 27, 28, 29, 30, 30, 31, 32, 33, 31, 32, 33, 34, 34, 35, 36, 37, 17,
                  18, 19, 20, 20, 21, 22, 23, 21, 22, 23, 24, 24, 25, 26, 27, 22, 23, 24, 25, 25, 26, 27, 28, 26, 27,
                  28, 29, 29, 30, 31, 32, 23, 24, 25, 26, 26, 27, 28, 29, 27, 28, 29, 30, 30, 31, 32, 33, 28, 29, 30,
                  31, 31, 32, 33, 34, 32, 33, 34, 35, 35, 36, 37, 38, 24, 25, 26, 27, 27, 28, 29, 30, 28, 29, 30, 31,
                  31, 32, 33, 34, 29, 30, 31, 32, 32, 33, 34, 35, 33, 34, 35, 36, 36, 37, 38, 39, 30, 31, 32, 33, 33,
                  34, 35, 36, 34, 35, 36, 37, 37, 38, 39, 40, 35, 36, 37, 38, 38, 39, 40, 41, 39, 40, 41, 42, 42, 43, 44, 45]
decimaltobinary= [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 3, 5, 15, 27, 63, 119, 255, 495, 510, 476, 504, 432, 480, 320, 384, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 7, 11, 31, 63, 127, 255, 511, 511, 511, 511, 511, 511, 511, 510, 508, 504, 496, 416, 448, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 23, 63, 127, 255, 511, 511, 511, 511, 511, 511, 511, 511, 511, 511, 511, 510, 508, 504, 464, 480, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 47, 127, 255, 511, 511, 511, 511, 511, 511, 511, 511, 511, 511, 511, 511, 511, 510, 508, 488, 496, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 63, 95, 255, 511, 511, 511, 511, 511, 511, 511, 511, 511, 511, 511, 511, 511, 510, 500, 504, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 127, 191, 511, 511, 511, 511, 511, 511, 511, 511, 511, 511, 511, 506, 508, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 383, 447, 479, 495, 503, 507, 509, 510, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 511]]
popcount       = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 1, 2,
                  2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 1, 2, 2, 3,
                  2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3, 4,
                  4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 1, 2, 2, 3, 2, 3, 3, 4,
                  2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4,
                  4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5,
                  4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6,
                  6, 7, 4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
                  2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4,
                  4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5,
                  4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 4, 5, 5, 6, 5, 6,
                  6, 7, 5, 6, 6, 7, 6, 7, 7, 8, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6,
                  4, 5, 5, 6, 5, 6, 6, 7, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 4, 5, 5, 6, 5, 6, 6, 7, 5, 6,
                  6, 7, 6, 7, 7, 8, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7,
                  6, 7, 7, 8, 4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8, 5, 6, 6, 7, 6, 7, 7, 8, 6, 7, 7, 8, 7, 8, 8, 9]
binarytodisplay= ['          ', '         1', '        2 ', '        21', '       3  ', '       3 1', '       32 ', '       321', '      4   ', '      4  1', '      4 2 ', '      4 21', '      43  ', '      43 1', '      432 ', '      4321', '     5    ', '     5   1', '     5  2 ', '     5  21', '     5 3  ', '     5 3 1', '     5 32 ', '     5 321', '     54   ', '     54  1', '     54 2 ', '     54 21', '     543  ', '     543 1', '     5432 ', '     54321', '    6     ', '    6    1', '    6   2 ', '    6   21', '    6  3  ', '    6  3 1', '    6  32 ', '    6  321', '    6 4   ', '    6 4  1', '    6 4 2 ', '    6 4 21', '    6 43  ', '    6 43 1', '    6 432 ', '    6 4321', '    65    ', '    65   1', '    65  2 ', '    65  21', '    65 3  ', '    65 3 1', '    65 32 ', '    65 321', '    654   ', '    654  1', '    654 2 ', '    654 21', '    6543  ', '    6543 1', '    65432 ', '    654321', '   7      ', '   7     1', '   7    2 ', '   7    21', '   7   3  ', '   7   3 1', '   7   32 ', '   7   321', '   7  4   ', '   7  4  1', '   7  4 2 ', '   7  4 21', '   7  43  ', '   7  43 1', '   7  432 ', '   7  4321', '   7 5    ', '   7 5   1', '   7 5  2 ', '   7 5  21', '   7 5 3  ', '   7 5 3 1', '   7 5 32 ', '   7 5 321', '   7 54   ', '   7 54  1', '   7 54 2 ', '   7 54 21', '   7 543  ', '   7 543 1', '   7 5432 ', '   7 54321', '   76     ', '   76    1', '   76   2 ', '   76   21', '   76  3  ', '   76  3 1', '   76  32 ', '   76  321', '   76 4   ', '   76 4  1', '   76 4 2 ', '   76 4 21', '   76 43  ', '   76 43 1', '   76 432 ', '   76 4321', '   765    ', '   765   1', '   765  2 ', '   765  21', '   765 3  ', '   765 3 1', '   765 32 ', '   765 321', '   7654   ', '   7654  1', '   7654 2 ', '   7654 21', '   76543  ', '   76543 1', '   765432 ', '   7654321', '  8       ', '  8      1', '  8     2 ', '  8     21', '  8    3  ', '  8    3 1', '  8    32 ', '  8    321', '  8   4   ', '  8   4  1', '  8   4 2 ', '  8   4 21', '  8   43  ', '  8   43 1', '  8   432 ', '  8   4321', '  8  5    ', '  8  5   1', '  8  5  2 ', '  8  5  21', '  8  5 3  ', '  8  5 3 1', '  8  5 32 ', '  8  5 321', '  8  54   ', '  8  54  1', '  8  54 2 ', '  8  54 21', '  8  543  ', '  8  543 1', '  8  5432 ', '  8  54321', '  8 6     ', '  8 6    1', '  8 6   2 ', '  8 6   21', '  8 6  3  ', '  8 6  3 1', '  8 6  32 ', '  8 6  321', '  8 6 4   ', '  8 6 4  1', '  8 6 4 2 ', '  8 6 4 21', '  8 6 43  ', '  8 6 43 1', '  8 6 432 ', '  8 6 4321', '  8 65    ', '  8 65   1', '  8 65  2 ', '  8 65  21', '  8 65 3  ', '  8 65 3 1', '  8 65 32 ', '  8 65 321', '  8 654   ', '  8 654  1', '  8 654 2 ', '  8 654 21', '  8 6543  ', '  8 6543 1', '  8 65432 ', '  8 654321', '  87      ', '  87     1', '  87    2 ', '  87    21', '  87   3  ', '  87   3 1', '  87   32 ', '  87   321', '  87  4   ', '  87  4  1', '  87  4 2 ', '  87  4 21', '  87  43  ', '  87  43 1', '  87  432 ', '  87  4321', '  87 5    ', '  87 5   1', '  87 5  2 ', '  87 5  21', '  87 5 3  ', '  87 5 3 1', '  87 5 32 ', '  87 5 321', '  87 54   ', '  87 54  1', '  87 54 2 ', '  87 54 21', '  87 543  ', '  87 543 1', '  87 5432 ', '  87 54321', '  876     ', '  876    1', '  876   2 ', '  876   21', '  876  3  ', '  876  3 1', '  876  32 ', '  876  321', '  876 4   ', '  876 4  1', '  876 4 2 ', '  876 4 21', '  876 43  ', '  876 43 1', '  876 432 ', '  876 4321', '  8765    ', '  8765   1', '  8765  2 ', '  8765  21', '  8765 3  ', '  8765 3 1', '  8765 32 ', '  8765 321', '  87654   ', '  87654  1', '  87654 2 ', '  87654 21', '  876543  ', '  876543 1', '  8765432 ', '  87654321', ' 9        ', ' 9       1', ' 9      2 ', ' 9      21', ' 9     3  ', ' 9     3 1', ' 9     32 ', ' 9     321', ' 9    4   ', ' 9    4  1', ' 9    4 2 ', ' 9    4 21', ' 9    43  ', ' 9    43 1', ' 9    432 ', ' 9    4321', ' 9   5    ', ' 9   5   1', ' 9   5  2 ', ' 9   5  21', ' 9   5 3  ', ' 9   5 3 1', ' 9   5 32 ', ' 9   5 321', ' 9   54   ', ' 9   54  1', ' 9   54 2 ', ' 9   54 21', ' 9   543  ', ' 9   543 1', ' 9   5432 ', ' 9   54321', ' 9  6     ', ' 9  6    1', ' 9  6   2 ', ' 9  6   21', ' 9  6  3  ', ' 9  6  3 1', ' 9  6  32 ', ' 9  6  321', ' 9  6 4   ', ' 9  6 4  1', ' 9  6 4 2 ', ' 9  6 4 21', ' 9  6 43  ', ' 9  6 43 1', ' 9  6 432 ', ' 9  6 4321', ' 9  65    ', ' 9  65   1', ' 9  65  2 ', ' 9  65  21', ' 9  65 3  ', ' 9  65 3 1', ' 9  65 32 ', ' 9  65 321', ' 9  654   ', ' 9  654  1', ' 9  654 2 ', ' 9  654 21', ' 9  6543  ', ' 9  6543 1', ' 9  65432 ', ' 9  654321', ' 9 7      ', ' 9 7     1', ' 9 7    2 ', ' 9 7    21', ' 9 7   3  ', ' 9 7   3 1', ' 9 7   32 ', ' 9 7   321', ' 9 7  4   ', ' 9 7  4  1', ' 9 7  4 2 ', ' 9 7  4 21', ' 9 7  43  ', ' 9 7  43 1', ' 9 7  432 ', ' 9 7  4321', ' 9 7 5    ', ' 9 7 5   1', ' 9 7 5  2 ', ' 9 7 5  21', ' 9 7 5 3  ', ' 9 7 5 3 1', ' 9 7 5 32 ', ' 9 7 5 321', ' 9 7 54   ', ' 9 7 54  1', ' 9 7 54 2 ', ' 9 7 54 21', ' 9 7 543  ', ' 9 7 543 1', ' 9 7 5432 ', ' 9 7 54321', ' 9 76     ', ' 9 76    1', ' 9 76   2 ', ' 9 76   21', ' 9 76  3  ', ' 9 76  3 1', ' 9 76  32 ', ' 9 76  321', ' 9 76 4   ', ' 9 76 4  1', ' 9 76 4 2 ', ' 9 76 4 21', ' 9 76 43  ', ' 9 76 43 1', ' 9 76 432 ', ' 9 76 4321', ' 9 765    ', ' 9 765   1', ' 9 765  2 ', ' 9 765  21', ' 9 765 3  ', ' 9 765 3 1', ' 9 765 32 ', ' 9 765 321', ' 9 7654   ', ' 9 7654  1', ' 9 7654 2 ', ' 9 7654 21', ' 9 76543  ', ' 9 76543 1', ' 9 765432 ', ' 9 7654321', ' 98       ', ' 98      1', ' 98     2 ', ' 98     21', ' 98    3  ', ' 98    3 1', ' 98    32 ', ' 98    321', ' 98   4   ', ' 98   4  1', ' 98   4 2 ', ' 98   4 21', ' 98   43  ', ' 98   43 1', ' 98   432 ', ' 98   4321', ' 98  5    ', ' 98  5   1', ' 98  5  2 ', ' 98  5  21', ' 98  5 3  ', ' 98  5 3 1', ' 98  5 32 ', ' 98  5 321', ' 98  54   ', ' 98  54  1', ' 98  54 2 ', ' 98  54 21', ' 98  543  ', ' 98  543 1', ' 98  5432 ', ' 98  54321', ' 98 6     ', ' 98 6    1', ' 98 6   2 ', ' 98 6   21', ' 98 6  3  ', ' 98 6  3 1', ' 98 6  32 ', ' 98 6  321', ' 98 6 4   ', ' 98 6 4  1', ' 98 6 4 2 ', ' 98 6 4 21', ' 98 6 43  ', ' 98 6 43 1', ' 98 6 432 ', ' 98 6 4321', ' 98 65    ', ' 98 65   1', ' 98 65  2 ', ' 98 65  21', ' 98 65 3  ', ' 98 65 3 1', ' 98 65 32 ', ' 98 65 321', ' 98 654   ', ' 98 654  1', ' 98 654 2 ', ' 98 654 21', ' 98 6543  ', ' 98 6543 1', ' 98 65432 ', ' 98 654321', ' 987      ', ' 987     1', ' 987    2 ', ' 987    21', ' 987   3  ', ' 987   3 1', ' 987   32 ', ' 987   321', ' 987  4   ', ' 987  4  1', ' 987  4 2 ', ' 987  4 21', ' 987  43  ', ' 987  43 1', ' 987  432 ', ' 987  4321', ' 987 5    ', ' 987 5   1', ' 987 5  2 ', ' 987 5  21', ' 987 5 3  ', ' 987 5 3 1', ' 987 5 32 ', ' 987 5 321', ' 987 54   ', ' 987 54  1', ' 987 54 2 ', ' 987 54 21', ' 987 543  ', ' 987 543 1', ' 987 5432 ', ' 987 54321', ' 9876     ', ' 9876    1', ' 9876   2 ', ' 9876   21', ' 9876  3  ', ' 9876  3 1', ' 9876  32 ', ' 9876  321', ' 9876 4   ', ' 9876 4  1', ' 9876 4 2 ', ' 9876 4 21', ' 9876 43  ', ' 9876 43 1', ' 9876 432 ', ' 9876 4321', ' 98765    ', ' 98765   1', ' 98765  2 ', ' 98765  21', ' 98765 3  ', ' 98765 3 1', ' 98765 32 ', ' 98765 321', ' 987654   ', ' 987654  1', ' 987654 2 ', ' 987654 21', ' 9876543  ', ' 9876543 1', ' 98765432 ', ' 987654321']
todo           =set(['r0','r1','r2','r3','r4','r5','r6','r7','r8','c0','c1','c2','c3','c4','c5','c6','c7','c8','b0','b1','b2','b3','b4','b5','b6','b7','b8'])   #All the rows, columns and xetes that need to be processed

#The "xets" data allows me to treat every set (rows, columns, xets and cages) in the same way with the same code.
#"xet" and "xets" instead of "set" and "sets" to prevent clashes with the word "set"
xets           =[[ 0,  1,  2,  3,  4,  5,  6,  7,  8],  #Row data
                 [ 9, 10, 11, 12, 13, 14, 15, 16, 17],
                 [18, 19, 20, 21, 22, 23, 24, 25, 26],
                 [27, 28, 29, 30, 31, 32, 33, 34, 35],
                 [36, 37, 38, 39, 40, 41, 42, 43, 44],
                 [45, 46, 47, 48, 49, 50, 51, 52, 53],
                 [54, 55, 56, 57, 58, 59, 60, 61, 62],
                 [63, 64, 65, 66, 67, 68, 69, 70, 71],
                 [72, 73, 74, 75, 76, 77, 78, 79, 80],
                 [ 0,  9, 18, 27, 36, 45, 54, 63, 72],  #Column data
                 [ 1, 10, 19, 28, 37, 46, 55, 64, 73],
                 [ 2, 11, 20, 29, 38, 47, 56, 65, 74],
                 [ 3, 12, 21, 30, 39, 48, 57, 66, 75],
                 [ 4, 13, 22, 31, 40, 49, 58, 67, 76],
                 [ 5, 14, 23, 32, 41, 50, 59, 68, 77],
                 [ 6, 15, 24, 33, 42, 51, 60, 69, 78],
                 [ 7, 16, 25, 34, 43, 52, 61, 70, 79],
                 [ 8, 17, 26, 35, 44, 53, 62, 71, 80],
                 [ 0,  1,  2,  9, 10, 11, 18, 19, 20],  #Nonet data
                 [ 3,  4,  5, 12, 13, 14, 21, 22, 23],
                 [ 6,  7,  8, 15, 16, 17, 24, 25, 26],
                 [27, 28, 29, 36, 37, 38, 45, 46, 47],
                 [30, 31, 32, 39, 40, 41, 48, 49, 50],
                 [33, 34, 35, 42, 43, 44, 51, 52, 53],
                 [54, 55, 56, 63, 64, 65, 72, 73, 74],
                 [57, 58, 59, 66, 67, 68, 75, 76, 77],
                 [60, 61, 62, 69, 70, 71, 78, 79, 80]]

#***********************************************************************************************************************
def print_board():
# Function to display the board as-is, where LHS is only definite values, rhs is possible values
#For example:
#1 . . . . . . 2 .          1  987654321  987654321  987654321  987654321  987654321     6 4321         2   987654321
#. . . . . 3 . . .  987654321   8     2   987654321  987654321  987654321        3      7 5  2   987654321  987654321
#. . . 4 . . . . .  98765  2   987654321  9 7 5           4     987654321  987654321  987654321  987654321  987654321
#. 5 . . . 6 . . .  987 54321      5      987654321  987654321  9 7     1     6       987654321  987654321  987654321
#. . . . . . . . .  987654321  987654321  987654321       43    987654321  987654321  9  6 4321  987654321  987654321
#. . . . 7 . . 8 9  987654321  987654321  987654321  987654321    7        987654321  987654321   8         9
#. . . . . . . . 2  987654321  987654321  987654321  987654321  987654321  98  54 21  987654321  987654321         2
#. 3 . . . . . . .  987654321        3    987654321  987654321  98   4  1  987654321  987654321  987654321  987654321
#. . . . . . . . 1  987654321  987654321  987654321  987654321   87 54321  987654321  987654321  987654321          1
#***********************************************************************************************************************
    for row in range(9):
        rowbase=row*9
        #Left hand show of known cells
        for col in range(9):
            cellno=rowbase+col;
            if popcount[board[cellno]]<=1:
                print(binarytodecimal[board[cellno]],end=' ')
            else:
                print('. ',end='')
        #right hand view of possible values
        for col in range(9):
            cellno=rowbase+col;
            print(binarytodisplay[board[cellno]],end=' ')

        print()
    print("BoardPopcount(board)= ",boardpopcount(board))

def resetboard(n):
    # clear the board down to fully unknown
    for i in range(0,81):
        board[i]=n;

def boardpopcount(board):
    #Get the popcount for the entire board
    total=0
    for i in range(0,81):
        total=total+popcount[board[i]]
    return total

def ruleof1xet(xet): #Eliminate possibles from other cells where one cell in that set is definitely known.
    #print("ruleof1xet(",n,")")

    singles=0  #We know no values for sure
    for cellno in xet:  # Look at every cell for single values
        if popcount[board[cellno]]==1:
            singles=singles | board[cellno]         #Just in case we have an error with 2 cells having the same value. Avoid the error getting more complicated!
    notsingles=511-singles    #Find every unknown value
    for cellno in xet: #Look at every cell for single values
        if popcount[board[cellno]]!=1:
            board[cellno]=board[cellno] & notsingles  #Wipe out the values we clearly know

def ruleof2xet(xet): #Eliminate possibles where a cellpair in that set are definitely known.
    #for example:         3 1  987654321  987654321
    #               987654321        3 1  987654321
    #               987654321  987654321  987654321
    #should result in 3 & 1 being removed from the rest of the xet:
    #for example:         3 1  987654 2   987654 2
    #               987654 2         3 1  987654 2
    #               987654 2   987654 2   987654 2
    #    print("ruleof2xet(",n,")")
    #print_board()
    for n1 in range(0,len(xet)-1):                         #Compare every cell on the row
        cell1=board[xet[n1]]
        if popcount[cell1]<=2:                               #Performance: Don't bother if more than 2 digits already
            #print("popcount[cell]=", popcount[cell1])
            for n2 in range(n1+1,len(xet)):                  #with every other cell on the row
                cell2=board[xet[n2]]
                #if n2==4:
                    #print("A: n1=", n1, ",n2=", n2, "cell1=", cell1, "cell2=", cell2)
                if popcount[cell1 | cell2] < 2:  # and if only 3 digits are set then...
                    print("ERROR: Too few digits in ruleof2xet")
                    x = 1 / 0
                if popcount[cell1 | cell2] == 2:  # and if only 2 digits are set then...
                    #print("B: n1=", n1, ",n2=", n2, "cell1=", cell1, "cell2=", cell2)
                    #print("Match")
                    notthis=511-(cell1 | cell2);        #The inverse of this value
                    for nn in range(0,len(xet)):         #Look through every cell on the xet
                        if (nn!=n1) and (nn!=n2): #If the cell is not one that we are pointing at right now:
                            board[xet[nn]]=board[xet[nn]] & notthis #Strip these digits
                            #print("C: n1=", n1, ",n2=", n2, ", nn=",nn,", cell1=", cell1, ", cell2=", cell2, ", notthis=", notthis)

def ruleof3xet(xet): #Eliminate possibles where a celltriple in that set are definitely known.
    #for example:      6  3 1  987654321  987654321
    #               987654321     6  3 1  987654321
    #                  6  3 1  987654321  987654321
    #should result in 3 & 1 being removed from the rest of the xet:
    #for example:      6  3 1  987 54 2   987 54 2
    #               987 54 2      6  3 1  987 54 2
    #                  6  3 1  987 54 2   987 54 2
    #    print("ruleof3xet(",y,")")
    for n1 in range(0,len(xet)-2):                         #Compare every cell on the row
        cell1 = board[xet[n1]]  # What is in this cell?
        if popcount[cell1] <= 3:  # and if only 3 digits are set then...
            for n2 in range(n1+1,len(xet)-1):                  #with every other cell on the row
                cell2 = board[xet[n2]]  # What is in this cell?
                if popcount[cell1 | cell2] <= 3:  # and if only 3 digits are set then...
                    for n3 in range(n2 + 1, len(xet)):           # with every other cell on the row
                        cell3 = board[xet[n3]]  # What is in this cell?
                        if popcount[cell1 | cell2 | cell3] < 3:  # and if only 3 digits are set then...
                            print("ERROR: Too few digits in ruleof3xet")
                            x=1/0
                        if popcount[cell1 | cell2 | cell3] == 3:  # and if only 3 digits are set then...
                            #print("n1=",n1,", n2=",n2,", n3=",n3)  #display where we are
                            #print("Match")
                            notthis=511-(cell1 | cell2 | cell3);        #The inverse of this value
                            for nn in range(0,len(xet)):          #Look through every cell on the xet
                                if (nn!=n1) and (nn!=n2) and (nn!=n3): #If the cell is not one that we are pointing at right now:
                                    board[xet[nn]]=board[xet[nn]] & notthis #Strip these digits
                                    #nn=nn+0

def ruleof4xet(xet): #Eliminate possibles where a cellquad in that set are definitely known.
    #for example:   9  6  3 1  987654321  987654321
    #               987654321  9  6  3 1  987654321
    #               9  6  3 1  987654321  987654321
    #should result in 3 & 1 being removed from the rest of the xet:
    #for example:   9  6  3 1   87 54 2    87 54 2
    #                87 54 2   9  6  3 1   87 54 2
    #               9  6  3 1   87 54 2    87 54 2
    #    print("ruleof4xet(",y,")")
    for n1 in range(0,len(xet)-3):                         #Compare every cell on the row
        cell1 = board[xet[n1]]  # What is in this cell?
        if popcount[cell1] <= 4:  # and if only 4 digits are set then...
            for n2 in range(n1+1,len(xet)-2):                  #with every other cell on the row
                cell2 = board[xet[n2]]  # What is in this cell?
                if popcount[cell1 | cell2] <= 4:  # and if only 4 digits are set then...
                    for n3 in range(n2 + 1, len(xet)-1):           # with every other cell on the row
                        cell3 = board[xet[n3]]  # What is in this cell?
                        if popcount[cell1 | cell2 | cell3] <= 4:  # and if only 4 digits are set then...
                            for n4 in range(n3 + 1, len(xet)):  # with every other cell on the row
                                cell4 = board[xet[n4]]  # What is in this cell?
                                if popcount[cell1 | cell2 | cell3 | cell4] < 4:  # and if only 3 digits are set then...
                                    print("ERROR: Too few digits in ruleof4xet")
                                    x=1/0
                                if popcount[cell1 | cell2 | cell3 | cell4] == 4:  # and if only 3 digits are set then...
                                    #print("n1=",n1,", n2=",n2,", n3=",n3, n4=",n4)  #display where we are
                                    #print("Match")
                                    notthis=511-(cell1 | cell2 | cell3 | cell4);        #The inverse of this value
                                    for nn in range(0,len(xet)):          #Look through every cell on the xet
                                        if (nn!=n1) and (nn!=n2) and (nn!=n3) and (nn!=n4): #If the cell is not one that we are pointing at right now:
                                            board[xet[nn]]=board[xet[nn]] & notthis #Strip these digits

def ruleof5xet(xet): #Eliminate possibles where a cellquad in that set are definitely known.
    #for example:   98 6  3 1  987654321  987654321
    #               987654321  98 6  3 1  98 6  3 1
    #               98 6  3 1  987654321  987654321
    #should result in 3 & 1 being removed from the rest of the xet:
    #for example:   98 6  3 1    7 54 2     7 54 2
    #                 7 54 2   98 6  3 1  98 6  3 1
    #               98 6  3 1    7 54 2     7 54 2
    #    print("ruleof4xet(",y,")")
    for n1 in range(0,len(xet)-4):                         #Compare every cell on the row
        cell1 = board[xet[n1]]  # What is in this cell?
        #print("n1=",n1)
        if popcount[cell1] <= 5:  # and if only 5 digits are set then...
            for n2 in range(n1+1,len(xet)-3):                  #with every other cell on the row
                #print("n1=",n1,"n2=", n2)
                cell2 = board[xet[n2]]  # What is in this cell?
                if popcount[cell1 | cell2] <= 5:  # and if only 5 digits are set then...
                    for n3 in range(n2 + 1, len(xet)-2):           # with every other cell on the row
                        #print("n1=",n1,"n2=", n2,"n3=", n3)
                        cell3 = board[xet[n3]]  # What is in this cell?
                        if popcount[cell1 | cell2 | cell3] <= 5:  # and if only 5 digits are set then...
                            for n4 in range(n3 + 1, len(xet)-1):  # with every other cell on the row
                                #print("n1=",n1,"n2=", n2,"n3=", n3,"n4=", n4)
                                cell4 = board[xet[n4]]  # What is in this cell?
                                if popcount[cell1 | cell2 | cell3 | cell4] <= 5:  # and if only 5 digits are set then...
                                    for n5 in range(n4 + 1, len(xet)):  # with every other cell on the row
                                        #print("n1=",n1,"n2=", n2,"n3=", n3,"n4=", n4, "n5=", n5)
                                        cell5 = board[xet[n5]]  # What is in this cell?
                                        if popcount[cell1 | cell2 | cell3 | cell4 | cell5] < 5:  # and if only 3 digits are set then...
                                            print("ERROR: Too few digits in ruleof5xet")
                                            x=1/0
                                        if popcount[cell1 | cell2 | cell3 | cell4 | cell5] == 5:  # and if only 3 digits are set then...
                                            #print("n1=",n1,", n2=",n2,", n3=",n3, ", n4=",n4, ", n5=",n5)  #display where we are
                                            #print("Match")
                                            notthis=511-(cell1 | cell2 | cell3 | cell4 | cell5);        #The inverse of this value
                                            for nn in range(0,len(xet)):          #Look through every cell on the xet
                                                if (nn!=n1) and (nn!=n2) and (nn!=n3) and (nn!=n4) and (nn!=n5): #If the cell is not one that we are pointing at right now:
                                                    board[xet[nn]]=board[xet[nn]] & notthis #Strip these digits


def testruleof1xet(): #Test the "Rule of 1" for a set.
    #Try each set in the puzzle.
    for xet in xets:       #Every row, column and nonet
        resetboard(511)    #set every cell to every possible value
        board[xet[5]]=16   #Middle cell in this xet is now "5"
        ruleof1xet(xet)    #Remove "5" from every cell in that xet
        # test that "5" has been removed from the xet, but nowhere else
        # As I worked through these tests, make them 511 so I can check everything left is 511
        assert board[xet[ 5]]==16  #Check this is still 16, but fix it.
        board[xet[5]]=511-16
        for n in range(0,len(xet)):
            assert board[xet[n]]==511-16
            board[xet[n]]= 511
        for n in range(0, 81):
            assert board[n] == 511

def testruleof2xet(): #Test the "Rule of 2" for a set. If 2 cells contain the same 2 digits, eliminate that from the rest of the cells
    #Try each xet in the puzzle.
    for xet in xets:
        resetboard(511)  # set every cell to every possible value
        board[xet[0]]=5   #Top left cell in this xet is now "3" or "1"
        board[xet[4]]=5   #Middle cell in this xet is now "3" or "1"
        #print_board()
        ruleof2xet(xet)                 #Remove "3" and "1" from 7 cells in that xet
        # test that "3" & "1" have been removed from the xet, but nowhere else
        #print_board()
        assert board[xet[ 0]]==  5  #Check this is still 5, but fix it.
        board[xet[ 0]] =511-5
        assert board[xet[ 4]]==  5  #Check this is still 5, but fix it.
        board[xet[ 4]] =511-5
        for n in range(0,len(xet)):
            assert board[xet[n]]==511-5
            board[xet[n]]= 511
        for n in range(0, 81):
            assert board[n] == 511

def testruleof3xet():  # Test the "Rule of 3" for a set. If 3 cells contain the same 3 digits, eliminate that from the rest of the cells
    # Try each xet in the puzzle.
    for xet in xets:
        resetboard(511)  # set every cell to every possible value
        board[xet[0]] =  13  # Top left cell in this xet is now "9", "4", "3" | "1" (8+4+1)
        board[xet[2]] =  13  # Top right cell in this xet is now "9", "4", "3" | "1"
        board[xet[3]] =  13  # Centre left centre cell in this xet is now "9", "4", "3" | "1"
        ruleof3xet(xet)  # Remove "4", "3" and "1" from 7 cells in that xet
        # test that "4", "3" & "1" have been removed from the xet, but nowhere else
        #print_board()
        assert board[xet[0]] == 13  # Check this is still 13, but fix it.
        board[xet[0]] = 511-13
        assert board[xet[2]] == 13  # Check this is still 13, but fix it.
        board[xet[2]] = 511-13
        assert board[xet[3]] == 13  # Check this is still 13, but fix it.
        board[xet[3]] = 511-13
        for n in range(0, len(xet)):
            assert board[xet[n]] == 511 - 13  # Check every cell in the set is okay
            board[xet[n]] = 511
        #print_board()
        for n in range(0, 81):                # Check every cell in the board
            assert board[n] == 511

def testruleof4xet():  # Test the "Rule of 4" for a set. If 4 cells contain the same 4 digits, eliminate that from the rest of the cells
    # Try each xet in the puzzle.
    for xet in xets:
        resetboard(511)  # set every cell to every possible value
        board[xet[0]] = 269  # Top left cell in this xet is now "9", "4", "3" or "1" (256+8+4+1)
        board[xet[2]] = 269  # Top right cell in this xet is now "9", "4", "3" or "1"
        board[xet[3]] = 269  # Centre left centre cell in this xet is now "9", "4", "3" or "1"
        board[xet[5]] = 269  # Centre right centre cell in this xet is now "9", "4", "3" or "1"
        ruleof4xet(xet)  # Remove "9", "4", "3" and "1" from 7 cells in that xet
        # test that "9", "4", "3" & "1" have been removed from the xet, but nowhere else
        #print_board()
        assert board[xet[0]] == 269  # Check this is still 269, but fix it.
        board[xet[0]] = 511-269
        assert board[xet[2]] == 269  # Check this is still 269, but fix it.
        board[xet[2]] = 511-269
        assert board[xet[3]] == 269  # Check this is still 269, but fix it.
        board[xet[3]] = 511-269
        assert board[xet[5]] == 269  # Check this is still 269, but fix it.
        board[xet[5]] = 511-269
        for n in range(0, len(xet)):
            assert board[xet[n]] == 511 - 269  # Check every cell in the set is okay
            board[xet[n]] = 511
        #print_board()
        for n in range(0, 81):                # Check every cell in the board
            assert board[n] == 511

def testruleof5xet():  # Test the "Rule of 5" for a set. If 5 cells contain the same 5 digits, eliminate that from the rest of the cells
    # Try each xet in the puzzle.
    for xet in xets:
        resetboard(511)  # set every cell to every possible value
        board[xet[0]] = 397  # Top left cell in this xet is now "9", "8", "4", "3" or "1" (256+128+8+4+1)
        board[xet[2]] = 397  # Top right cell in this xet is now "9", "8", "4", "3" or "1"
        board[xet[3]] = 397  # Centre left centre cell in this xet is now "9", "8", "4", "3" or "1"
        board[xet[5]] = 397  # Centre right centre cell in this xet is now "9", "8", "4", "3" or "1"
        board[xet[6]] = 397  # Centre right centre cell in this xet is now "9", "8", "4", "3" or "1"
        ruleof5xet(xet)  # Remove "9", "4", "3" and "1" from 7 cells in that xet
        # test that "9", "4", "3" & "1" have been removed from the xet, but nowhere else
        #print_board()
        assert board[xet[0]] == 397  # Check this is still 397, but fix it.
        board[xet[0]] = 511-397
        assert board[xet[2]] == 397  # Check this is still 397, but fix it.
        board[xet[2]] = 511-397
        assert board[xet[3]] == 397  # Check this is still 397, but fix it.
        board[xet[3]] = 511-397
        assert board[xet[5]] == 397  # Check this is still 397, but fix it.
        board[xet[5]] = 511-397
        assert board[xet[6]] == 397  # Check this is still 397, but fix it.
        board[xet[6]] = 511-397
        for n in range(0, len(xet)):
            assert board[xet[n]] == 511 - 397  # Check every cell in the set is okay
            board[xet[n]] = 511
        #print_board()
        for n in range(0, 81):                # Check every cell in the board
            assert board[n] == 511

#    def testruleof5xet()
#    def testruleof6xet()
#    def testruleof7xet()
#    def testruleof8xet()
#    def testonlyplacexet()
#    def testruleof1col()
#    def testruleof2col()
#    def testruleof3col()
#    def testruleof4col()
#    def testruleof5col()
#    def testruleof6col()
#    def testruleof7col()
#    def testruleof8col()
#    def testonlyplacecol()
#    def testruleof1row()
#    def testruleof2row()
#    def testruleof3row()
#    def testruleof4row()
#    def testruleof5row()
#    def testruleof6row()
#    def testruleof7row()
#    def testruleof8row()
#    def testonlyplacerow()
#    def testruleof1cage()
#    def testruleof2cage()
#    def testruleof3cage()
#    def testruleof4cage()
#    def testruleof5cage()
#    def testruleof6cage()
#    def testruleof7cage()
#    def testruleof8cage()
#    def testonlyplacecage()



#Execute the tests:
start_time = time.process_time()
testruleof1xet()
testruleof2xet()
testruleof3xet()
testruleof4xet()
testruleof5xet()
#testruleof6xet()
#testruleof7xet()
#testruleof8xet()
#testonlyplacexet()
#testruleof1col()
#testruleof2col()
#testruleof3col()
#testruleof4col()
#testruleof5col()
#testruleof6col()
#testruleof7col()
#testruleof8col()
#testonlyplacecol()
#testruleof1row()
#testruleof2row()
#testruleof3row()
#testruleof4row()
#testruleof5row()
#testruleof6row()
#testruleof7row()
#testruleof8row()
#testonlyplacerow()
#testruleof1cage()
#testruleof2cage()
#testruleof3cage()
#testruleof4cage()
#testruleof5cage()
#testruleof6cage()
#testruleof7cage()
#testruleof8cage()
#testonlyplacecage()
print("Elapsed=",time.process_time()-start_time)
