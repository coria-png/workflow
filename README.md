hello dont look at this 


if you look at this, this repo is currently a container for a specific use case and is supposed to do two things:

orchestrator = watches step1 and starts the chain if youve got a multi-step process with a separate script for each step

feed_me = watches final output folder and pulls more fodder from a raw folder into step1



for professional terminology this system has:

- an event-driven watcher
- a multi-step orchestrator
- a debounced batch feeder
- a lock-file synchronization mechanism
- file validation

ToDo(but probably wont):
- debug cross-process interactions
- add logging mechanism
- make pipeline self-healing
