from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

app = Flask(__name__)

engine = create_engine('sqlite:///ads.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Ad(Base):
    __tablename__ = 'ads'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = Column(String)


Base.metadata.create_all(bind=engine)


@app.route('/ads', methods=['POST'])
def create_ad():
    session = Session()

    title = request.json.get('title')
    description = request.json.get('description')
    owner = request.json.get('owner')

    ad = Ad(title=title, description=description, owner=owner)
    session.add(ad)
    session.commit()

    return jsonify(ad.id)


@app.route('/ads/<int:id>', methods=['GET'])
def get_ad(id):
    session = Session()

    ad = session.query(Ad).filter_by(id=id).first()
    if ad is None:
        return jsonify({'error': f'Ad with id {id} not found'})

    return jsonify({
        'id': ad.id,
        'title': ad.title,
        'description': ad.description,
        'created_at': ad.created_at.isoformat(),
        'owner': ad.owner
    })


@app.route('/ads/<int:id>', methods=['DELETE'])
def delete_ad(id):
    session = Session()

    ad = session.query(Ad).filter_by(id=id).first()
    if ad is None:
        return jsonify({'error': f'Ad with id {id} not found'})

    session.delete(ad)
    session.commit()

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)