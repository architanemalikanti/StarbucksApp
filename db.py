from flask_sqlalchemy import SQLAlchemy
import datetime
import hashlib
import os
import bcrypt

db = SQLAlchemy()

association_table = db.Table("association", db.Model.metadata,
    db.Column("shiftLead_id", db.Integer, db.ForeignKey("shiftLead.id")),
    db.Column("baristas_id", db.Integer, db.ForeignKey("baristas.id"))
)


#class for a Barista. 
class Barista(db.Model):
    #name of model
    __tablename__ = "baristas"
    #user information:
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullName = db.Column(db.String, nullable=False)
    userName = db.Column(db.String, nullable=False)
    profilePictureUrl = db.Column(db.String, nullable=False)
    starbucksLocation = db.Column(db.String, nullable=False) #assuming that the starbucks location is a string
    shiftLead=db.relationship("ShiftLead", secondary=association_table,back_populates="baristas")
    password_digest = db.Column(db.String, nullable=False)

    #session information:
    session_token = db.Column(db.String, nullable=False)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)



    #now we need to initialize this object and serialize it
    #initialize:
    def __init__(self, **kwargs):
        """
        initialize an assignment object
        """
        self.fullName=kwargs.get("code", "")
        self.profilePictureUrl = kwargs.get("profilePictureUrl", "")
        self.starbucksLocation = kwargs.get("starbucksLocation", "")
        self.userName = kwargs.get("userName", "")
        self.password_digest= bcrypt.hashpw(kwargs.get("password").encode("utf-8"), bcrypt.gensalt(rounds=13))
        self.renew_session()

    #used to randomly generate/update session tokens:
    def _urlsafe_base_64(self):
        return hashlib.sha1(os.urandom(64)).hexdigest()
    
    def renew_session(self):
        self.session_token=self._urlsafe_base_64()
        self.session_expiration=datetime.datetime.now()+datetime.timedelta(days=1)
        self.update_token=self._urlsafe_base_64()

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password_digest)
    
    #checks if session token is valid and hasnt expired:
    def verify_session_token(self, session_token):
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration
    
    def verify_update_token(self, update_token):
        return update_token == self.update_token


    #serialize method
    def serialize(self):
        return{
            "id": self.id,
            "fullName": self.fullName,
            "profilePictureUrl": self.profilePictureUrl,
            "starbucksLocation": self.starbucksLocation,
            "shiftLead": [s.simple_serialize() for s in self.shiftLead]
        }
    
    #simple serialize method:
    def simple_serialize(self):
        return{
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "profilePictureUrl": self.profilePictureUrl,
            "starbucksLocation": self.starbucksLocation
        }
    
def create_barista(userName, password, fullName, starbucksLocation):
    existing_barista= Barista.query.filter(Barista.userName==userName).first()
    if existing_barista:
        return False, None
    
    Barista=Barista(userName=userName, password=password, fullName=fullName, starbucksLocation=starbucksLocation)
    db.session.add(Barista)
    db.session.commit()
    return True, Barista

def verify_credentials(userName, password):
    existing_barista= Barista.query.filter(Barista.userName==userName).first()
    if not existing_barista:
        return False, None
    
    return existing_barista.verify_password(password), existing_barista

def renew_session(update_token):
    existing_barista= Barista.query.filter(Barista.update_token==update_token).first()
    if not existing_barista:
        return False, None
    
    existing_barista.renew_session()
    db.session.commit()
    return True, existing_barista


def verify_session(session_token):
    return Barista.query.filter(Barista.session_token==session_token).first()





    



#class for a ShiftLead
class ShiftLead(db.Model):
    #name of model
    __tablename__ = "shiftLead"
    #columns
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    profilePictureUrl = db.Column(db.String, nullable=False)
    starbucksLocation = db.Column(db.String, nullable=False) #assuming that the starbucks location is a string
    baristas=db.relationship("Barista", secondary=association_table,back_populates="shiftLead")

    #now we need to initialize this object
    #initialize:
    def __init__(self, **kwargs):
        """
        initialize an assignment object
        """
        self.firstName=kwargs.get("code", "")
        self.lastName=kwargs.get("name", "")
        self.profilePictureUrl = kwargs.get("profilePictureUrl", "")
        self.starbucksLocation = kwargs.get("starbucksLocation", "")


    #serialize method
    def serialize(self):
        return{
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "profilePictureUrl": self.profilePictureUrl,
            "starbucksLocation": self.starbucksLocation,
            "baristas": [b.simple_serialize() for b in self.baristas]
        }
    
    #simple serialize method:
    def simple_serialize(self):
        return{
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "profilePictureUrl": self.profilePictureUrl,
            "starbucksLocation": self.starbucksLocation
        }
    






#class for a Pastry Pull. 
class PastryPull(db.Model):
    #name of model
    __tablename__ = "pastrypull"

    #columns
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateToday = db.Column(db.DateTime, nullable=False)

    #images of all the pastries: inputs to the ML model
    imageOfCheeseDanish = db.Column(db.String, nullable=False)
    imageOfChocolateCroissant = db.Column(db.String, nullable=False)
    imageOfButterCroissant = db.Column(db.String, nullable=False)
    imageOfBanannaLoaf = db.Column(db.String, nullable=False)
    imageOfLemonLoad = db.Column(db.String, nullable=False)
    imageOfPumpkinLoaf = db.Column(db.String, nullable=False)
    imageOfBlueberryMuffin = db.Column(db.String, nullable=False)
    imageOfVanillaBeanScone = db.Column(db.String, nullable=False)
    imageOfCoffeeCake = db.Column(db.String, nullable=False)
    imageOfCookiesAndCreamCakePop = db.Column(db.String, nullable=False)
    imageOfBirthdayCakePop = db.Column(db.String, nullable=False)
    imageOfChocolateCakePop = db.Column(db.String, nullable=False)
    imageOfChocolateChipCookie = db.Column(db.String, nullable=False)

    #output the to ML model: the number of each pastry on the shelf right now
    numberOfCheeseDanish = db.Column(db.Integer, nullable=False)
    numberOfChocolateCroissant = db.Column(db.Integer, nullable=False)
    numberOfButterCroissant = db.Column(db.Integer, nullable=False)
    numberOfBanannaLoaf = db.Column(db.Integer, nullable=False)
    numberOfLemonLoad = db.Column(db.Integer, nullable=False)
    numberOfPumpkinLoaf = db.Column(db.Integer, nullable=False)
    numberOfBlueberryMuffin = db.Column(db.Integer, nullable=False)
    numberOfVanillaBeanScone = db.Column(db.Integer, nullable=False)
    numberOfCoffeeCake = db.Column(db.Integer, nullable=False)
    numberOfCookiesAndCreamCakePop = db.Column(db.Integer, nullable=False)
    numberOfBirthdayCakePop = db.Column(db.Integer, nullable=False)
    numberOfChocolateCakePop = db.Column(db.Integer, nullable=False)
    numberOfChocolateChipCookie = db.Column(db.Integer, nullable=False)

    
    #the second output to the ML model: how many of each pastry we need to throw away. 
    numberOfCheeseDanishToThrowAway = db.Column(db.Integer, nullable=False)
    numberOfChocolateCroissantToThrowAway = db.Column(db.Integer, nullable=False)
    numberOfButterCroissantToThrowAway = db.Column(db.Integer, nullable=False)
    numberOfBanannaLoafToThrowAway = db.Column(db.Integer, nullable=False)
    numberOfLemonLoadToThrowAway = db.Column(db.Integer, nullable=False)
    numberOfPumpkinLoafToThrowAway = db.Column(db.Integer, nullable=False)
    numberOfBlueberryMuffinToThrowAway = db.Column(db.Integer, nullable=False)
    numberOfVanillaBeanSconeToThrowAway = db.Column(db.Integer, nullable=False)
    numberOfCoffeeCakeToThrowAway = db.Column(db.Integer, nullable=False)
    numberOfCookiesAndCreamCakePopToThrowAway = db.Column(db.Integer, nullable=False)
    numberOfBirthdayCakePopToThrowAway = db.Column(db.Integer, nullable=False)
    numberOfChocolateCakePopToThrowAway = db.Column(db.Integer, nullable=False)
    numberOfChocolateChipCookieToThrowAway = db.Column(db.Integer, nullable=False)


    #which barista did the pull:
    baristaWhoDidThePull = db.Column(db.String, db.ForeignKey('baristas.id'), nullable=False)


    #now we need to initialize this object
    #initialize:
    def __init__(self, **kwargs):
        """
        initialize an assignment object
        """
        self.dateToday = datetime.datetime.now()
        self.imageOfCheeseDanish = kwargs.get("imageOfCheeseDanish", "")
        self.imageOfChocolateCroissant = kwargs.get("imageOfChocolateCroissant", "")
        self.imageOfButterCroissant = kwargs.get("imageOfButterCroissant", "")
        self.imageOfBanannaLoaf = kwargs.get("imageOfBanannaLoaf", "")
        self.imageOfLemonLoad = kwargs.get("imageOfLemonLoad", "")
        self.imageOfPumpkinLoaf = kwargs.get("imageOfPumpkinLoaf", "")
        self.imageOfBlueberryMuffin = kwargs.get("imageOfBlueberryMuffin", "")
        self.imageOfVanillaBeanScone = kwargs.get("imageOfVanillaBeanScone", "")
        self.imageOfCoffeeCake = kwargs.get("imageOfCoffeeCake", "")
        self.imageOfCookiesAndCreamCakePop = kwargs.get("imageOfCookiesAndCreamCakePop", "")
        self.imageOfBirthdayCakePop = kwargs.get("imageOfBirthdayCakePop", "")
        self.imageOfChocolateCakePop = kwargs.get("imageOfChocolateCakePop", "")
        self.imageOfChocolateChipCookie = kwargs.get("imageOfChocolateChipCookie", "")


        self.numberOfCheeseDanish = kwargs.get("numberOfCheeseDanish", 0)
        self.numberOfChocolateCroissant = kwargs.get("numberOfChocolateCroissant", 0)
        self.numberOfButterCroissant = kwargs.get("numberOfButterCroissant", 0)
        self.numberOfBanannaLoaf = kwargs.get("numberOfBanannaLoaf", 0)
        self.numberOfLemonLoad = kwargs.get("numberOfLemonLoad", 0)
        self.numberOfPumpkinLoaf = kwargs.get("numberOfPumpkinLoaf", 0)
        self.numberOfBlueberryMuffin = kwargs.get("numberOfBlueberryMuffin", 0)
        self.numberOfVanillaBeanScone = kwargs.get("numberOfVanillaBeanScone", 0)
        self.numberOfCoffeeCake = kwargs.get("numberOfCoffeeCake", 0)
        self.numberOfCookiesAndCreamCakePop = kwargs.get("numberOfCookiesAndCreamCakePop", 0)
        self.numberOfBirthdayCakePop = kwargs.get("numberOfBirthdayCakePop", 0)
        self.numberOfChocolateCakePop = kwargs.get("numberOfChocolateCakePop", 0)
        self.numberOfChocolateChipCookie = kwargs.get("numberOfChocolateChipCookie", 0)


        self.numberOfCheeseDanishToThrowAway = kwargs.get("numberOfCheeseDanishToThrowAway", 0)
        self.numberOfChocolateCroissantToThrowAway = kwargs.get("numberOfChocolateCroissantToThrowAway", 0)
        self.numberOfButterCroissantToThrowAway = kwargs.get("numberOfButterCroissantToThrowAway", 0)
        self.numberOfBanannaLoafToThrowAway = kwargs.get("numberOfBanannaLoafToThrowAway", 0)
        self.numberOfLemonLoadToThrowAway = kwargs.get("numberOfLemonLoadToThrowAway", 0)
        self.numberOfPumpkinLoafToThrowAway = kwargs.get("numberOfPumpkinLoafToThrowAway", 0)
        self.numberOfBlueberryMuffinToThrowAway = kwargs.get("numberOfBlueberryMuffinToThrowAway", 0)
        self.numberOfVanillaBeanSconeToThrowAway = kwargs.get("numberOfVanillaBeanSconeToThrowAway", 0)
        self.numberOfCoffeeCakeToThrowAway = kwargs.get("numberOfCoffeeCakeToThrowAway", 0)
        self.numberOfCookiesAndCreamCakePopToThrowAway = kwargs.get("numberOfCookiesAndCreamCakePopToThrowAway", 0)
        self.numberOfBirthdayCakePopToThrowAway = kwargs.get("numberOfBirthdayCakePopToThrowAway", 0)
        self.numberOfChocolateCakePopToThrowAway = kwargs.get("numberOfChocolateCakePopToThrowAway", 0)
        self.numberOfChocolateChipCookieToThrowAway = kwargs.get("numberOfChocolateChipCookieToThrowAway", 0)


    #serialize method
    def serialize(self):
        return{

            "id": self.id,
            "dateToday": self.dateToday,
            "imageOfCheeseDanish": self.imageOfCheeseDanish,
            "imageOfChocolateCroissant": self.imageOfChocolateCroissant,
            "imageOfButterCroissant": self.imageOfButterCroissant,
            "imageOfBanannaLoaf": self.imageOfBanannaLoaf,
            "imageOfLemonLoad": self.imageOfLemonLoad,
            "imageOfPumpkinLoaf": self.imageOfPumpkinLoaf,
            "imageOfBlueberryMuffin": self.imageOfBlueberryMuffin,
            "imageOfVanillaBeanScone": self.imageOfVanillaBeanScone,
            "imageOfCoffeeCake": self.imageOfCoffeeCake,
            "imageOfCookiesAndCreamCakePop": self.imageOfCookiesAndCreamCakePop,
            "imageOfBirthdayCakePop": self.imageOfBirthdayCakePop,
            "imageOfChocolateCakePop": self.imageOfChocolateCakePop,
            "imageOfChocolateChipCookie": self.imageOfChocolateChipCookie,

            "numberOfCheeseDanish": self.numberOfCheeseDanish,
            "numberOfChocolateCroissant": self.numberOfChocolateCroissant,
            "numberOfButterCroissant": self.numberOfButterCroissant,
            "numberOfBanannaLoaf": self.numberOfBanannaLoaf,
            "numberOfLemonLoad": self.numberOfLemonLoad,
            "numberOfPumpkinLoaf": self.numberOfPumpkinLoaf,
            "numberOfBlueberryMuffin": self.numberOfBlueberryMuffin,
            "numberOfVanillaBeanScone": self.numberOfVanillaBeanScone,
            "numberOfCoffeeCake": self.numberOfCoffeeCake,
            "numberOfCookiesAndCreamCakePop": self.numberOfCookiesAndCreamCakePop,
            "numberOfBirthdayCakePop": self.numberOfBirthdayCakePop,
            "numberOfChocolateCakePop": self.numberOfChocolateCakePop,
            "numberOfChocolateChipCookie": self.numberOfChocolateChipCookie,

            "numberOfCheeseDanishToThrowAway": self.numberOfCheeseDanishToThrowAway,
            "numberOfChocolateCroissantToThrowAway": self.numberOfChocolateCroissantToThrowAway,
            "numberOfButterCroissantToThrowAway": self.numberOfButterCroissantToThrowAway,
            "numberOfBanannaLoafToThrowAway": self.numberOfBanannaLoafToThrowAway,
            "numberOfLemonLoadToThrowAway": self.numberOfLemonLoadToThrowAway,
            "numberOfPumpkinLoafToThrowAway": self.numberOfPumpkinLoafToThrowAway,
            "numberOfBlueberryMuffinToThrowAway": self.numberOfBlueberryMuffinToThrowAway,
            "numberOfVanillaBeanSconeToThrowAway": self.numberOfVanillaBeanSconeToThrowAway,
            "numberOfCoffeeCakeToThrowAway": self.numberOfCoffeeCakeToThrowAway,
            "numberOfCookiesAndCreamCakePopToThrowAway": self.numberOfCookiesAndCreamCakePopToThrowAway,
            "numberOfBirthdayCakePopToThrowAway": self.numberOfBirthdayCakePopToThrowAway,
            "numberOfChocolateCakePopToThrowAway": self.numberOfChocolateCakePopToThrowAway,
            "numberOfChocolateChipCookieToThrowAway": self.numberOfChocolateChipCookieToThrowAway,
            "baristaWhoDidThePull": self.baristaWhoDidThePull.simple_serialize()
        }
    
    


