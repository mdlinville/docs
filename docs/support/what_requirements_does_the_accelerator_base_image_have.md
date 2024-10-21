---
title: "What requirements does the accelerator base image have?"
<<<<<<< HEAD
tags:
   - launch
---

=======
tags: []
---

### What requirements does the accelerator base image have?
>>>>>>> 6ef6c45f4d73f19772f9c0cbb4fbccb2cee243c2
For jobs that use an accelerator, an accelerator base image with the required accelerator components installed can be provided. Other requirements for the provided accelerator image include:
- Debian compatibility (the Launch Dockerfile uses apt-get to fetch python )
- Compatibility CPU & GPU hardware instruction set (Make sure your CUDA version is supported by the GPU you intend on using)
- Compatibility between the accelerator version you provide and the packages installed in your ML algorithm
- Packages installed that require extra steps for setting up compatibility with hardware