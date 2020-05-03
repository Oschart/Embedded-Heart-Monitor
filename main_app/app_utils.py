def valid_input(prompt, is_valid):
    res = input(prompt)
    while not is_valid(res):
        print('Sorry, try again!')
        res = input(prompt)
    return res

def display_brief_guide():
    print('Supported Commands: ')
    print('SSR(R): -> Sets sampling rate to R')
    return
    
