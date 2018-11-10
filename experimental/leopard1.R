

#         xcor, ycor, gender, age, fedstate, 

leopard <- array(dim=c(2,5))
leopard[1,] = c(0, 0, 1, 3, 0)


dx = 1
dy = 1
for (k in c(1:100)) {

	leopard[1,1] = leopard[1,1] + dx
	leopard[1,2] = leopard[1,2] + dy
	leopard[2,1] = leopard[2,1] + dy
}
