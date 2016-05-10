from modules import parse
from modules import ID3
from modules import pruning
from modules import graph

(t_array,t_attributes)=parse.parse('/Users/Ben/Documents/Programming/Class/eecs349/ml_ps2/data/test_btrain.csv',False)
(v_array,v_attributes)=parse.parse('/Users/Ben/Documents/Programming/Class/eecs349/ml_ps2/data/test_bvalidate.csv',False)

graph.get_graph(t_array,t_attributes,v_array,[2,2,2,2,2,2,2,2,2,2,2,2,2,2],16,3,0.1,1.0,0.1)
# print d