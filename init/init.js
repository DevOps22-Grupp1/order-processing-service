db.createUser({
	user: "order_admin",
	pwd: "password",
	roles: [
		{
			role: "readWrite",
			db: "orders",
		},
	],
});

db.createCollection("orders");
db.orders.insertMany([
	{
		order: "Samsung Galaxy S10",
		price: 999.99,
		customer: "Max Svensson",
		quantity: 2,
	},
	{
		order: "LG G8 ThinQ",
		price: 1499.99,
		customer: "Jarl Svensson",
		quantity: 1,
	},
	{
		order: "MSI GS65 Stealth Thin",
		price: 499.99,
		customer: "Harisha Svensson",
		quantity: 3,
	},
	{
		order: "Bowers & Wilkins PX7",
		price: 799.99,
		customer: "Dennis Svensson",
		quantity: 1,
	},
	{
		order: "Apple AirPods Pro",
		price: 699.99,
		customer: "Simon Svensson",
		quantity: 4,
	},
	{
		order: "Air Jordan 1 Retro High OG",
		price: 2099.99,
		customer: "Zoreh Svensson",
		quantity: 2,
	},
]);
