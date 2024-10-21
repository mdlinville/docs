---
title: "What does `wandb.init` do to my training process?"
<<<<<<< HEAD
tags:
   - 
---

=======
tags: []
---

### What does `wandb.init` do to my training process?
>>>>>>> 6ef6c45f4d73f19772f9c0cbb4fbccb2cee243c2
When `wandb.init()` is called from your training script an API call is made to create a run object on our servers. A new process is started to stream and collect metrics, thereby keeping all threads and logic out of your primary process. Your script runs normally and writes to local files, while the separate process streams them to our servers along with system metrics. You can always turn off streaming by running `wandb off` from your training directory, or setting the `WANDB_MODE` environment variable to `offline`.