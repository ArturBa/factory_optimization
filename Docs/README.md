# Factory
![factory image](img/Factory_scheme.png "factory model")

## Factory main goal function:  
  
$Income = \sum^{n_i}_{i=0}(p_i*v_i) - \sum^{n_w}_{i = 0}(w_i*s_i*t_i) - n_m*m_p - p_{un}*\sum^{n_i}_{i=0}(r_i-p_i)*v_i$  
  
Where:   
- $n_i$ -- number of item types  
- $n_w$ -- number of types of employees  
- $n_m$ -- number of materials  
- $p_i$ -- the number of the i-th subject  
- $r_i$ -- the required number of the i-th subject  
- $v_i$ -- the value of the i-th subject  
- $w_i$ -- number of i-th employees
- $s_i$ -- the value of employees' salary  
- $t_i$ -- working time of i-th employees  
- $m_p$ -- material price
- $p_{un}$ -- punishment rate 

Last submission is valid only if: $r_i - p_i > 0$


### Product value
$q_i =  \frac{t_{wi}}{t_{bi}} ∗ w_q ∗ 100\%$
$v_i = v_{bi} * q_i$

Where:
- $t_{wi}$ -- real working time of the i-th machine for one product  
- $t_{bi}$ -- basic working time of the i-th machine for one product  
- $v_{bi}$ -- the basic value of the product from the i-th machine  
- $q_i$ -- the quality of the product from the i-th machine  
- $w_q$ -- employee quality (depends on the bonus)  
### Product time 
$t_{mi} =\frac{t_{pi}}{t_{wi}}+p*\frac{t_{wi}}{t_{bi}}$

Where: 
- $t_{pi}$ -- preparation time for the i-th machine  
- $t_{mi}$ - working time of the i-th machine for the whole day  


## Model assumption
Parameter | value
----|---
Material number | [$x$ - 100]
Material cost   | 15
Working time | [1 - 16]
Quality | [0.9 - 1.1]
Minimal number of big parts | [0 - 10]
Minimal number of small parts | [0 -10]
Big machine worker sallary | 70
Big machine material requirments | 4
Big machine preparation time | 30 min
Base big machine item value | 50
Base big machine working time per item | 1h
Number of big machines | [0 - 10]
Small machine worker sallary | 60
Small machine material requirments | 3
Big machine preparation time | 45 min
Base small machine item value | 35
Base small machine working time per item | 45 min
Number of small machines | [0 - 10]
Max working time per worker | 8h
Worker bonus | [0.0 - 0.2]
Punishment rate | 1.5

Where:
- $x$ -- number of required parts * cost of part
- Input parameters are given in square brackets
- Worker is hired on full time. Must work 8h 
- First and second shifts are equal in machine and workers number

