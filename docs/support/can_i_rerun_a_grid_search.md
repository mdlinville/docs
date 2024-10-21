---
title: "Can I rerun a grid search?"
<<<<<<< HEAD
tags:
   - sweeps
---

=======
tags: []
---

### Can I rerun a grid search?
>>>>>>> 6ef6c45f4d73f19772f9c0cbb4fbccb2cee243c2
Yes. If you exhaust a grid search but want to re-execute some of the W&B Runs (for example because some crashed). Delete the W&B Runs ones you want to re-execute, then choose the **Resume** button on the [sweep control page](./sweeps-ui.md). Finally, start new W&B Sweep agents with the new Sweep ID.

Parameter combinations with completed W&B Runs are not re-executed.