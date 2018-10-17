# conversion.py: handles conversions between bits and ASCII characters

def binaryToInt(binary):
    return int(binary, 2)

def intToChar(intVal):
    return chr(intVal)

def convertTo8Bits(charString):
    '''
    Converts a string of characters to its 8 bit representation.

    Returns: string of binary values
    '''
    result = ''
    for char in charString:
        intChar = ord(char)
        binaryChar = format(intChar, '08b')
        result += binaryChar
    return result

def convertTo32Bits(charString):
    '''
    Converts the number of bits in a string to its 32 bit representation.

    Returns: 32 bit string of binary values
    '''
    numOfBits = 8 * len(charString)
    result = format(numOfBits, '032b')
    return result

def changeLSB(intVal, bitVal):
    '''
    Replaces least significant bit of an R, G, or B value with a given bit value.

    Returns: string of bits
    '''
    binaryVal = format(intVal, 'b')
    bits = list(binaryVal)
    bits[-1] = bitVal
    bits = ''.join(bits)
    return bits

def extractLSB(intVal):
    '''
    Extracts least significant bit of an R, G, or B value.

    Returns: least significant bit
    '''
    binaryVal = format(intVal, 'b')
    bits = list(binaryVal)
    return bits[-1]