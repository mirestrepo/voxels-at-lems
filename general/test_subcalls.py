#! /usr/bin/env python
 
import math
import random
 
import Queue
import multiprocessing
import time
 
def normal_pdf(x, mean, sd):
    return ( (1.0 / math.sqrt(2 * math.pi * pow(sd, 2)))
            * math.exp(-1 * float(pow(x - mean, 2))/(2 * pow(sd, 2))) )
 
def log_prob(x, mean, sd):
    if hasattr(x, "__iter__"):
        return sum([log_prob(i, mean, sd) for i in x])
    else:
        return math.log(normal_pdf(x, mean, sd))
 
class Worker(multiprocessing.Process):
 
    def __init__(self,
            work_queue,
            result_queue,
            mean=0,
            sd=1):
 
        # base class initialization
        multiprocessing.Process.__init__(self)
 
        # job management stuff
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.kill_received = False
 
        # job execution stuff
        self.mean = mean
        self.sd = sd
 
    def run(self):
        while not self.kill_received:
 
            # get a task
            try:
                job = self.work_queue.get_nowait()
            except Queue.Empty:
                break
 
            # the actual processing
            log_prob = sum([math.log(normal_pdf(i, self.mean, self.sd))
                    for i in job])
 
            # store the result
            self.result_queue.put(log_prob)
 
def execute(jobs, num_processes=2):
 
    # load up work queue
    work_queue = multiprocessing.Queue()
    for job in jobs:
        work_queue.put(job)
 
    # create a queue to pass to workers to store the results
    result_queue = multiprocessing.Queue()
 
    # spawn workers
    for i in range(num_processes):
        worker = Worker(work_queue, result_queue, mean=0, sd=1)
        worker.start()
 
    # collect the results off the queue
    results = []
    while len(results) < len(jobs):
        result = result_queue.get()
        results.append(result)
 
    return results
 
if __name__ == "__main__":
 
    for t in range(0,2):
        # generate stuff to do
        rng = random.Random()
        num_jobs = 20
        jobs = []
        for i in range(num_jobs):
            data = []
            for j in range(10):
                data.append(rng.gauss(0, 1))
            jobs.append(data)
     
        # run
        results = execute(jobs)
     
        # dump results
        for r in results:
            print(r)
            
        time.sleep(5)
        print "Round done"