db = db.getSiblingDB('r18'),
db.createUser({
    user: "r18",
    pwd: "r18_mongo_password",
    roles: ["readWrite"]
});
