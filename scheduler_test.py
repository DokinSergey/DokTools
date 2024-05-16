import sched, time
s = sched.scheduler(time.time, time.sleep)
p = time.time()
def print_time(a='default'):
    print("From print_time", time.time() - p, a)

def print_some_times():
    print(time.time()-p)
    s.enter(10, 1, print_time)
    s.enter(5, 2, print_time, argument=('positional',))
    s.enter(5, 0, print_time, kwargs={'a': 'keyword'})
    s.run()
    print(time.time()-p)

print_some_times()
