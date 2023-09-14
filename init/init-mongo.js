db.createUser({
	user: "order_admin",
	pwd: "password",
	roles: [
		{
			role: "readWrite",
			db: "all_orders",
		},
	],
});

db.createCollection("orders");
db.orders.insertMany([
	{
		id:1,
		userid:1,
		productid: 1
	},
	{
		id:2,
		userid:2,
		productid: 3
	},
	{
		id:3,
		userid:3,
		productid: 2
	},
	{
		id:4,
		userid:4,
		productid: 5
	},
	{
		id:5,
		userid:5,
		productid: 6

	},
	{
		id:6,
		userid:6,
		productid: 4
	},
]);
