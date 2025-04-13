import os
import string
import random


##########################################################################################
def PassGen(oper:str = 'pass',ln:int = 12)->str:#'solt'
    random.seed()#-1289)
    # Getting character set for password + string.punctuation
    pss=''
    #-------------------------------------------------------------
    if oper == 'pass':
        ap  = len(punct := r'!"#$%&()*+/:;<=>@[]^`{}~')
        lnp = ln//4 - 1
        # lnp = round(ln/4,0)
        bi = 0
        while len(pss) < lnp or bi > ap:
            bi += 1
            bt = random.choice(punct)
            if bt in pss:continue
            pss += bt
        print(f'p={bi:2}',end=' ')
    #--------------------------------------------------------------,flush = True
    elif oper == 'solt':
        ln = 8
        lnp = 0
    ad = len(digi := string.digits)
    lnd = ln//4# - 1
    # lnd = round(ln/4,0)
    bi = 0
    while len(pss) < lnp + lnd or bi > ad:
        bi += 1
        bt = random.choice(digi)
        if bt in pss:continue
        pss += bt
    print(f'd = {bi:2}',end=' ')
    #-------------------------------------------------------------,flush = True
    au = len(upp := string.ascii_uppercase)
    lnu = ln//4# + 1
    lnu = round(ln/4,0)# + 1
    bi = 0
    while len(pss) < lnp + lnd + lnu or bi > au:
        bi += 1
        bt = random.choice(upp)
        if bt in pss:continue
        pss += bt
    print(f'Up={bi:2}',end=' ')
    #-------------------------------------------------------------,flush = True
    al = len(low := string.ascii_lowercase)
    bi = 0
    while len(pss) < ln or bi > al:
        bi += 1
        bt = random.choice(low)
        if bt in pss.lower():continue
        pss += bt
    print(f'low = {bi:2}',end=' ')
    #-------------------------------------------------------------
    lss = list(pss)
    random.shuffle(lss)
    pss = ''.join(str(ipss) for ipss in lss)
    print(pss)
    return pss
##########################################################################################
if __name__ == '__main__':
    a = ''
    while not a:
        for ii in range(40):

            PassGen('pass',12)
            # PassGen('solt',22)
            # print(f'{ii:2}  {PassGen('pass')}')
        a = input('\nПовтор :-> ')
        print()
    os._exit(0)
