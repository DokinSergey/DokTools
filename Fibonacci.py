from time import perf_counter
from rich import print as rpn
a = b = 0
t0 = perf_counter()
for _ in range(36):
    fi = a + b
    if not fi:b = 1
    a,b = b,fi
    # rpn(fi)
t1 = perf_counter()


rpn(f' {fi} {(t1 - t0) * 1000:.3f}')



input('Выход:-> ')
