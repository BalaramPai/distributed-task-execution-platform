# src/workers/worker.py
from threading import Thread

class Worker:
    """
    Represents a single worker in the scheduler.

    This class acts as a wrapper around the worker thread and will
    gradually be extended with lifecycle information, statistics,
    heartbeats, and shutdown controls in later phases.
    
    So earlier a thread used to do the work.
    Now the worker makes the thread do the work.
    Both times thread does the work, but now the thread is created and
    managed by the worker with all the above features.
    """
    
    # Exectues the moment a worker object is created.
        # So basically Id and name alloted to worker and he creates a thread.
    def __init__(self,worker_id,target):
        
        # So when we call the class for a worker object
        # it'll be Worker(1,worker)  where the worker is the function.
        
        # This is the worker id.
        self.worker_id = worker_id
        
        # Here the worker is creating the thread for itself.
        self.thread = Thread(
            target = target,
            daemon=True,   # Means its a background thread that terminates when main program finishes executing and thus dont block the program from exiting.
            name=f"Worker-{worker_id}"
        )

    
    @property
    # Now this is used similar to a method.
            # So instead of making a class method like get_name() and then calling 
            # worker.get_name()-- function we just do worker.name  
            # Reason is name is data and we can just call it as property instead of calling it as a function.
            
            # Note : Why not just make methods , well you can but python tries to make it better: 
            #  method will be .func() but just for some data itll be .parameter. 
    def name(self):
        return self.thread.name
    
    
        
    # Method 1 : Start Thread
    def start(self):
        self.thread.start()
        
    # Method 2: Check Thread status.
    def is_alive(self):
        return self.thread.is_alive()
        