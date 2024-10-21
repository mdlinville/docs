---
title: "What permissions does the agent require in Kubernetes?"
<<<<<<< HEAD
tags:
   - launch
---

=======
tags: []
---

### What permissions does the agent require in Kubernetes?
>>>>>>> 6ef6c45f4d73f19772f9c0cbb4fbccb2cee243c2
“The following kubernetes manifest will create a role named
`wandb-launch-agent` in the`wandb`namespace. This role will allow the agent to create pods, configmaps, secrets, and pods/log in the `wandb` namespace. The `wandb-cluster-role` will allow the agent to create pods, pods/log, secrets, jobs, and jobs/status in any namespace of your choice.”