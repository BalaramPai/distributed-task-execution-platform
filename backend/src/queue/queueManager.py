from src.queue.taskQueue import TaskQueue

# We do this so that there is one gloabl queue that is created and not for every request we create a new queue or something.

# This queue object is for tasks.
task_queue = TaskQueue()

# This queue is for tasks that have finished their maximum number of tries.
dead_letter_queue = TaskQueue()