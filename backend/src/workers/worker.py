# src/workers/worker.py
from threading import Thread, Event
from time import sleep
from datetime import datetime
from src.schemas.enums import WorkerState
from src.constants.workerConstants import (
    HEARTBEAT_INTERVAL,
    HEARTBEAT_TIMEOUT
)

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
        
        # Meta data of the Thread.
        self.created_at = datetime.utcnow()
        self.thread_id = None   # The OS doesnt allot any identifier to a thread unless it starts so when we create the object its none as the thread has still not started executing and thus the OS hasnt alloted anythign yet.
        self.current_task = None
        self.tasks_executed = 0
        self.successful_tasks = 0
        self.failed_tasks = 0
        self.retried_tasks = 0
        self.state = WorkerState.STARTING
        self.last_heartbeat = datetime.utcnow()
        self.shutdown_event = Event() # Creates a thread-safe signal that this worker can use, to detect when a shutdown has been requested.
        
        # Here the worker is creating the thread for itself.
        self.thread = Thread(
            target = target,
            # Note : It has to be self, as args takes a tuple and just self will be element.
            args=(self,),  # Now the thread automatically passes its owning Worker object into the function.
            ## So basically the WORKER OBJ starts a thread and then pushes itself inside the thread via the worker fucntion.
            daemon=True,   # Means its a background thread that terminates when main program finishes executing and thus dont block the program from exiting.
            name=f"Worker-{worker_id}",
        )
        
        # Here the worker is creating the heatbeat thread for itself.
        self.heartbeat_thread = Thread(
            target=self._heartbeat_loop,
            daemon=True,
            name=f"Worker-{worker_id}-Heartbeat",
        )
        
        # Worker-1
        # │
        # ├── Worker-1
        # │     └── executes tasks
        # │
        # └── Worker-1-Heartbeat
        #     └── updates heartbeat every 2 seconds

    
    @property
    # Now this is used similar to a method.
            # So instead of making a class method like get_name() and then calling 
            # worker.get_name()-- function we just do worker.name  
            # Reason is name is data and we can just call it as property instead of calling it as a function.
            
            # Note : Why not just make methods , well you can but python tries to make it better: 
            #  method will be .func() but just for some data itll be .parameter. 
    def name(self):
        return self.thread.name
    
    @property
    def is_idle(self):
        return self.state == WorkerState.IDLE  
    
    @property
    def is_healthy(self):
        # A worker is healthy when its latest heartbeat is within the allowed timeout.
        elapsed_time = datetime.utcnow() - self.last_heartbeat
        return elapsed_time.total_seconds() <= HEARTBEAT_TIMEOUT    # Returns true if heartbeat in the designated time interval.
    
        
    # Methods and functions for a worker.
    def start(self):
        self.thread.start()
        self.heartbeat_thread.start()
        
        self.thread_id = self.thread.ident # Thread-id is owned by the Worker.
        self.state = WorkerState.IDLE # After creation untill it processes its in idle.
    
    def update_heartbeat(self):
            self.last_heartbeat = datetime.utcnow() # Updates the timestamp to show that this worker is still alive and responsive.
    
    def stop(self):
        print(f"{self.name} shutdown requested.")
        self.state = WorkerState.STOPPING  # It means we have initiated a shutdown request and the worker has to stop after finishing the cuurent task.
        self.shutdown_event.set()       # Changes it from FALSE -> TRUE (Which means a shutdown has been intitiated.)
    
    def join(self):
        self.thread.join()  # wait until it has actually finished shutting down.
        self.heartbeat_thread.join() # wait untill the heartbeat thread finishes.
        print(f"{self.name} stopped.")
        
    # So stop is requesting to stop
    # join is waiting for the thread to stop.    
    
    def is_alive(self):
        return self.thread.is_alive()
    
    def _heartbeat_loop(self):
        while not self.shutdown_event.is_set():
            self.update_heartbeat()
            sleep(HEARTBEAT_INTERVAL)
    
    def __repr__(self):     # stands for Representation, if someone wants to represent this object as text.
        return(
            "Worker("
            f"id={self.worker_id}, "
            f"name={self.name}, "           # Python automcatically concats strings.
            f"alive={self.is_alive()}, "
            f"state={self.state}, "
            f"current_task={self.current_task}, "
            f"tasks_executed={self.tasks_executed}, "
            f"successful_tasks={self.successful_tasks}, "
            f"failed_tasks={self.failed_tasks}, "
            f"retried_tasks={self.retried_tasks}"
            ")"
        ) 