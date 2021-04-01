import sys
pi=22/7
def evaluate():
    x=input('Enter a valid question: ')
    if 'exit' in x:
        return 0
    try:
        x=x.replace('^','**')
        print('Answer:',eval(x))
        return 1
    
    except SyntaxError:
        x=x.replace('^','**')
        if x.endswith('='):
            x=x.replace('=','')
            try:
                print('Answer:',eval(x))
                return 1
            except Exception as e:
                sys.stderr.write('Please make sure you have given the right input.\n')
                return 2
        else:
            sys.stderr.write('Please make sure you have given the right input.\n')
            return 2
    
    except Exception as e:
        sys.stderr.write('Please make sure you have given the right input.\n')
        return 2
        
def main():
    code=1
    while code!=0:
        code=evaluate()
    sys.exit(0)
    
if __name__ == '__main__':
    main()