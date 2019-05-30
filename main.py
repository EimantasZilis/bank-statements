import user_input.parser as parser

def main():
    cmd = parser.init_parser()
    parser.process_commands(cmd)
    
if __name__ == "__main__":
    main()
