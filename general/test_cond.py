import multiprocessing
import time

def stage_1(cond):
    """perform first stage of work, then notify stage_2 to continue"""
    name = multiprocessing.current_process().name
    print 'Starting', name
    with cond:
        print '%s done and ready for stage 2' % name
        cond.notify_all()

def stage_2(cond1, cond2):
    """wait for the condition telling us stage_1 is done"""
    name = multiprocessing.current_process().name
    print 'Starting', name
    cond1.acquire()
    cond1.wait()
    cond1.release()

    cond2.acquire()
    cond2.wait()
    cond2.release()
    
    print '%s running' % name
#    with cond1:
#        cond1.wait()
#        cond2.wait()
#        print '%s running' % name

if __name__ == '__main__':
    condition1 = multiprocessing.Condition()
    condition2 = multiprocessing.Condition()
    s1 = multiprocessing.Process(name='s1', target=stage_1, args=(condition1,))
    s1_2 = multiprocessing.Process(name='s1_2', target=stage_1, args=(condition2,))

    s2_clients = [
        multiprocessing.Process(name='stage_2[%d]' % i, target=stage_2, args=(condition1,condition2))
        for i in range(1, 3)
        ]

    for c in s2_clients:
        c.start()
        time.sleep(1)
    s1.start()
    s1_2.start()

    s1.join()
    s1_2.join()
    for c in s2_clients:
        c.join()

    print("waiting?");