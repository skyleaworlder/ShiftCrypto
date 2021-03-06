name = "continued"
help_info = '''
[ShiCrypto] You're using CLI-continued, the following help info might be helpful:
            Usage: python continued.py [<nume>] [<deno>] [<expand-layer>]
            eg. python continued.py 17 45 4
                python continued.py 17 45 6
'''

export_info = {
    "name": name,
    "help": help_info
}

import sys
from src.continued import continuedFrac

def main(argv):
    nume, deno = int(argv[0]), int(argv[1])
    '''
    because wienner-attack, add member:layer
    but use continued.py always needn't param layer
    if python continued.py 17 45 => layer = 2
    else python continued.py 17 45 4 => layer = 4
    '''
    layer = 2 if len(argv) <= 2 else int(argv[2])
    obj = continuedFrac(nume, deno, layer)
    print(argv[0]+"/"+argv[1]+"'s abbreviated notation is", obj.a_arr, "(layer = "+str(layer)+")")
    print("and nume arr is", obj.p_arr)
    print("    deno arr is", obj.q_arr)

if __name__ == "__main__":
    main(sys.argv[1:])
