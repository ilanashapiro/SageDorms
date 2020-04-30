def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

suite1ID = randomString()
suite2ID = randomString()
suite3ID = randomString()
suite4ID = randomString()
suite5ID = randomString()
suite6ID = randomString()

INSERT INTO SUITE (suiteID, isSubFree, numRooms)

CREATE TABLE IF NOT EXISTS Suite (
   suiteID VARCHAR(50) NOT NULL,
   isSubFree BOOLEAN NOT NULL,
   numRooms INT NOT NULL,
   numPeople INT NOT NULL,
   dormName VARCHAR(50) NOT NULL,
   otherDescription VARCHAR(100),
