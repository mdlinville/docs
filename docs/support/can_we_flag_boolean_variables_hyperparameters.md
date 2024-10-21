---
title: "Can we flag boolean variables as hyperparameters?"
<<<<<<< HEAD
tags:
   - sweeps
---

=======
tags: []
---

### Can we flag boolean variables as hyperparameters?
>>>>>>> 6ef6c45f4d73f19772f9c0cbb4fbccb2cee243c2
You can use the `${args_no_boolean_flags}` macro in the command section of the config to pass hyperparameters as boolean flags. This will automatically pass in any boolean parameters as flags. When `param` is `True` the command will receive `--param`, when `param` is `False` the flag will be omitted.