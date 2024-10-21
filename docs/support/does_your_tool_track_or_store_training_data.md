---
title: "Does your tool track or store training data?"
<<<<<<< HEAD
tags:
   - 
---

=======
tags: []
---

### Does your tool track or store training data?
>>>>>>> 6ef6c45f4d73f19772f9c0cbb4fbccb2cee243c2
You can pass a SHA or other unique identifier to `wandb.config.update(...)` to associate a dataset with a training run. W&B does not store any data unless `wandb.save` is called with the local file name.