A set of visualization tools based on taichi GGUI. It intends to help debug simulation codes of taichi. 

一系列基于taichi GGUI的可视化小工具。主要目的是方便debug仿真代码。- 

please see this issue:
https://github.com/taichi-dev/taichi/issues/7853

## Roadmap
- Particles/faces selector
  - [ ] By drawing a rectangle with mouse, it should return the ids of the particles/faces and highlight them.
  - [ ] It should have two modes: penatration mode and surface selection mode, like paraview.
  - APIs: 

- Sparse grid visualizer
  - [ ] It should show the activated sparse grid with wireframed box, like Houdini.
  - APIs: 


- Matrix checker
  - [ ] It should show the pattern of a sparse matrix, like the `spy()` function in `scipy` or `MATLAB`. 
  - [ ] It should show the value of the matrix, with capability of zoom in/out
  - APIs:


