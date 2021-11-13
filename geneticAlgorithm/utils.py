from types import CellType
import numpy as np
import classes.Trap as TrapClass
from classes.Cell import Cell
from classes.Encoding import Encoding
from enums.Cell import CellType as CellEnum
from enums.Angle import AngleType as AngleEnum
from enums.Rotation import RotationType as RotationEnum
from enums.Thick import ThickType as ThickEnum

def createTrap(configuration):
    """Takes in a board configuration and wraps that configuration in a trap class"""
    return TrapClass.Trap(len(configuration[0]), len(configuration), False, chosenBoard = configuration)

def convertStringToEncoding(strEncoding, delimiter=','):
    """Takes in an encoding as a string and returns that encoding as a list"""
    if delimiter not in strEncoding:
        delimiter = ' '

    strList = strEncoding.strip()[1:-1] # getting the numbers
    digitList = strList.split(delimiter) # splitting number strings by digits

    return np.array([int(digit.strip()) for digit in digitList if digit])

def convertEncodingToString(encoding):
    """Takes in an encoding and returns the string version of it"""
    encodingStr = '[ '

    for i, elem in enumerate(encoding):            
        encodingStr += '{}'.format(str(elem))
        if i < len(encoding) - 1:
            encodingStr += ', '
    encodingStr += ' ]'
    
    return encodingStr

def convertStringToDecoding(strEncoding, encoder: Encoding = None):
    """ Takes in a string encoding and returns the decoded trap """
    if not encoder:
        encoder = Encoding()
    return encoder.singleDecoding(convertStringToEncoding(strEncoding))

def createCell(cell_code):
    '''
    Creates the given cell using the respective cell codes
    type = { door: 1, wire: 2, arrow: 3, food: 5, floor: 6 }
    angle = { lacute: 0, racute: 1, lright: 2, rright : 3, lobtuse : 4, robtuse : 5, straight : 6, na: 'x' }
    rotation = { up: 0, right: 2, down: 4, left: 6, na: 'x' }
    thickness = { skinny: 0, normal: 1, wide: 2, na: 'x' }

    Example cell code: '3202' -> arrow, right angled to the left, rotated up, wide thickness
    '''
    if len(cell_code) != 4:
        print(f'{cell_code} is not a valid cell code')
        return None

    type, angle, rotation, thickness = cell_code

    type = int(type)
    angle = int(angle) if angle != 'x' else angle
    rotation = int(rotation) if rotation != 'x' else rotation
    thickness = int(thickness) if thickness != 'x' else thickness

    type = CellEnum(type)
    angle = AngleEnum(angle)
    rotation = RotationEnum(rotation)
    thickness = ThickEnum(thickness)

    return Cell(0, 0, type, None, angle, rotation, thickness)

def createTrap(cell_codes: list[str], encoding: Encoding = Encoding()):
    '''
    takes in a list of cell codes and returns the encoding of a trap with those cells
    example: createTrap(['6xxx', '6xxx', '6xxx', '6xxx', '6xxx', '5xxx', '6xxx', '6xxx', '6xxx', '3162', '1xxx', '3022'])
    creates all floors and heavy arrows at the doors
    '''
    if len(cell_codes) != 12:
        print('Traps should have 12 elements in them')
        return None
    
    return encoding.encode([createCell(code) for code in cell_codes])
