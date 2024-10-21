---
title: "Does logging block my training?"
<<<<<<< HEAD
tags:
   - 
---

=======
tags: []
---

### Does logging block my training?
>>>>>>> 6ef6c45f4d73f19772f9c0cbb4fbccb2cee243c2
"Is the logging function lazy? I don't want to be dependent on the network to send the results to your servers and then carry on with my local operations."

Calling `wandb.log` writes a line to a local file; it does not block any network calls. When you call `wandb.init` we launch a new process on the same machine that listens for filesystem changes and talks to our web service asynchronously from your training process.