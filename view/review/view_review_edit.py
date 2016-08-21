from Chimera.utils import model_to_dict
from django.http import HttpResponse
from Chimera.results import Result
from Chimera.models import Review
from json import dumps, loads


def review_edit(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.POST_ONLY)
            return HttpResponse(response, content_type='application/json')

        review_id = body.get('review_id')
        rating = body.get('rating')
        title = body.get('title')
        summary = body.get('summary')

        if not review_id:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except Review.MultipleObjectsReturned:
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        if rating:
            if type(rating) is not int or rating < 0 or rating > 10:
                response = Result.get_result_dump(Result.RATING_INVALID)
                return HttpResponse(response, content_type='application/json')
            else:
                review.rating = rating

        if title:
            review.title = title

        if summary:
            review.summary = summary

        try:
            review.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_UPDATE_REVIEW)
            return HttpResponse(response, content_type='application/json')

        if kwargs:
            return review

        response = {'review': model_to_dict(review)}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
