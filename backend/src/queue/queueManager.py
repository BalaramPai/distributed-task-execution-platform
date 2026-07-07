from src.queue.taskQueue import TaskQueue

# We do this so that there is one gloabl queue that is created and not for every request we create a new queue or something.

# This queue object is for tasks.
task_queue = TaskQueue()
