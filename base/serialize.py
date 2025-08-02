
from .models import Question

def serialize_questions(city_name):
    qs = Question.objects.filter(city__name=city_name).prefetch_related('answer_set')
    data = []
    for q in qs:
        data.append({
            'id': q.id,
            'city': city_name,
            'text': q.text,
            'img': q.imageURL if q.img else None,
            'answers': [
                {'id': a.id, 'text': a.text, 'is_correct': a.correct}
                for a in q.answer_set.all()
            ]
        })
    return data
