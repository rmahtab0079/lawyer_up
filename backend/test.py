import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('lawyer-up-dubhacks-firebase-adminsdk-bg7wy-142f040934.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
wrongful_dismissal_ref = db.collection(u'wrongful-dismissal')
docs = wrongful_dismissal_ref.stream()

numInDB = 0
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))
    numInDB += 1
print('db initialized')
print(numInDB)