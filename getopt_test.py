import getopt
import sys

def parse_args(args):
    mac = test_str = None
    try:
        opts, args = getopt.getopt(args, "hm:s:", ["mac=", "string="])
    except getopt.GetoptError:
        print("you're doing it wrong")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("this is a help message")
            sys.exit()
        elif opt in ('-m', '--mac'):
            mac = arg
        elif opt in ('-s', '--string'):
            test_str = arg
    
    return mac, test_str

if __name__ == '__main__':
    mac_a, test_a = parse_args(sys.argv[1:])
    print(mac_a)
    print(test_a)

