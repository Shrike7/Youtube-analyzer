var adminUsername = process.env.MONGO_INITDB_ROOT_USERNAME;
var adminPassword = process.env.MONGO_INITDB_ROOT_PASSWORD;
var adminDb       = process.env.MONGO_INITDB_ROOT_DATABASE;

var dbUsername    = process.env.MONGO_DB_USER;
var dbPassword    = process.env.MONGO_DB_PASSWORD;
var dbName        = process.env.MONGO_DB_NAME;


var admin = db.getSiblingDB(adminDb);
admin.auth(adminUsername, adminPassword);

db = db.getSiblingDB(dbName);

db.createUser({
    user: dbUsername,
    pwd: dbPassword,
    roles: [
        {
            role: 'dbOwner',
            db: dbName,
        },
    ],
});
