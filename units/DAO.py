from units.models import EmotionColour, Record  # Import the models
from units.db_init import db  # Import the db session

class EmotionColourDAO:
    # No __init__ needed, since we are not instantiating

    @staticmethod
    def get_emotion_by_id(emotion_id):
        return db.session.query(EmotionColour).filter_by(emotion_id=emotion_id).first()

    
    @staticmethod
    def get_emotion_record_by_emotion(emotion_name):
        return db.session.query(EmotionColour).filter_by(emotion_name=emotion_name).first()
    
    @staticmethod
    def update_emotion(emotion_id, **kwargs):
        emotion = EmotionColourDAO.get_emotion_by_id(emotion_id)
        if emotion:
            # Update all provided fields dynamically
            for key, value in kwargs.items():
                setattr(emotion, key, value)
            try:
                db.session.commit()  # Save changes
                return emotion
            except Exception as e:
                db.session.rollback()
                print(f"Error updating emotion: {e}")
                return None
        return None
    
    @staticmethod
    def get_all_emotions():
        return db.session.query(EmotionColour).all()

    @staticmethod
    def create_emotion(emotion_name, **colour_values):
        new_emotion = EmotionColour(emotion_name=emotion_name, **colour_values)
        db.session.add(new_emotion)
        db.session.commit()
        return new_emotion

    @staticmethod
    def update_emotion(emotion_id, **kwargs):
        emotion = EmotionColourDAO.get_emotion_by_id(emotion_id)
        if emotion:
            for key, value in kwargs.items():
                setattr(emotion, key, value)
            db.session.commit()
            return emotion
        return None

    @staticmethod
    def delete_emotion(emotion_id):
        emotion = EmotionColourDAO.get_emotion_by_id(emotion_id)
        if emotion:
            db.session.delete(emotion)
            db.session.commit()
            return True
        return False
    
     # New function to get all colour values for a specific emotion
    @staticmethod
    def get_emotion_colours(emotion_name, available_colours):
        # Query the database for the emotion with the matching name
        emotion_record = EmotionColour.query.filter_by(emotion_name=emotion_name).first()
        
        if emotion_record:
            # List of colour column names to extract values from
            
            
            # Create a dictionary with the color names as keys and their values
            emotion_colours = {colour: getattr(emotion_record, colour) for colour in available_colours}
            return emotion_colours
        else:
            return None  # If no matching emotion is found


class RecordDAO:
    # No __init__ needed, since we are not instantiating

    @staticmethod
    def get_record_by_id(record_id):
        return db.session.query(Record).filter_by(record_id=record_id).first()

    @staticmethod
    def get_all_records():
        return db.session.query(Record).all()

    @staticmethod
    def create_record(emotion_name, likelihood_score, colour_displayed, record_date, colour_match):
        new_record = Record(
            emotion_name=emotion_name,
            likelihood_score=likelihood_score,
            colour_displayed=colour_displayed,
            record_date=record_date,
            colour_match=colour_match
        )
        db.session.add(new_record)
        db.session.commit()
        return new_record

    @staticmethod
    def update_record(record_id, **kwargs):
        record = RecordDAO.get_record_by_id(record_id)
        if record:
            for key, value in kwargs.items():
                setattr(record, key, value)
            db.session.commit()
            return record
        return None

    @staticmethod
    def delete_record(record_id):
        record = RecordDAO.get_record_by_id(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return True
        return False
