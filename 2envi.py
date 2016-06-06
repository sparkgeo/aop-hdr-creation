import sys, getopt
from aop_to_envi_hdr import create_hdr

def main(argv):
    aop = ''
    try:
        opts, args = getopt.getopt(argv, 'a:', ["aop="])
    except getopt.GetoptError:
        print '2envi.py -a <aop file>'
        sys.exit(2)
    for opt, arg in opts:
        print opt
        if opt in ('-a', "--aop"):
            create_hdr(arg)
        else:
            print '2envi.py -a <aop file>'


if __name__ == "__main__":
    main(sys.argv[1:])