## Python wrapper for muSSP 

Provided code allows you to construct a proper graph for the [muSSP implementation of min-cost flow multi-object tracking](https://github.com/yu-lab-vt/muSSP) and infer trajectories of detected objects (see `test.py` for usage details).

### Dependencies

```
networkx==2.6.3
```
### Input 
The input of the muSSP wrapper is a **list of detections' centroids per each frame** (*dim*: number of frames $\times$ number of detections $\times$ 2) + **list of corresponding detection confidences** (*dim*: number of frames $\times$ number of detections).

On top of that, you should specify the following parameters for the graph construction:
- cost_in, cost_out -- edge costs associated with the source/sink nodes 
- cost function -- custom function estimating correspondence strength between two detections. 
- transition_threshold -- filtering value for cost function output  

### Output

The `muSSP` function from `muSSP.py` returns a list of inter-frame relations between provided detections.  



