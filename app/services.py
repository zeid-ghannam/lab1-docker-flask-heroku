from app.models import db, Person, person_schema, persons_schema

class PersonService:
    @staticmethod
    def get_person(person_id):
        result = Person.query.get_or_404(person_id)
        return person_schema.dump(result)

    @staticmethod
    def get_all_persons():
        all_persons = Person.query.all()
        result = persons_schema.dump(all_persons)
        return result

    @staticmethod
    def create_person(name, age, address, work):
        person = Person(name=name, age=age, address=address, work=work)
        db.session.add(person)
        db.session.commit()
        return person_schema.dump(person)

    @staticmethod
    def update_person(person_id, name, age, address, work):
        person = Person.query.get_or_404(person_id)
        if person:
            person.name = name
            person.age = age
            person.address = address
            person.work = work
            db.session.commit()
        return person_schema.dump(person)

    @staticmethod
    def delete_person(person_id):
        person = Person.query.get_or_404(person_id)
        if person:
            db.session.delete(person)
            db.session.commit()
            return True
        return False
