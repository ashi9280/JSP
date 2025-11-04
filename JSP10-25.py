import matplotlib.pyplot as plt
from mpmath import mp

mp.dps = 100


def print_mat(arr):
    for i in range(len(arr)):
        print(arr[i])

def find_q(p):
    p = mp.mpf(p)

    state_diagram = [[0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0]]

    As            = [[0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]]

    Bs            = [[0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]]

    Penter        = [[1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]]

    for i in range(3):
        for j in range(4):
            balls = 3-j
            strikes = 2-i

            e1 = mp.mpf(state_diagram[strikes][balls+1])
            e2 = mp.mpf(state_diagram[strikes+1][balls])

            ev = mp.mpf((e2-e1)**2/(e2-e1+p*(e2-4)) + e1)

            state_diagram[strikes][balls] = ev

            As[strikes][balls] = mp.mpf(p*(e2-4)/(e2-e1+p*(e2-4)))
            Bs[strikes][balls] = mp.mpf((e2-e1)/(e2-e1+p*(e2-4)))

    for strikes in range(3):
        for balls in range(4):
            if balls == 0 and strikes == 0:
                continue

            from_ball = 0
            from_strike = 0

            if balls:
                A = As[strikes][balls-1]
                B = mp.mpf(1) - A
                from_ball = Penter[strikes][balls-1] * A * A
            if strikes:
                A = As[strikes-1][balls]
                B = mp.mpf(1) - A
                from_strike = Penter[strikes-1][balls] * (A*B + (mp.mpf(1)-A)*B*(mp.mpf(1)-p) + (mp.mpf(1)-A)*(mp.mpf(1)-B))

            Penter[strikes][balls] = from_ball + from_strike

    q = Penter[2][3]

    return q

print(find_q(0.1855))



pmin = mp.mpf(0)
pmax = mp.mpf(1)

n_pts = 100

sweep_p_log = []
sweep_res_log = []

for i in range(n_pts):
    p = mp.mpf(pmin + ((pmax-pmin)*(i+1)) / (n_pts))

    print(p)

    sweep_p_log.append(p)
    sweep_res_log.append(find_q(p))

plt.figure(figsize=(7,5))
plt.plot(sweep_p_log, sweep_res_log, marker='o')
plt.xlabel('p (Home run probability)')
plt.ylabel('q (Probability of reaching full count)')
plt.title('Full-count probability vs home run probability')
plt.grid(True)
plt.show()


pmin = mp.mpf(0.001)
pmax = mp.mpf(1)

qmin = find_q(pmin)
qmax = find_q(pmax)

iters = 100

search_p_log = []
search_res_log = []

for i in range(iters):
    p1 = (pmax - pmin)/mp.mpf(3) + pmin
    p2 = mp.mpf(2)*(pmax - pmin)/3 + pmin

    print(p1, p2)

    q1 = find_q(p1)
    q2 = find_q(p2)

    print(q1, q2)

    if q1 < q2:
        pmin = p1
        search_p_log.append(p1)
        search_res_log.append(q1)
        print(p1)
    else:
        pmax = p2
        search_p_log.append(p2)
        search_res_log.append(q2)
        print(p2)


print(search_p_log[-1])
print(search_res_log)

plt.figure(figsize=(7,5))
plt.plot(search_p_log, search_res_log, marker='o', linestyle='-')
plt.xlabel('p (home run probability)')
plt.ylabel('q (probability of reaching full count)')
plt.title('Search trace for maximizing q(p)')
plt.grid(True)
plt.show()