---
title: "Can I just set the run name to the run ID?"
<<<<<<< HEAD
tags:
   - experiments
---

=======
tags: []
---

### Can I just set the run name to the run ID?
>>>>>>> 6ef6c45f4d73f19772f9c0cbb4fbccb2cee243c2
If you'd like to overwrite the run name (like snowy-owl-10) with the run ID (like qvlp96vk) you can use this snippet:

```python
import wandb

wandb.init()
wandb.run.name = wandb.run.id
wandb.run.save()
```