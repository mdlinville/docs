---
title: "How do I switch between accounts on the same machine?"
<<<<<<< HEAD
tags:
   - 
---

=======
tags: []
---

### How do I switch between accounts on the same machine?
>>>>>>> 6ef6c45f4d73f19772f9c0cbb4fbccb2cee243c2
If you have two W&B accounts working from the same machine, you'll need a nice way to switch between your different API keys. You can store both API keys in a file on your machine then add code like the following to your repos. This is to avoid checking your secret key into a source control system, which is potentially dangerous.

```python
if os.path.exists("~/keys.json"):
    os.environ["WANDB_API_KEY"] = json.loads("~/keys.json")["work_account"]
```