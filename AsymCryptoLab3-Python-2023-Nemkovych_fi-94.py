import random
import math


def euclid(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


def euclid_extended(p, q):
    if p == 0:
        return 0, 1
    x1, y1 = euclid_extended(q % p, p)
    u = y1 - (q // p) * x1
    v = x1
    return u, v


def jacobi(a, n, j):
    i = 0
    while a % 2 == 0:
        a = a / 2
        i += 1
    if i % 2 == 1:
        j = j * (-1) ** ((n ** 2 - 1) / 8)
    if a != 1:
        a1 = n % a
        n1 = a
    else:
        a1 = a
        n1 = n
    j = j * (-1) ** (((a - 1) * (n - 1)) / 4)
    if a1 == 0:
        j = 0
    if a1 == 2:
        j = j * ((-1) ** ((n1 ** 2 - 1) / 8))
    if a1 >= 3:
        j = jacobi(a1, n1, j)
    return j


def trial_divs(n):
    n = str(n)
    i = 0
    a = []
    while i < len(n):
        a.append(int(n[i]))
        i += 1
    m = [2, 3, 5]
    i = m[-1] + 1
    while i < 1000:
        if mill_rab(i) == 1:
            m.append(i)
        i += 1
    dividers = []
    i = 0
    while i < len(m):
        r = [1]
        j = 0
        summ = 0
        while j < len(a) - 1:
            r.append((r[j] * 10) % m[i])
            j += 1
        j = 0
        while j < len(a):
            summ += a[len(a) - j - 1] * r[j]
            j += 1
        if summ % m[i] == 0:
            dividers.append(m[i])
        i += 1
    if len(dividers) == 0:
        return 1
    return dividers


def mill_rab(p):
    d = p - 1
    s = 0
    k = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    if (d * (2 ** s)) != (p - 1):
        print('d =', d)
        print('s =', s)
        print('d * (2**s) =', d * (2 ** s))
        return 'incorrect number arrangement'
    while k < 1000:
        cheker_x = 0
        x = random.randint(2, p)
        if euclid(x, p) != 1:
            return 0
        x = pow(x, d, p)
        if x == 1 or x == p - 1:
            cheker_x = 1
        else:
            x_r = pow(x, 2, p)
            i = 0
            while i < s:
                if x_r == p - 1:
                    cheker_x = 1
                    break
                if x_r == 1:
                    return 0
                x_r = pow(x_r, 2, p)
                i += 1
        if cheker_x == 0:
            return 0
        if pow(x, p - 1, p) != 1:
            return 0
        k += 1
    return 1


def bbs(n):
    lst = []
    # p = 284100283511244958272321698211826428679
    # q = 22582480853028265529707582510375286184991
    p = hex(0xD5BBB96D30086EC484EBA3D7F9CAEB07)
    q = hex(0x425D2B9BFDB25B9CF6C416CC6E37B59C1F)
    p = int(p, 16)
    q = int(q, 16)
    pq = p * q
    r = random.randint(2, pq - 1)
    for i in range(0, n - 2):
        r = pow(r, 2, pq)
        r_i = bin(r).replace("0b", "")
        for j in range(0, 8):
            lst.append(int(r_i[-1 - j]))
    while len(lst) > n - 1:
        lst.pop()
    lst.insert(0, 1)
    lst[-1] = 1
    return lst


# 0x00 = 0, 0xFF = 255


def lst_to_int(lst):
    n = 0
    i = 0
    while i < len(lst):
        n += lst[i] * pow(2, len(lst) - 1 - i)
        i += 1
    return n


def prime_pair():
    pq = []
    notpq = []
    var = lst_to_int(bbs(150))
    while len(pq) != 2:
        if trial_divs(var) == 1 and mill_rab(var) == 1:
            var1 = 4 * var + 3
            i = 2
            while i <= 1000:
                if trial_divs(var1) == 1 and mill_rab(var1) == 1:
                    pq.append(var1)
                    var = lst_to_int(bbs(256))
                    print('+1 prime:', var1)
                    break
                notpq.append(var1)
                var1 = 4 * i * var + 3
                i += 1
        else:
            notpq.append(var)
            var += 2
    return pq, notpq


def generate_key_pair():
    pq = prime_pair()[0]
    p = pq[0]
    q = pq[1]
    n = p * q
    n_len = len(str(n))
    b = lst_to_int(bbs(n_len))
    return [p, q, b], [n, b]


# +1 k: 50363049279313381763221905613517663557976408296002413892411275258479401591611
# +1 prime: 24375715851187676773399402316942549162060581615265168323927057225104030370339727
# +1 k: 51328036674747074133754277505317862391634212796779204703807968739754712172813
# +1 prime: 410624293397976593070034220042542899133073702374233637630463749918037697382507
# 170


def format_m(m, n, change_r):
    m = bin(m).replace('0b', '')
    m = [int(i) for i in m]
    if change_r == 0:
        n_str = bin(n).replace('0b', '')
        while len(n_str) % 8 != 0:
            n_str = '0' + n_str

        while len(m) != (len(n_str) - 80):
            m.insert(0, 0)
        for i in range(8):
            m.insert(0, 1)
        r = bbs(64)
        m = m + r
    else:
        del m[(len(m) - 64):]
        r = bbs(64)
        m += r
    return m


def encrypt(public_key, x):
    n, b = public_key
    x = lst_to_int(x)
    print(hex(n))
    print(hex(x))
    y = (x * (x + b)) % n
    b_2 = b * pow(2, -1, n)
    c_1 = ((x + b_2) % n) % 2
    if jacobi(x + b_2, n, 1) == 1:
        c_2 = 1
    else:
        c_2 = 0
    return hex(y), c_1, c_2


#print([76758244053636461179013759911522556793921788712017992801470169734100161234073, 70834703743325079791850008388434552349615476308514453243515374993884519528631], )
def decrypt(secret_key, c):
    p, q, b = secret_key
    y, c_1_real, c_2_real = c
    n = p * q
    var1 = (- b * pow(2, -1, n)) % n
    var2 = y + (pow(b, 2, n) * pow(4, -1, n)) % n
    print('var2 =', var2)
    s_1 = pow(var2, int((p + 1) / 4), p)
    s_2 = pow(var2, int((q + 1) / 4), q)
    print(s_1)
    print(s_2)
    u, v = euclid_extended(p, q)
    x_1 = (u * p * s_2 + v * q * s_1) % n
    x_2 = (u * p * s_2 - v * q * s_1) % n
    x_3 = (-u * p * s_2 + v * q * s_1) % n
    x_4 = (-u * p * s_2 - v * q * s_1) % n
    x_list = [x_1, x_2, x_3, x_4]
    print('')
    for i in x_list:
        print(hex(i))
    print('')
    for i in x_list:
        print(bin(i).replace('0b', ''))
    print('')
    for i in range(4):
        c_1 = (x_list[i]) % 2
        if jacobi(x_list[i], n, 1) == 1:
            c_2 = 1
        else:
            c_2 = 0
        if c_1 == c_1_real and c_2 == c_2_real:
            x_list[i] = (var1 + x_list[i]) % n
            print('x =', x_list[i])
            result = bin((x_list[i])).replace('0b', '')
            result = [int(i) for i in result]
            result = result[8:len(result) - 64]
            result = lst_to_int(result)
            return result, c_1, c_2


def sign(m, secret_key):
    p, q, b = secret_key
    n = p * q
    x = format_m(m, n, 0)
    x = lst_to_int(x)
    while jacobi(x, p, 1) != 1 and jacobi(x, q, 1) != 1:
        x = format_m(x, n, 1)
        x = lst_to_int(x)
    print(bin(x).replace('0b', ''))
    print(len(bin(x).replace('0b', '')))
    print(len(bin(n).replace('0b', '')))
    s_1 = pow(x, int((p + 1) / 4), p)
    s_2 = pow(x, int((q + 1) / 4), q)
    print('')
    print(s_1)
    print(p)
    print('')
    print(s_2)
    print(q)
    # s_1 = pow(x, int((p + 1) * pow(4, -1, p)), p)
    # s_2 = pow(x, int((q + 1) * pow(4, -1, q)), q)
    u, v = euclid_extended(p, q)
    u = u
    v = v
    print('')
    print((u * p * s_2) % n)
    print((v * q * s_1) % n)
    print('')
    s = (u * p * s_2 + v * q * s_1) % n
    return m, s


def verify(ms, public_key):
    m, s = ms
    n = public_key[0]
    x = pow(s, 2, n)
    x = bin(x).replace('0b', '')
    x_ = [int(i) for i in x]

    m = bin(m).replace('0b', '')
    n = bin(n).replace('0b', '')
    if len(m) < len(n) - 80:
        m = '0' * (len(n) - 80 - len(m)) + m
    m = '1' * 8 + m
    m_ = [int(i) for i in m]
    if x_[:len(x_) - 64] == m_:
        return hex(lst_to_int(x_[8:len(x_) - 64])), 'Signature is verified'
    else:
        return 0, 'Signature is not verified'


def attack(n):
    t = random.randint(2 ** 8, 2 ** 2048)
    print('Value t^2 :', hex(pow(t, 2, n)).replace('0x', ''))
    z = int(input(), 16)
    while (n % math.gcd(t + z, n)) != 1:
        t = random.randint(2 ** 8, 2 ** 2048)
        print('Value t^2 :', hex(pow(t, 2, n)).replace('0x', ''))
        print(math.gcd(t + z, n), ' - p')
        z = int(input(), 16)
        if t != z and t != n - z:
            return hex(math.gcd(t + z, n)), 'VICTORY!!!'

    print(math.gcd(t + z, n), ' - p')
    return math.gcd(t + z, n), 'VICTORY!!!'


def initialization():
    private, public = generate_key_pair()
    return private, public


def verify_sign_proc(ms, public):
    result = verify(ms, public)
    return result
