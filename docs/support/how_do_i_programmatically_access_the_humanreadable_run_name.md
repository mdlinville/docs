---
title: "How do I programmatically access the human-readable run name?"
<<<<<<< HEAD
tags:
   - experiments
---

=======
tags: []
---

### How do I programmatically access the human-readable run name?
>>>>>>> 6ef6c45f4d73f19772f9c0cbb4fbccb2cee243c2
It's available as the `.name` attribute of a [`wandb.Run`](../../ref/python/run.md).

```python
import wandb

wandb.init()
run_name = wandb.run.name
```