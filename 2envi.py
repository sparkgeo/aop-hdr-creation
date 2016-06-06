import sys, getopt
from hdr_meta_clean import AOP_2_ENVI

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
            AOP_2_ENVI(arg)
        else:
            print '2envi.py -a <aop file>'


if __name__ == "__main__":
    main(sys.argv[1:])