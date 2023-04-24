# Gomory solver

Program find integer solution of minimazation/maximization linear function with several linear constraints (Algorithm Gomory).

## Example
### Input
$$
3x_1 - 5x_2 + 3x_3 \to max
$$

$$
\begin{cases}
3x_1 + x_2 - x_3 \ge 12 \\
2x_1 + 5x_2 - 2x_3 = 20 \\
-x_1 + x_2 + 3x_3 \le 16
\end{cases}
$$

$$
x_j \ge 0, j=\overline{1,3}
$$

### Console output
```
TOTAL NUMBER OF STEPS: 4
F_max=108
X*=(23, 0, 13, 44)
```

### Excel output
