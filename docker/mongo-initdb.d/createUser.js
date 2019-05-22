db = db.getSiblingDB('r18'),
db.createUser({
    user: "r18",
    pwd: "r18password",
    roles: ["readWrite"]
});
