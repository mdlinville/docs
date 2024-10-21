---
title: "Best practices to organize hyperparameter searches"
<<<<<<< HEAD
tags:
   - 
---

=======
tags: []
---

### Best practices to organize hyperparameter searches
>>>>>>> 6ef6c45f4d73f19772f9c0cbb4fbccb2cee243c2
If 10k runs per project (approx.) is a reasonable limit then our recommendation would be to set tags in `wandb.init()` and have a unique tag for each search. This means that you'll easily be able to filter the project down to a given search by clicking that tag in the Project Page in the Runs Table. For example `wandb.init(tags='your_tag')`  docs for this can be found [here](../../ref/python/init.md).