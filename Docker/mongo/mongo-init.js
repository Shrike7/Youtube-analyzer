var admin = db.getSiblingDB('admin');
admin.auth('root', 'root');

db = db.getSiblingDB('youtube_analyzer')

db.createUser({
    user: 'django',
    pwd: 'django',
    roles: [
      {
        role: 'dbOwner',
      db: 'youtube_analyzer',
    },
  ],
});
