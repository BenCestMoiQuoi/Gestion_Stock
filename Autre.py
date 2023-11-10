#####################################
#                                   #
#            Parametres             #
#                                   #
#####################################

path = 'Suivis_couture/'

Nom_projet = 'Suivie de la couture'
Nom_icon = f'{path}icone.ico'

VAR_NULL = '-------'
SEPAR_PARAM = '!'
PARAM_STOCK = ['En cours', 'En stock', 'Vendu']
NOM_FILE = f'{path}stock.csv'


#####################################
#                                   #
#             Fonction              #
#                                   #
#####################################

def reorganiser():
    f = open(NOM_FILE, 'r')
    lines = f.readlines()
    print(lines)
    f.close()

    for i in range(len(lines)):
        t1 = lines[i]
        alpha = t1
        alpha_s = t1.split(';')
        print(i, end='')
        l_para = i
        for j in range(i, len(lines)):
            t2 = lines[j]
            t2_s = t2.split(';')
            if t2_s[1] < alpha_s[1] or t2_s[1] == alpha_s[1] and t2_s[2] < alpha_s[2]:
                alpha_s = t2_s
                l_para = j
        alpha_s[0] = f'{i}'
        alpha = ''
        for k in alpha_s:
            alpha += f'{k}'
            if k != alpha_s[-1]:
                alpha += ';'
        print(j, lines[j])
        lines[i], lines[l_para] = alpha, lines[i]

    f = open(NOM_FILE, 'w')
    for i in lines:
        print(i)
        f.writelines(i)
    f.close()
