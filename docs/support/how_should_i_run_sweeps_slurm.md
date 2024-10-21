---
title: "How should I run sweeps on SLURM?"
<<<<<<< HEAD
tags:
   - sweeps
---

=======
tags: []
---

### How should I run sweeps on SLURM?
>>>>>>> 6ef6c45f4d73f19772f9c0cbb4fbccb2cee243c2
When using sweeps with the [SLURM scheduling system](https://slurm.schedmd.com/documentation.html), we recommend running `wandb agent --count 1 SWEEP_ID` in each of your scheduled jobs, which will run a single training job and then exit. This makes it easier to predict runtimes when requesting resources and takes advantage of the parallelism of hyperparameter search.